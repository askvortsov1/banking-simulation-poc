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

    def update(self, new_attrs):
        """Takes in dict of attributes, and updates self, making sure not to override methods, and that is not adding a null value
        """
        for k, v in new_attrs.items():
            if hasattr(self, k) and not callable(getattr(self, k)) and v is not None:
                setattr(self, k, v)

    def json(self):
        """JSON-encodes object by going through whitelist of returned attributes (and id), then returning the string value of all attributes (called if callable). If an attribute is a property, calls its __get__ magic method to obtain value.
        """
        json_dict = {}
        for attr in ["id"] + list(self.JSON_ATTRIBUTES):
            raw_val = getattr(self, attr) or self.__class__.__dict__.get(attr, None)
            if raw_val is None:
                continue
            val = raw_val() if callable(raw_val) else raw_val
            if isinstance(val, property):
                val = val.fget(self)
            json_dict[attr] = str(val)
        return json_dict
