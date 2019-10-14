import config
from app import db

from .bank import Bank, Staff


class User(db.Model):
    """Database representation of user
    """
    fname = db.Column(db.String(128), nullable=False)
    lname = db.Column(db.String(128), nullable=False)
    credit_score = db.Column(db.String(9), nullable=False, default=config.USA_AVERAGE_FICO_CREDIT_SCORE)
    staff = db.relationship('Staff', backref='user', lazy=True, uselist=False)

    accounts = db.relationship('Account', backref='user', lazy=True)

    _is_superuser = db.Column(db.Boolean, nullable=False, default=False)

    JSON_ATTRIBUTES = ("fname", "lname", "full_name", "credit_score",)

    @property
    def full_name(self):
        """Gets user full name

        Returns:
            str -- User full name
        """
        return "{} {}".format(self.fname, self.lname)

    def get_permission_level(self, bank=None):
        """Gets permission level at a given bank. Returns admin if global admin, and customer if no staff positions for bank found

        Keyword Arguments:
            bank {Bank} -- Bank instance for which to get permissions (default: {None})

        Raises:
            TypeError: If provided, Bank must be an instance of Bank

        Returns:
            int -- Ordinal permission level
        """
        if bank is None:
            return config.ADMIN if self._is_superuser else config.CUSTOMER
        elif isinstance(bank, Bank):
            staff = Staff.query.filter(Staff.user == self and Staff.bank == bank)
            return staff.role
        else:
            raise TypeError("Bank must be instance of Bank or None.")

    def __repr__(self):
        """Verbose representation of user instance

        Returns:
            str -- Verbose representation of user instance
        """
        return self.full_name
