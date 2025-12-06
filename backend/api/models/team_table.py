from sqlalchemy import Table, Column, Integer, ForeignKey, MetaData, String, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func

metadata = MetaData()

team = Table(
    'team',
    metadata,
    Column('team_id', Integer, primary_key=True, autoincrement=True),
    Column('account_id', Integer, ForeignKey('account.account_id', ondelete='CASCADE'), nullable=False),
    Column('team_name', String, nullable=False, default='My Team'),
    Column('generation', String, nullable=False),
    Column('time_created', DateTime(timezone=True), nullable=False, server_default=func.now()),
    Column('last_time_used', DateTime(timezone=True), nullable=False, server_default=func.now()),
    Column('overlapping_weaknesses', JSONB, nullable=False),
)
