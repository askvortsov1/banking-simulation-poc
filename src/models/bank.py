import config
from app import db


class Bank(db.Model):
    """The Bank model represents banks in the database.

    Arguments:
        name {str} -- [description]
    """
    name = db.Column(db.String(128), nullable=False, unique=True)

    # Many-To-One Definitions
    branches = db.relationship('BankBranch', backref="bank", lazy=True)
    account_configs = db.relationship('AccountConfig', backref='bank', lazy=True)
    accounts = db.relationship('Account', backref='bank', lazy=True)

    JSON_ATTRIBUTES = ("name",)

    def __repr__(self):
        return self.name


class BankBranch(db.Model):
    name = db.Column(db.String(128), nullable=False)
    bank_id = db.Column(db.Integer, db.ForeignKey('bank.id'), nullable=False)

    staff = db.relationship('Staff', backref='branch', lazy=True)

    JSON_ATTRIBUTES = ("name", "bank")

    def __repr__(self):
        return "{} - {} Branch".format(self.bank, self.name)


class Staff(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    branch_id = db.Column(db.Integer, db.ForeignKey('bank_branch.id'), nullable=False)

    role = db.Column(db.Integer, nullable=False)

    JSON_ATTRIBUTES = ("user", "branch", "role_display")

    @property
    def role_display(self):
        role_mapping = {
            config.MANAGER: "Manager",
            config.ASSISTANT_MANAGER: "Assistant Manager",
            config.TELLER: "Teller",
        }
        return role_mapping[self.role]

    def __repr__(self):
        return "{}: {} {}".format(self.branch.bank, self.role_display, self.user)
