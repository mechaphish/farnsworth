from datetime import datetime

class RoundRelatedModel(object):
    @classmethod
    def update_or_create(cls, round_, **kwargs):
        update = cls.update(updated_at=datetime.now(),
                            **kwargs).where(cls.round == round_)
        if update.execute() == 0:
            cls.create(round=round_, **kwargs)
