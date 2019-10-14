from flask_restful import Resource, reqparse

import config
from flask import abort
from app import db
from utils import json_serialize
from models import Account, AccountConfig, Bank, Check, Transaction, User


def _deposit_check(check):
    """Helper method for depositing check in transaction

    Withdraw amount from issuing account, then mark check as deposited

    Arguments:
        check {Check} -- Check being deposited
    """
    transaction = _gen_withdraw_transaction(check.issuing_account, -1 * check.amount, description="Check Payment")
    check.issuing_account.process_transaction(transaction)
    check.deposit()


def _gen_deposit_transaction(account, cash_amount, description=None, checks=[]):
    """Helper method for processing deposits

    Separate checks into valid and invalid.
    If any are invalid, terminate and return invalid check ids in error message.
    If all are good, process deposit on all checks and return generated deposit transaction

    Arguments:
        account {Account} -- Account being deposited from
        cash_amount {float} -- Amount being deposited

    Keyword Arguments:
        description {str} -- Optional description for transaction (default: {None})
        checks {list[Check]} -- List of Check objects being deposited

    Returns:
        Transaction -- Transaction object
    """
    good_checks = []
    failed_checks = []
    for check in checks:
        good_checks.append(check) if check.validate(account) else failed_checks.append(check)

    if failed_checks:
        abort(400, "Checks #s {} Are Invalid".format(", ".join([str(check.id) for check in failed_checks])))

    for check in good_checks:
        # This will withdraw relevant amount from issuing account. If failed, no changes would be applied to the database.
        _deposit_check(check)

    # All Good
    transaction = Transaction(
        account=account,
        cash_amount=cash_amount,
        checks=good_checks,
        fees=account.config.deposit_fee,
        description=description or "Deposit"
    )
    db.session.add(transaction)
    return transaction


def _gen_withdraw_transaction(account, cash_amount, description=None):
    """Helper method for processing withdrawals
    Check if savings and if max number of withdrawals for savings has been reached.
    Check if overdraft allowed, and if current transaction qualifies for overdraft protection
    Generate transaction if all of above successful.

    Arguments:
        account {Account} -- Account being withdrawn from
        cash_amount {float} -- Amount being withdrawn

    Keyword Arguments:
        description {str} -- Optional description for transaction (default: {None})

    Returns:
        Transaction -- Transaction object
    """
    cash_amount = abs(cash_amount) * -1
    fees = abs(account.config.withdrawal_fee)
    # Check withdrawal limit
    if account.config.is_savings and account.withdrawals_last_month >= config.SAVINGS_ACCOUNT_MAX_WITHDRAWALS_PER_MONTH:
        abort(403, "You can only withdraw from a saving account {} times each month".format(
            config.SAVINGS_ACCOUNT_MAX_WITHDRAWALS_PER_MONTH))
    # Check Overdraft
    if account._balance + cash_amount < 0:
        if not account.config.allow_overdraft:
            abort(403, "Withdrawal amount exceeds balance, and this account does not allow you to overdraft.")
        if account.balance + cash_amount < -1 * account.config.overdraft_limit:
            abort(403, "Withdrawal amount exceeds balance, and you have exceeded this account's overdraft limit")
        # Overdraft allowed, apply Overdraft Fee
        fees += account.config.overdraft_fee

    # All Good
    transaction = Transaction(
        account=account,
        cash_amount=cash_amount,
        fees=fees,
        description=description or "Withdrawal"
    )
    db.session.add(transaction)
    return transaction


_account_config_fields = {
    "name": str,
    "is_savings": bool,
    "is_checking": bool,
    "min_opening_balance": float,
    "interest": float,
    "deposit_fee": float,
    "withdrawal_fee": float,
    "allow_overdraft": bool,
    "overdraft_limit": float,
    "overdraft_fee": float
}

_account_config_create_parser = reqparse.RequestParser()
_account_config_update_parser = reqparse.RequestParser()
for field, type_ in _account_config_fields.items():
    _account_config_create_parser.add_argument(field, type=type_, required=True, help="No {} Provided".format(field.capitalize()), location="json")
    _account_config_update_parser.add_argument(field, type=type_, required=False, help="No {} Provided".format(field.capitalize()), location="json")


class AccountConfigListApi(Resource):
    """API Endpoint for bank's account config options
    """
    def get(self, bank_id):
        """API Endpoint to get all Account Configs for a bank.
        """
        bank = Bank.query.get_or_404(bank_id)
        config_options = bank.account_configs
        return json_serialize(config_options)

    def put(self, bank_id):
        """API Endpoint to add account config for a bank
        """
        args = _account_config_create_parser.parse_args()
        bank = Bank.query.get_or_404(bank_id)
        conf = AccountConfig(bank=bank, **args)
        conf.check_account_type_valid()
        db.session.add(conf)
        db.session.commit()
        return json_serialize(conf)


class AccountConfigApi(Resource):
    """API Endpoint for account config instance
    """
    def get(self, bank_id, account_config_id):
        """API Endpoint for getting account config instance
        """
        bank = Bank.query.get_or_404(bank_id)
        conf = AccountConfig.query.filter_by(bank=bank, id=account_config_id).first_or_404()
        return json_serialize(conf)

    def post(self, bank_id, account_config_id):
        """API Endpoint for updating account config instance
        """
        args = _account_config_update_parser.parse_args()
        bank = Bank.query.get_or_404(bank_id)
        conf = AccountConfig.query.filter_by(bank=bank, id=account_config_id).first_or_404()
        conf.update(args)
        conf.check_account_type_valid()
        db.session.commit()
        return json_serialize(conf)

    def delete(self, bank_id, account_config_id):
        """API Endpoint for deleting account config
        """
        bank = Bank.query.get_or_404(bank_id)
        conf = AccountConfig.query.filter_by(bank=bank, id=account_config_id).first_or_404()
        db.session.delete(conf)
        db.session.commit()
        return json_serialize(conf)


