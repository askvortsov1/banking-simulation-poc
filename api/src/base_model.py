import sqlalchemy as sa
from flask_sqlalchemy import Model
from sqlalchemy.ext.declarative import declared_attr


class IdModel(Model):
    """Abstract model that serves as base for all models used.
    """
    @declared_attr
    def id(cls):
        """Provides id column for all inheriting models.
        """
        return sa.Column(sa.Integer, primary_key=True)

    def __str__(self):
        """Sets str to always return repr.
        """
        return self.__repr__()

    def json(self):
        """JSON-encodes object
        """
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}
