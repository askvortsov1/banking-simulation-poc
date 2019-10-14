from datetime import datetime
from flask import abort

from app import db


class Check(db.Model):
    """Database model representing check
    """
    issuing_account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    payable_to = db.Column(db.String(256), nullable=False)
    amount = db.Column(db.Float, nullable=False)

    transaction_id = db.Column(db.Integer, db.ForeignKey('transaction.id'), nullable=True)

    _deposited = db.Column(db.Boolean, nullable=False, default=False)
    _void = db.Column(db.Boolean, nullable=False, default=False)

    JSON_ATTRIBUTES = ("issuing_account", "payable_to", "amount", "is_void", "is_deposited")

    @property
    def is_deposited(self):
        """Encapsulation of whether check is deposited.
        """
        return self._deposited

    @property
    def is_void(self):
        """Encapsulation of whether check is void
        """
        return self._void

    def validate(self, depositing_account):
        """Validates check with respect to depositing account

        Makes sure this check is written out to the depositing account

        Arguments:
            depositing_account {Account} -- Account trying to deposit the check

        Returns:
            bool -- Whether check is depositable to the depositing account
        """
        valid_depositing_account = self.payable_to == depositing_account or self.payable_to == depositing_account.user.full_name
        return not self.is_deposited and not self.is_void and valid_depositing_account

    def deposit(self):
        """Mark check as account
        """
        if self._deposited or self._void:
            abort(403, "Can't deposit deposited or voided check")
        self._void = True

    def void(self):
        """Mark check as void
        """
        if self._deposited:
            abort(403, "Can't void deposited check")
        self._void = True

    def __repr__(self):
        """Verbose representation of check instance

        Returns:
            str -- Verbose representation of check instance
        """
        return "{} Check Payable To {}".format(self.amount, self.payable_to)


class Transaction(db.Model):
    """Database model representing transaction.
    """
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
        """Computes total amount of transaction
        """
        return self.cash_amount + self._check_amount - self.fees

    def __init__(self, *args, **kwargs):
        """Caches sum of check amounts, then initialized database record as usual.
        """
        super().__init__(*args, **kwargs)
        # Store check amount to avoid repetetive future lookups
        self._check_amount = sum([check.amount for check in self.checks])

    def __repr__(self):
        """Verbose representation of transaction instance

        Returns:
            str -- Verbose representation of transaction instance
        """
        return "{} Transaction: {}".format(self.datetime, self.total_amount)
