"""Test model"""

from peewee import * #pylint:disable=wildcard-import,unused-wildcard-import
from .base import BaseModel
from .challenge_binary_node import ChallengeBinaryNode
from .job import Job
from farnsworth.actions import CQE_POV, Data, Write


class Test(BaseModel):
    """Test model"""
    blob = BlobField()
    cbn = ForeignKeyField(ChallengeBinaryNode, db_column='cbn_id', related_name='tests')
    job = ForeignKeyField(Job, db_column='job_id', to_field='id', related_name='tests')
    drilled = BooleanField(null=False, default=False)
    colorguard_traced = BooleanField(null=False, default=False)
    poll_created = BooleanField(null=False, default=False)

    @classmethod
    def unsynced_testcases(cls, prev_sync_time):
        """Return test cases not synced"""
        return cls.select().where(cls.created_at > prev_sync_time)

    def to_cqe_pov_xml(self):
        """
            Method to convert job into to cqe xml format
            :return Xml Containing test data in CQE POV format
        """
        pov_header = """<?xml version="1.0" standalone="no" ?>
                        <!DOCTYPE pov SYSTEM "/usr/share/cgc-docs/replay.dtd">
                    """
        pov = CQE_POV(str(self.cbn.id), []) # pylint:disable=no-member
        # the Write
        pov.actions.append(Write([Data(self.blob)]))

        return pov_header + str(pov)
