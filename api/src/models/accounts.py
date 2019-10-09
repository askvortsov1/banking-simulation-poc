from datetime import datetime

from app import db


class AccountConfig(db.Model):
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

    def check_account_type_valid(self):
        if self.is_checking and self.is_savings:
            raise ValueError("Account can't be both savings and checkings.")

    def __repr__(self):
        return self.name


class Account(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    bank_id = db.Column(db.Integer, db.ForeignKey('bank.id'), nullable=False)
    config_id = db.Column(db.Integer, db.ForeignKey('account_config.id'), nullable=False)

    checks_issued = db.relationship('Check', backref='issuing_account', lazy=True)

    transactions = db.relationship('Transaction', backref='account', lazy=True)

    _balance = db.Column(db.Float, nullable=False, default=0)

    _closed = db.Column(db.Boolean, nullable=False, default=False)

    @property
    def balance(self):
        return self._balance

    @property
    def closed(self):
        return self._closed

    @property
    def withdrawals_last_month(self):
        count = 0
        i = len(self.transactions) - 1
        while i >= 0 and (datetime.now() - self.transactions[i].datetime).months < 1:
            i -= 1
            if self.transactions[i].amount < 0:
                # Withdrawal, so increment counter
                count += 1
        return count

    def audit(self):
        try:
            assert self._balance == sum([transaction.total_amount for transaction in self.transactions if not transaction.undone])
        except AssertionError:
            raise Exception("Balance doesn't match up with transactions")

    def close(self):
        self.closed = True

    def process_transaction(self, transaction):
        self._balance += transaction.total_amount

    def __repr__(self):
        return "{} #{}".format(self.config, self.id)
