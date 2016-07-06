""" Function Identity model """

from peewee import ForeignKeyField, BigIntegerField, CharField

from .base import BaseModel
from .challenge_binary_node import ChallengeBinaryNode

class FunctionIdentity(BaseModel):
    """ Function Identity model """
    cbn = ForeignKeyField(db_column='cbn_id',
            rel_model=ChallengeBinaryNode,
            to_field='id',
            related_name='function_identities')

    address = BigIntegerField(null=False)
    function_name = CharField(null=False)

    class Meta:  # pylint: disable=no-init,too-few-public-methods,old-style-class
        db_table = 'function_identities'

# pylint: enable=missing-docstring
