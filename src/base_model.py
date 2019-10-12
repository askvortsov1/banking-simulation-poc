import sqlalchemy as sa
from flask_sqlalchemy import Model
from sqlalchemy.ext.declarative import declared_attr


class IdModel(Model):
    """Abstract model that serves as base for all models used.
    """
    JSON_ATTRIBUTES = ()

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
        json_dict = {}
        for attr in ["id"] + list(self.JSON_ATTRIBUTES):
            raw_val = getattr(self, attr)
            if raw_val is None:
                continue
            val = raw_val() if callable(raw_val) else raw_val
            json_dict[attr] = val
        return json_dict
            
