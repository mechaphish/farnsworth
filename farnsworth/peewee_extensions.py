"""Extend Peewee basic types."""

from peewee import Field

class EnumField(Field):
    """Define a EnumField type"""
    db_field = "enum"

    def coerce(self, value):
        if value not in self.choices:
            raise Exception("Invalid Enum Value `%s`", value)
        return str(value)

    def get_column_type(self):
        return "enum"
