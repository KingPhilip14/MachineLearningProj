from sqlalchemy import Table, Column, Integer, ForeignKey, MetaData, UniqueConstraint

metadata = MetaData()

moveset = Table(
    'moveset',
    metadata,
    Column('moveset_id', Integer, primary_key=True),
    Column('pit_id', Integer, ForeignKey('pokemon_in_team.move_id'), nullable=False),
    Column('move_id', Integer, ForeignKey('move.move_id'), nullable=False),
    Column('slot_number', Integer, nullable=False),
    UniqueConstraint('pit_id', 'slot_number', name='pit_with_slot_number'),
    UniqueConstraint('pit_id', 'move_id', name='pit_with_move_id'),
)
