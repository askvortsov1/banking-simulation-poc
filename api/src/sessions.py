from .exceptions import NoActiveAccount, SessionClosed, PermissionDenied, NoAvailableStaff
from .people import Person
from ..settings import MANAGER, ASSISTANT_MANAGER, TELLER, MIN_LARGE_TRANSFER


class Session:
    def __init__(self, user, bank):
        if not isinstance(user, Person):
            raise TypeError("User must be a Person")
        self._user = user
        self._bank = bank
        self._closed = False
        self._account = None

    def _check_session_active(self):
        if self._closed or not self._user:
            raise SessionClosed("This session is not active.")

    def _check_active_account_selected(self):
        if not self._account:
            raise NoActiveAccount("You must select an active account before you can complete this operation.")

    def get_accounts(self):
        self._check_session_active()
        return self._bank.get_accounts_for_user(self._user)

    def set_active_account(self, account):
        self._check_session_active()
        self._account = self._bank.get_and_validate_account(account, self._user)

    def check_balance(self):
        self._check_session_active()
        self._check_active_account_selected()
        return self._account.get_balance()

    def deposit(self, amount, checks=[]):
        self._check_session_active()
        self._check_active_account_selected()
        return self._account.deposit(amount, checks)

    def withdraw(self, amount):
        self._check_session_active()
        self._check_active_account_selected()
        return self._account.withdraw(amount)

    def make_check(self, amount, payable_to):
        self._check_session_active()
        self._check_active_account_selected()
        return self._account.make_check(amount, payable_to)

    def close(self):
        self._closed = True


class ATMSession(Session):
    def __init__(self, user, atm):
        super().__init__(user, atm.bank)


class BranchSession(Session):
    def __init__(self, user, branch):
        super().__init__(user, branch.bank)
        self.branch = branch
        self._staff_assisting = None

    def _request_staff_assistance(self, permission_level):
        if not self._staff_assisting or self._staff_assisting.permission_level < permission_level:

            # If staff already assigned, but insufficient permissions, unassign them.
            if self._staff_assisting is not None:
                self.branch.unassign_staff_member(self._staff_assisting)
                self._staff_assisting = None

            # Request and assign a new staff member to assist.
            staff = self.branch.get_available_staff_member(permission_level)
            if staff is None:
                raise NoAvailableStaff("No staff with required permissions are currently available to assist you. Please try again later.")
            self._staff_assisting = staff
            self.branch.assign_staff_member(staff)

    def check_balance(self):
        self._request_staff_assistance(TELLER)
        return super().check_balance()

    def deposit(self, amount, checks=[]):
        self._request_staff_assistance(TELLER)
        return super().deposit(amount, checks)

    def withdraw(self, amount):
        self._request_staff_assistance(TELLER)
        return super().withdraw(amount)

    def get_account_options(self):
        self._check_session_active()
        return self._bank.account_options

    def open_account(self, config_option, initial_deposit=0):
        self._check_session_active()
        self._request_staff_assistance(MANAGER)
        self._bank.open_account(config_option, self._user, initial_deposit)

    def close_account(self):
        self._check_session_active()
        self._check_active_account_selected()
        self._request_staff_assistance(MANAGER)
        self._account.close()

    def add_signer_to_account(self, other_user):
        self._check_session_active()
        self._check_active_account_selected()
        self._request_staff_assistance(MANAGER)
        self._account.add_signer(other_user)

    def remove_signer_from_account(self, other_user):
        self._check_session_active()
        self._check_active_account_selected()
        self._request_staff_assistance(MANAGER)
        self._account.remove_signer(other_user)

    # TODO
    def open_loan(self, amount):
        self._check_session_active()
        self._check_active_account_selected()
        self._request_staff_assistance(ASSISTANT_MANAGER)
        self._bank.open_loan(amount, self._user)

    # TODO
    def pay_towards_loan(self, loan, user):
        self._check_session_active()
        self._check_active_account_selected()
        self._request_staff_assistance(TELLER)

    def transfer_to_different_account(self, receiving_account, amount):
        self._check_session_active()
        if amount > MIN_LARGE_TRANSFER:
            self._request_staff_assistance(ASSISTANT_MANAGER)
        else:
            self._request_staff_assistance(TELLER)
        if not self._bank.get_and_validate_account(receiving_account, self._user):
            raise PermissionDenied("You do not have access to receiving account.")

        self.withdraw(amount)
        receiving_account.deposit(amount)

    def close(self):
        self.branch.unassign_staff_member(self._staff_assisting)
        self._staff_assisting = None
        super().close()

