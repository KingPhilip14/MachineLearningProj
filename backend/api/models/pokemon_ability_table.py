from sqlalchemy import Table, Column, Integer, Boolean, MetaData, ForeignKey

metadata = MetaData()

pokemon_ability = Table(
    'pokemon_ability',
    metadata,
    Column('pokemon_id', Integer, ForeignKey('pokemon.pokemon_id'), primary_key=True, nullable=False),
    Column('ability_id', Integer, ForeignKey('ability.ability_id'), primary_key=True, nullable=False),
    Column('is_hidden', Boolean, nullable=False, default=False),
)
