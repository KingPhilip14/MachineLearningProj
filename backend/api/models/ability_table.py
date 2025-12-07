from sqlalchemy import Table, Column, Integer, String, MetaData

metadata = MetaData()

ability = Table(
    'ability',
    metadata,
    Column('ability_id', Integer, primary_key=True),
    Column('ability_name', String, nullable=False, unique=True),
    Column('effect_desc', String, nullable=False),
    Column('short_desc', String, nullable=False),
    Column('flavor_text', String, nullable=False),
)
