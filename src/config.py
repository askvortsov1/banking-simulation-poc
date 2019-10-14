import os

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), os.environ.get("FLASK_DB_FILE", 'app.db'))
SQLALCHEMY_TRACK_MODIFICATIONS = False

# =====Banking Settings======

# Ordinal permission levels, initialized with distance between them to allow future modification
ADMIN = 15
MANAGER = 12
ASSISTANT_MANAGER = 8
TELLER = 4
CUSTOMER = 0

# U.S. Bank Secrecy Act requires that deposits and transfers over $10,000 USD be reported.
MIN_LARGE_TRANSFER = 10000

USA_AVERAGE_FICO_CREDIT_SCORE = 695

# As per Regulation D, customers cannot withdraw from a savings account more than 6 times per calendar month
SAVINGS_ACCOUNT_MAX_WITHDRAWALS_PER_MONTH = 6

# Taken from https://www.myfico.com/credit-education/calculators/loan-savings-calculator/ on 9/30/2019. Generalized from mortgages to all loans
CREDIT_SCORE_INTEREST_RATE_MAPPING = {
    760: .03369,
    700: .03591,
    680: .03768,
    660: .03982,
    640: .04412,
    620: .04958,
    0: None
}

# API Settings
BASE_PATH = "/api/v1"
