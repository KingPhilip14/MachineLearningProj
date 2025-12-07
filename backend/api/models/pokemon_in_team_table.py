from sqlalchemy import Table, Column, Integer, ForeignKey, MetaData, String, Boolean
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func

metadata = MetaData()

pokemon_in_team_table = Table(
    'pokemon_in_team',
    metadata,
    Column('pit_id', Integer, primary_key=True),
    Column('team_id', Integer, ForeignKey('team.team_id', ondelete='CASCADE'), nullable=False),
    Column('pokemon_id', Integer, ForeignKey('pokemon.pokemon_id'), nullable=False),
    Column('chosen_ability_id', Integer, ForeignKey('ability.ability_id')),
    Column('nickname', String(30), nullable=False, default=''),
    Column('is_shiny', Boolean, nullable=False, default=False),
)
