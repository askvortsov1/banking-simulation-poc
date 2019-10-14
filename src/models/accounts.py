from datetime import datetime

from app import db


class AccountConfig(db.Model):
    """Database model representing account configuration entry.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    is_savings = db.Column(db.Boolean, nullable=False)
    is_checking = db.Column(db.Boolean, nullable=False)

    min_opening_balance = db.Column(db.Float, nullable=False)
    interest = db.Column(db.Float, nullable=False)

    deposit_fee = db.Column(db.Float, nullable=False)
    withdrawal_fee = db.Column(db.Float, nullable=False)

    allow_overdraft = db.Column(db.Boolean, nullable=False)
    overdraft_limit = db.Column(db.Float, nullable=False)
    overdraft_fee = db.Column(db.Float, nullable=False)

    bank_id = db.Column(db.Integer, db.ForeignKey('bank.id'), nullable=False)

    accounts = db.relationship('Account', backref='config', lazy=True)

    JSON_ATTRIBUTES = ("name", "account_type", "min_opening_balance", "interest", "deposit_fee", "withdrawal_fee", "allow_overdraft", "overdraft_limit", "overdraft_fee")

    @property
    def account_type(self):
        """Returns verbose account type

        Returns:
            str -- Verbose account type
        """
        return "checking" if self.is_checking else "savings"

    def check_account_type_valid(self):
        """Validates that account isn't savings and checkings at the same time.
        """
        if self.is_checking and self.is_savings or self.is_checking == self.is_savings:
            raise ValueError("Account can't be both savings and checkings.")

    def __repr__(self):
        """String representation of account config

        Returns:
            str -- verbose representation of account config instance
        """
        return self.name


class Account(db.Model):
    """Database model representing account.
    """
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    bank_id = db.Column(db.Integer, db.ForeignKey('bank.id'), nullable=False)

    config_id = db.Column(db.Integer, db.ForeignKey('account_config.id'), nullable=False)

    checks_issued = db.relationship('Check', backref='issuing_account', lazy=True)

    transactions = db.relationship('Transaction', backref='account', lazy=True)

    _balance = db.Column(db.Float, nullable=False, default=0)

    _closed = db.Column(db.Boolean, nullable=False, default=False)

    JSON_ATTRIBUTES = ("user", "bank", "config", "balance")

    @property
    def balance(self):
        """Encapsulates balance

        Returns:
            float -- Account instance balance
        """
        return self._balance

    @property
    def closed(self):
        """Encapsulates closed

        Returns:
            bool -- Whether the account instance is closed.
        """
        return self._closed

    @property
    def withdrawals_last_month(self):
        """Calculates withdrawals during last calendar month

        Returns:
            int -- number of withdrawals during last calendar month
        """
        count = 0
        i = len(self.transactions) - 1
        while i >= 0 and (datetime.now() - self.transactions[i].datetime).days / 31 < 1:
            i -= 1
            if self.transactions[i].total_amount < 0:
                # Withdrawal, so increment counter
                count += 1
        return count

    def audit(self):
        """Audits account to ensure that balance attribute matches transaction log

        Raises:
            Exception: Balance doesn't match up with transaction
        """
        try:
            assert self._balance == sum([transaction.total_amount for transaction in self.transactions if not transaction.undone])
        except AssertionError:
            raise Exception("Balance doesn't match up with transactions")

    def close(self):
        """Encapsulates closing account
        """
        self._closed = True

    def process_transaction(self, transaction):
        """Applies transaction to balance

        Arguments:
            transaction {Transaction} -- Transaction to apply to account balance
        """
        self._balance += transaction.total_amount

    def __repr__(self):
        """String representation of account

        Returns:
            str -- String representation of account
        """
        return "{} #{}".format(self.config, self.id)
