from sqlalchemy import Table, Column, Integer, String, Boolean, MetaData, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB

metadata = MetaData()

pokemon = Table(
    'pokemon',
    metadata,
    Column('pokemon_id', Integer, primary_key=True, nullable=False),
    Column('pokemon_name', String, nullable=False),
    Column('pokemon_role', String, nullable=False),
    Column('type_1', String, nullable=False),
    Column('type_2', String, nullable=False),
    Column('bst', Integer, nullable=False),
    Column('hp', Integer, nullable=False),
    Column('attack', Integer, nullable=False),
    Column('defense', Integer, nullable=False),
    Column('special_attack', Integer, nullable=False),
    Column('special_defense', Integer, nullable=False),
    Column('speed', Integer, nullable=False),
    Column('is_legend_or_mythical', Boolean, nullable=False),
    Column('weaknesses', JSONB, nullable=False),
    Column('resistances', JSONB, nullable=False),
)
