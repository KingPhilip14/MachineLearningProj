from sqlalchemy import Table, Column, Integer, String, MetaData

metadata = MetaData()

account = Table(
    'account',
    metadata,
    Column('account_id', Integer, primary_key=True, autoincrement=True),
    Column('username', String(30), nullable=False, unique=True),
    Column('password', String(30), nullable=False),
)
