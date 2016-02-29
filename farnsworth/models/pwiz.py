from peewee import *

database = PostgresqlDatabase('farnsworth', **{'user': 'postgres'})

class UnknownField(object):
    pass


class Teams(BaseModel):
    created_at = DateTimeField()
    id = BigIntegerField(primary_key=True)
    name = CharField()
    updated_at = DateTimeField()

    class Meta:
        db_table = 'teams'

class Rounds(BaseModel):
    created_at = DateTimeField()
    ends_at = DateTimeField(null=True)
    id = BigIntegerField(primary_key=True)
    updated_at = DateTimeField()

    class Meta:
        db_table = 'rounds'

class Pcaps(BaseModel):
    cbn = ForeignKeyField(db_column='cbn_id', rel_model=ChallengeBinaryNodes, to_field='id')
    created_at = DateTimeField()
    id = BigIntegerField(primary_key=True)
    round = ForeignKeyField(db_column='round_id', rel_model=Rounds, to_field='id')
    team = ForeignKeyField(db_column='team_id', rel_model=Teams, to_field='id')
    type = UnknownField()  # USER-DEFINED
    updated_at = DateTimeField()

    class Meta:
        db_table = 'pcaps'

class Performances(BaseModel):
    created_at = DateTimeField()
    id = BigIntegerField(primary_key=True)
    test = ForeignKeyField(db_column='test_id', rel_model=Tests, to_field='id')
    updated_at = DateTimeField()

    class Meta:
        db_table = 'performances'

class Scores(BaseModel):
    created_at = DateTimeField()
    id = BigIntegerField(primary_key=True)
    round = ForeignKeyField(db_column='round_id', rel_model=Rounds, to_field='id')
    score_actual = FloatField(null=True)
    score_predicted = FloatField(null=True)
    test = ForeignKeyField(db_column='test_id', rel_model=Tests, to_field='id')
    updated_at = DateTimeField()

    class Meta:
        db_table = 'scores'
