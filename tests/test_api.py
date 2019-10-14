import requests
from . import data


URL_BASE = "http://localhost:5000/api/v1/"


def test_api():
    """Test case that covers operation of the entire API.
    """

    """BANK TESTS"""
    BANK_LIST_URL = URL_BASE + "bank/"

    assert requests.get(BANK_LIST_URL).json() == []  # Start with no banks

    # Check adding banks
    requests.put(BANK_LIST_URL, json=data.bank_1)
    assert len(requests.get(BANK_LIST_URL).json()) == 1
    for bank in [data.bank_2, data.bank_3]:
        requests.put(BANK_LIST_URL, json=bank)
    assert len(requests.get(BANK_LIST_URL).json()) == 3

    # Test deleting bank
    requests.delete(BANK_LIST_URL + "3/")
    assert len(requests.get(BANK_LIST_URL).json()) == 2

    # Test changing bank name and getting bank instance
    requests.post(BANK_LIST_URL + "2/", json={"name": "New Bank Corp"})
    assert requests.get(BANK_LIST_URL + "2/").json()['name'] == "New Bank Corp"

    """BRANCH TESTS"""
    BRANCH_LIST_URL_1 = BANK_LIST_URL + "1/" + "branch/"

    # Check adding branches
    requests.put(BRANCH_LIST_URL_1, json=data.branch_1_1)
    assert len(requests.get(BRANCH_LIST_URL_1).json()) == 1

    for branch in [data.branch_1_2, data.branch_1_3]:
        requests.put(BRANCH_LIST_URL_1, json=branch)
    assert len(requests.get(BRANCH_LIST_URL_1).json()) == 3

    # Test deleting branch
    requests.delete(BRANCH_LIST_URL_1 + "3/")
    assert len(requests.get(BRANCH_LIST_URL_1).json()) == 2

    # Test changing branch name and getting branch instance
    requests.post(BRANCH_LIST_URL_1 + "2/", json={"name": "London"})
    assert requests.get(BRANCH_LIST_URL_1 + "2/").json()['name'] == "London"

    """USER TESTS"""
    USER_LIST_URL = URL_BASE + "user/"

    # Check adding user
    requests.put(USER_LIST_URL, json=data.user_1)
    assert len(requests.get(USER_LIST_URL).json()) == 1
    for user in [data.user_2, data.user_3, data.user_4, data.user_5, data.user_6]:
        requests.put(USER_LIST_URL, json=user)
    assert len(requests.get(USER_LIST_URL).json()) == 6

    # Test deleting user
    requests.delete(USER_LIST_URL + "6/")
    assert len(requests.get(USER_LIST_URL).json()) == 5

    # Test changing user name and getting user instance
    requests.post(USER_LIST_URL + "2/", json={"fname": "Jessica"})
    assert requests.get(USER_LIST_URL + "2/").json()['full_name'] == "Jessica Roe"

    """STAFF TESTS"""
    STAFF_LIST_URL_1 = BRANCH_LIST_URL_1 + "1/" + "staff/"

    # Check adding staff
    requests.put(STAFF_LIST_URL_1, json=data.staff_1_1_1)
    assert len(requests.get(STAFF_LIST_URL_1).json()) == 1
    for staff in [data.staff_1_1_2, data.staff_1_1_3, data.staff_1_1_4, data.staff_1_1_5]:
        requests.put(STAFF_LIST_URL_1, json=staff)
    assert len(requests.get(STAFF_LIST_URL_1).json()) == 5

    # Test deleting staff
    requests.delete(STAFF_LIST_URL_1 + "5/")
    assert len(requests.get(STAFF_LIST_URL_1).json()) == 4

    # Test changing staff role and getting staff instance
    requests.post(STAFF_LIST_URL_1 + "4/", json={"role": 4})
    assert requests.get(STAFF_LIST_URL_1 + "4/").json()['role_display'] == "Teller"

    """ACCOUNT CONFIG TESTS"""
    CONFIG_LIST_URL_1 = BANK_LIST_URL + "1/" + "account_config/"
    CONFIG_LIST_URL_2 = BANK_LIST_URL + "2/" + "account_config/"

    # Check adding configs
    requests.put(CONFIG_LIST_URL_1, json=data.account_config_1)
    assert len(requests.get(CONFIG_LIST_URL_1).json()) == 1
    for conf in [data.account_config_2, data.account_config_3, data.account_config_4, data.account_config_5]:
        requests.put(CONFIG_LIST_URL_1, json=conf)
    assert len(requests.get(CONFIG_LIST_URL_1).json()) == 5
    requests.put(CONFIG_LIST_URL_2, json=data.account_config_1)
    assert len(requests.get(CONFIG_LIST_URL_1).json()) == 5

    # Test deleting configs
    requests.delete(CONFIG_LIST_URL_1 + "5/")
    assert len(requests.get(CONFIG_LIST_URL_1).json()) == 4

    # Test changing configs role and getting configs instance
    requests.post(CONFIG_LIST_URL_1 + "4/", json={"deposit_fee": 0,
                                                  "withdrawal_fee": 100,
                                                  "allow_overdraft": True,
                                                  "overdraft_fee": 5,
                                                  "overdraft_limit": 500})
    assert requests.get(CONFIG_LIST_URL_1 + "4/").json()['overdraft_limit'] == "500.0"

    """ACCOUNT TESTS"""
    ACCOUNT_LIST_URL_1 = BANK_LIST_URL + "1/" + "account/"
    ACCOUNT_LIST_URL_2 = BANK_LIST_URL + "2/" + "account/"

    # Check adding accounts
    assert requests.put(ACCOUNT_LIST_URL_1, json=data.account_1).status_code == 200
    assert len(requests.get(ACCOUNT_LIST_URL_1).json()) == 1
    for account in [data.account_2, data.account_3, data.account_4]:
        assert requests.put(ACCOUNT_LIST_URL_1, json=account).status_code == 200
    assert len(requests.get(ACCOUNT_LIST_URL_1).json()) == 4
    assert requests.put(ACCOUNT_LIST_URL_2, json=data.account_2).status_code == 200
    assert len(requests.get(ACCOUNT_LIST_URL_1).json()) == 4

    # Assert can't add account if initial deposit is less than minimum balance
    assert requests.put(ACCOUNT_LIST_URL_1, json=data.account_5_balance_too_low).status_code == 400

    # Test deleting accounts
    assert requests.delete(ACCOUNT_LIST_URL_1 + "4/").status_code == 200
    assert len(requests.get(ACCOUNT_LIST_URL_1).json()) == 3

    # Test getting accounts instance
    assert requests.get(ACCOUNT_LIST_URL_1 + "1/").json()['user'] == "Mark Smith"
    assert requests.get(ACCOUNT_LIST_URL_1 + "1/").json()['balance'] == "500.0"
    assert requests.get(ACCOUNT_LIST_URL_1 + "2/").json()['user'] == "Natalie Zhao"
    assert requests.get(ACCOUNT_LIST_URL_1 + "2/").json()['balance'] == "745.0"
    assert requests.get(ACCOUNT_LIST_URL_1 + "3/").json()['user'] == "Eric Erickson"
    assert requests.get(ACCOUNT_LIST_URL_1 + "3/").json()['balance'] == "990.0"
    assert requests.get(ACCOUNT_LIST_URL_2 + "5/").json()['user'] == "Natalie Zhao"
    assert requests.get(ACCOUNT_LIST_URL_2 + "5/").json()['balance'] == "745.0"

    """CHECK TESTS"""
    CHECK_LIST_URL_1 = ACCOUNT_LIST_URL_1 + "1/check/"
    CHECK_LIST_URL_2 = ACCOUNT_LIST_URL_1 + "2/check/"

    account_1_good_check_1 = {"payable_to": "Natalie Zhao", "amount": 10}
    account_1_good_check_2 = {"payable_to": "Natalie Zhao", "amount": 15}
    account_1_good_check_3 = {"payable_to": "Natalie Zhao", "amount": 10}
    account_1_bad_check = {"payable_to": "Natalie Zhao", "amount": 10000}

    account_2_good_check = {"payable_to": "Mark Smith", "amount": 20}

    # Test adding checks
    assert requests.put(CHECK_LIST_URL_1, json=account_1_good_check_1).status_code == 200
    assert len(requests.get(CHECK_LIST_URL_1).json()) == 1
    for check in [account_1_good_check_2, account_1_good_check_3, account_1_bad_check]:
        assert requests.put(CHECK_LIST_URL_1, json=check).status_code == 200
    assert len(requests.get(CHECK_LIST_URL_1).json()) == 4
    # Test adding check to different account doesn't have effect
    assert requests.put(CHECK_LIST_URL_2, json=account_2_good_check).status_code == 200
    assert len(requests.get(CHECK_LIST_URL_1).json()) == 4

    # Test deleting checks
    assert requests.delete(CHECK_LIST_URL_1 + "3/").status_code == 200
    assert len(requests.get(CHECK_LIST_URL_1).json()) == 3

    # Test getting checks instance
    assert requests.get(CHECK_LIST_URL_1 + "1/").json()['payable_to'] == "Natalie Zhao"
    assert requests.get(CHECK_LIST_URL_1 + "2/").json()['payable_to'] == "Natalie Zhao"
    assert requests.get(CHECK_LIST_URL_1 + "4/").json()['payable_to'] == "Natalie Zhao"
    assert requests.get(CHECK_LIST_URL_1 + "5/").json()['payable_to'] == "Mark Smith"

    """TRANSACTIONS TEST"""
    TRANSACTION_LIST_URL_1 = ACCOUNT_LIST_URL_1 + "1/transaction/"
    TRANSACTION_LIST_URL_2 = ACCOUNT_LIST_URL_1 + "2/transaction/"
    TRANSACTION_LIST_URL_3 = ACCOUNT_LIST_URL_1 + "3/transaction/"

    account_1_cash_deposit_1 = {"cash_amount": 100}
    account_2_cash_deposit_1 = {"cash_amount": 100}

    account_1_cash_withdrawal_1 = {"cash_amount": -100}
    account_1_cash_withdrawal_2 = {"cash_amount": -900}
    account_1_cash_withdrawal_3 = {"cash_amount": -9000}
    account_2_cash_withdrawal_1 = {"cash_amount": -100}
    account_3_cash_withdrawal_1 = {"cash_amount": -1000}

    account_1_check_deposit_1 = {"cash_amount": 150, "checks": [5]}
    account_2_check_deposit_1 = {"cash_amount": 150, "checks": [1]}

    # Test cash_deposit
    assert requests.put(TRANSACTION_LIST_URL_1, json=account_1_cash_deposit_1).status_code == 200
    assert requests.get(ACCOUNT_LIST_URL_1 + "1/").json()['balance'] == "600.0"

    assert requests.put(TRANSACTION_LIST_URL_2, json=account_2_cash_deposit_1).status_code == 200
    assert requests.get(ACCOUNT_LIST_URL_1 + "2/").json()['balance'] == "840.0"

    # Test Check Depoit
    assert requests.put(TRANSACTION_LIST_URL_1, json=account_1_check_deposit_1).status_code == 200
    assert requests.get(ACCOUNT_LIST_URL_1 + "1/").json()['balance'] == "770.0"
    assert requests.get(ACCOUNT_LIST_URL_1 + "2/").json()['balance'] == "815.0"  # Subtract 20$ check and 5$ withdrawal fee for check

    assert requests.put(TRANSACTION_LIST_URL_2, json=account_2_check_deposit_1).status_code == 200
    assert requests.get(ACCOUNT_LIST_URL_1 + "1/").json()['balance'] == "760.0"  # Subtract 10$ check. Account 1 has no fees
    assert requests.get(ACCOUNT_LIST_URL_1 + "2/").json()['balance'] == "970.0"

    # Check deposit with invalid check
    assert requests.put(TRANSACTION_LIST_URL_2, json=account_2_check_deposit_1).status_code == 400
    assert requests.get(ACCOUNT_LIST_URL_1 + "1/").json()['balance'] == "760.0"  # Subtract 10$ check. Account 1 has no fees
    assert requests.get(ACCOUNT_LIST_URL_1 + "2/").json()['balance'] == "970.0"

    # Test cash withdrawal
    assert requests.put(TRANSACTION_LIST_URL_1, json=account_1_cash_withdrawal_1).status_code == 200
    assert requests.get(ACCOUNT_LIST_URL_1 + "1/").json()['balance'] == "660.0"
    # Test overdraft fee applied
    assert requests.put(TRANSACTION_LIST_URL_1, json=account_1_cash_withdrawal_2).status_code == 200
    assert requests.get(ACCOUNT_LIST_URL_1 + "1/").json()['balance'] == "-275.0"
    # Test going over overdraft limit
    assert requests.put(TRANSACTION_LIST_URL_1, json=account_1_cash_withdrawal_3).status_code == 403
    assert requests.get(ACCOUNT_LIST_URL_1 + "1/").json()['balance'] == "-275.0"

    # Test working withdrawal
    assert requests.put(TRANSACTION_LIST_URL_2, json=account_2_cash_withdrawal_1).status_code == 200
    assert requests.get(ACCOUNT_LIST_URL_1 + "2/").json()['balance'] == "865.0"

    # Test overdraft attempt on account without overdraft
    assert requests.put(TRANSACTION_LIST_URL_3, json=account_3_cash_withdrawal_1).status_code == 403
    assert requests.get(ACCOUNT_LIST_URL_1 + "3/").json()['balance'] == "990.0"

    # Test withdraw from savings account more than 6 times
    account_3_valid_withdraw_transaction = {"cash_amount": -1}
    for i in range(6):
        assert requests.put(TRANSACTION_LIST_URL_3, json=account_3_valid_withdraw_transaction).status_code == 200
    assert requests.get(ACCOUNT_LIST_URL_1 + "3/").json()['balance'] == "924.0"  # Decreases by 11 per transaction: 1 for withdrawal and 10 for fee
    assert requests.put(TRANSACTION_LIST_URL_3, json=account_3_valid_withdraw_transaction).status_code == 403
