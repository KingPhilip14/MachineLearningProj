from sqlalchemy import Table, Column, Integer, String, Boolean, MetaData, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB

metadata = MetaData()

move = Table(
    'move',
    metadata,
    Column('move_id', Integer, primary_key=True, nullable=False),
    Column('move_name', String, nullable=False),
    Column('damage_class', String, nullable=False),
    Column('move_type', String, nullable=False),
    Column('power', Integer, nullable=True),
    Column('accuracy', Integer, nullable=True),
    Column('pp', Integer, nullable=True),
    Column('priority', Integer, nullable=False),
)
