import config
from app import db


class Bank(db.Model):
    """Database model representing bank
    """
    name = db.Column(db.String(128), nullable=False, unique=True)

    # Many-To-One Definitions
    branches = db.relationship('BankBranch', backref="bank", lazy=True)
    account_configs = db.relationship('AccountConfig', backref='bank', lazy=True)
    accounts = db.relationship('Account', backref='bank', lazy=True)

    JSON_ATTRIBUTES = ("name",)

    def __repr__(self):
        """Verbose representation of bank instance

        Returns:
            str -- Verbose representation of bank instance
        """
        return self.name


class BankBranch(db.Model):
    """Database model representing bank branch
    """
    name = db.Column(db.String(128), nullable=False)
    bank_id = db.Column(db.Integer, db.ForeignKey('bank.id'), nullable=False)

    staff = db.relationship('Staff', backref='branch', lazy=True)

    JSON_ATTRIBUTES = ("name", "bank")

    def __repr__(self):
        """Verbose representation of bank branch instance

        Returns:
            str -- Verbose representation of bank branch instance
        """
        return "{} - {} Branch".format(self.bank, self.name)


class Staff(db.Model):
    """Database representation of bank staff
    """
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    branch_id = db.Column(db.Integer, db.ForeignKey('bank_branch.id'), nullable=False)

    role = db.Column(db.Integer, nullable=False)

    JSON_ATTRIBUTES = ("user", "branch", "role_display")

    @property
    def role_display(self):
        """Converts ordinal role into verbose representation
        """
        role_mapping = {
            config.MANAGER: "Manager",
            config.ASSISTANT_MANAGER: "Assistant Manager",
            config.TELLER: "Teller",
        }
        return role_mapping[self.role]

    def __repr__(self):
        """Verbose representation of staff instance

        Returns:
            str -- Verbose representation of staff instance
        """
        return "{}: {} {}".format(self.branch.bank, self.role_display, self.user)
