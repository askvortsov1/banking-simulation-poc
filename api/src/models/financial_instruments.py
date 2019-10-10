from datetime import datetime
from werkzeug.exceptions import Forbidden

from app import db


class Check(db.Model):
    issuing_account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    payable_to = db.Column(db.String(256), nullable=False)
    amount = db.Column(db.Float, nullable=False)

    transaction_id = db.Column(db.Integer, db.ForeignKey('transaction.id'), nullable=True)

    _deposited = db.Column(db.Boolean, nullable=False, default=False)
    _void = db.Column(db.Boolean, nullable=False, default=True)

    JSON_ATTRIBUTES = ("issuing_account", "payable_to", "amount", "is_void", "is_deposited")

    @property
    def is_deposited(self):
        return self._deposited

    @property
    def is_void(self):
        return self._void

    def validate(self, depositing_account):
        valid_depositing_account = self.payable_to == depositing_account or any(
            [self._payable_to == signer.full_name for signer in depositing_account.signers])
        return not self._deposited and not self._void and valid_depositing_account

    def void(self):
        if self._deposited:
            raise Forbidden("Can't void deposited check")
        self._void = True

    def __repr__(self):
        return "{} Check Payable To {}".format(self.amount, self.payable_to)


class Transaction(db.Model):
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=True)

    cash_amount = db.Column(db.Float, nullable=False)
    checks = db.relationship('Check', backref='transaction', lazy=True)
    fees = db.Column(db.Float, nullable=False, default=0)

    description = db.Column(db.String(2000), nullable=False, default="")

    _check_amount = db.Column(db.Float, nullable=False, default=0)

    datetime = db.Column(db.DateTime, nullable=False, default=datetime.now)

    JSON_ATTRIBUTES = ("account", "total_amount", "datetime", "description")

    @property
    def total_amount(self):
        return self.amount + self._check_amount - self.fees

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Store check amount to avoid repetetive future lookups
        self._check_amount = sum([check.amount for check in self.checks])

    def __repr__(self):
        return "{} Transaction: {}".format(self.datetime, self.total_amount)
