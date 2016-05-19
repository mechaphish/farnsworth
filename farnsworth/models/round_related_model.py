"""Base class for models associated to Round"""

from datetime import datetime

class RoundRelatedModel(object):
    """Base class for models associated to Round"""
    @classmethod
    def update_or_create(cls, round_, **kwargs):
        """Update or create record"""
        update = cls.update(updated_at=datetime.now(), # pylint:disable=no-member
                            **kwargs).where(cls.round == round_) # pylint:disable=no-member
        if update.execute() == 0:
            cls.create(round=round_, **kwargs) # pylint:disable=no-member