_account_parser = reqparse.RequestParser()
_account_parser.add_argument("user_id", type=int, required=True, help="No User Id provided", location="json")
_account_parser.add_argument("account_config_id", type=int, required=True, help="No Account Config Id Provided", location="json")
_account_parser.add_argument("initial_deposit", type=float, required=False, default=0, location="json")


class AccountListApi(Resource):
    """API Endpoint for bank's accounts
    """
    def get(self, bank_id):
        """API Endpoint for getting all accounts for a bank
        """
        bank = Bank.query.get_or_404(bank_id)
        accounts = Account.query.filter(Account.bank == bank).filter_by(_closed=False).all()
        return json_serialize(accounts)

    def put(self, bank_id):
        """API Endpoint for adding new account to a bank
        """
        args = _account_parser.parse_args()
        bank = Bank.query.get_or_404(bank_id)
        user = User.query.get_or_404(args['user_id'])
        account_config = AccountConfig.query.get_or_404(args['account_config_id'])
        # Verify initial deposit is not an issue
        if account_config.min_opening_balance and args['initial_deposit'] < account_config.min_opening_balance:
            abort(400, "You must deposit at least {} to open this account.".format(account_config.min_opening_balance))
        # Create account
        account = Account(bank=bank, config=account_config, user=user, _balance=0)
        # If initial deposit, make initial deposit
        if args['initial_deposit']:
            transaction = _gen_deposit_transaction(account, args['initial_deposit'], description="Initial Deposit")
            account.process_transaction(transaction)
        db.session.add(account)
        db.session.commit()
        return json_serialize(account)


class AccountApi(Resource):
    """API Endpoint for account instances
    """
    def get(self, bank_id, account_id):
        """API Endpoint for accessing account instance
        """
        account = Account.query.get_or_404(account_id)
        return json_serialize(account)

    def delete(self, bank_id, account_id):
        """API Endpoint for closing account instance
        """
        account = Account.query.get_or_404(account_id)
        account.close()
        db.session.commit()
        return json_serialize(account)


_transaction_parser = reqparse.RequestParser()
_transaction_parser.add_argument("cash_amount", type=float, required=False, default=0)
_transaction_parser.add_argument("checks", type=int, required=False, default=[], action='append')
_transaction_parser.add_argument("description", type=str, required=False, default="")


class TransactionListApi(Resource):
    """API Endpoint for accessing and adding account transactions
    """
    def get(self, bank_id, account_id):
        """API Endpoint for getting all account transactions
        """
        account = Account.query.get_or_404(account_id)
        return json_serialize(account.transactions)

    def put(self, bank_id, account_id):
        """API Endpoint for adding account transaction
        """
        args = _transaction_parser.parse_args()
        account = Account.query.get_or_404(account_id)
        cash_amount = args['cash_amount']
        raw_checks = args['checks']
        checks = [Check.query.get_or_404(check_id) for check_id in raw_checks]

        # Classify Transaction
        if cash_amount < 0 and not checks:
            # Withdrawal
            transaction = _gen_withdraw_transaction(account, cash_amount, args['description'])
        elif cash_amount >= 0:
            # Deposit
            transaction = _gen_deposit_transaction(account, cash_amount, checks=checks, description=args['description'])
        else:
            abort(400, "Invalid Transaction: Must either have negative cash amount and no checks, or positive cash amount and checks.")

        # Change balance
        account.process_transaction(transaction)
        db.session.commit()
        return json_serialize(transaction)


class TransactionApi(Resource):
    """API Endpoint for accessing individual transaction data
    """
    def get(self, bank_id, account_id, transaction_id):
        """API Endpoint for accessing transaction instance
        """
        return json_serialize(Transaction.query.get_or_404(transaction_id))


_check_parser = reqparse.RequestParser()
_check_parser.add_argument("payable_to", type=str, required=True, help="No Payable To information provided", location="json")
_check_parser.add_argument("amount", type=float, required=True, help="No amount provided", location="json")


class CheckListApi(Resource):
    """API Endpoint for managing account's checks
    """
    def get(self, bank_id, account_id):
        """API Endpoint for accessing account's checks
        """
        account = Account.query.get_or_404(account_id)
        return json_serialize(Check.query.filter(Check.issuing_account == account).filter_by(_void=False).all())

    def put(self, bank_id, account_id):
        """API Endpoint for issuing a check
        """
        args = _check_parser.parse_args()
        account = Account.query.get_or_404(account_id)
        check = Check(issuing_account=account, amount=args['amount'], payable_to=args['payable_to'])
        db.session.add(check)
        db.session.commit()
        return json_serialize(check)


class CheckApi(Resource):
    """API Endpoint for managing individual check instances
    """
    def get(self, bank_id, account_id, check_id):
        """API Endpoint for accessing check instance
        """
        return json_serialize(Check.query.get_or_404(check_id))

    def delete(self, bank_id, account_id, check_id):
        """API Endpoint for voicing issued check instance
        """
        check = Check.query.get_or_404(check_id)
        check.void()
        db.session.commit()
        return json_serialize(check)
