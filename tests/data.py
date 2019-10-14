account_config_1 = {
    "name": "Basic Checking",
    "is_checking": True,
    "is_savings": False,
    "min_opening_balance": 0,
    "interest": 0,
    "deposit_fee": 0,
    "withdrawal_fee": 0,
    "allow_overdraft": True,
    "overdraft_fee": 35,
    "overdraft_limit": 500
}

account_config_2 = {
    "name": "Premium Checking",
    "is_checking": True,
    "is_savings": False,
    "min_opening_balance": 500,
    "interest": 0.05,
    "deposit_fee": 5,
    "withdrawal_fee": 5,
    "allow_overdraft": True,
    "overdraft_fee": 50,
    "overdraft_limit": 750
}

account_config_3 = {
    "name": "Basic Savings",
    "is_checking": False,
    "is_savings": True,
    "min_opening_balance": 750,
    "interest": 0.1,
    "deposit_fee": 10,
    "withdrawal_fee": 10,
    "allow_overdraft": False,
    "overdraft_fee": 0,
    "overdraft_limit": 0
}

account_config_4 = {
    "name": "Premium Savings",
    "is_checking": False,
    "is_savings": True,
    "min_opening_balance": 750,
    "interest": 0.2,
    "deposit_fee": 10,
    "withdrawal_fee": 10,
    "allow_overdraft": False,
    "overdraft_fee": 0,
    "overdraft_limit": 0
}

account_config_5 = {
    "name": "Basic Savings Copy",
    "is_checking": False,
    "is_savings": True,
    "min_opening_balance": 750,
    "interest": 0.1,
    "deposit_fee": 10,
    "withdrawal_fee": 10,
    "allow_overdraft": False,
    "overdraft_fee": 0,
    "overdraft_limit": 0
}

user_1 = {"fname": "John", "lname": "Doe", "credit_score": 800}
user_2 = {"fname": "Jane", "lname": "Roe", "credit_score": 800}
user_3 = {"fname": "Eric", "lname": "Erickson"}
user_4 = {"fname": "Mark", "lname": "Smith"}
user_5 = {"fname": "Natalie", "lname": "Zhao"}
user_6 = {"fname": "Terry", "lname": "Garlinger"}

bank_1 = {"name": "Grand Federal Bank"}
bank_2 = {"name": "Royal Bank of Mesopotamia"}
bank_3 = {"name": "Bitcoin Banking"}

branch_1_1 = {"name": "GFB State College"}
branch_1_2 = {"name": "GFB Philadelphia"}
branch_1_3 = {"name": "GFB Harrisburg"}

staff_1_1_1 = {"user_id": 1, "role": 4}  # Teller
staff_1_1_2 = {"user_id": 2, "role": 8}  # Assistant Manager
staff_1_1_3 = {"user_id": 3, "role": 12}  # Manager
staff_1_1_4 = {"user_id": 4, "role": 12}  # Manager
staff_1_1_5 = {"user_id": 5, "role": 12}  # Manager

account_1 = {"user_id": 4, "account_config_id": 1, "initial_deposit": 500}
account_2 = {"user_id": 5, "account_config_id": 2, "initial_deposit": 750}
account_3 = {"user_id": 3, "account_config_id": 3, "initial_deposit": 1000}
account_4 = {"user_id": 3, "account_config_id": 3, "initial_deposit": 1000}
account_5_balance_too_low = {"user_id": 5, "account_config_id": 3}
