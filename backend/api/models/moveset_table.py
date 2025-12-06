from sqlalchemy import Table, Column, Integer, ForeignKey, MetaData

metadata = MetaData()

moveset = Table(
    'moveset',
    metadata,
    Column('moveset_id', Integer, primary_key=True),
    Column('move_id', Integer, ForeignKey('move.move_id'), nullable=False),
)
