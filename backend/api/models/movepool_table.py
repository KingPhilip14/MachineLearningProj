from sqlalchemy import Table, Column, Integer, MetaData, ForeignKey

metadata = MetaData()

movepool = Table(
    'movepool',
    metadata,
    Column('pokemon_id', Integer, ForeignKey('pokemon.pokemon_id'), primary_key=True, nullable=False),
    Column('move_id', Integer, ForeignKey('move.move_id'), primary_key=True, nullable=False)
)
