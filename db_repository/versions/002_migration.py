from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
user = Table('user', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('firstname', VARCHAR(length=64)),
    Column('lastname', VARCHAR(length=64)),
    Column('is_enabled', BOOLEAN),
    Column('registered_on', DATETIME),
    Column('email', VARCHAR(length=120)),
    Column('email_confirmed', BOOLEAN),
    Column('confirmed_at', DATETIME),
    Column('phone_num', INTEGER),
    Column('password', VARCHAR(length=54)),
    Column('reset_password_token', VARCHAR(length=100)),
)

user = Table('user', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('first_name', String(length=64)),
    Column('last_name', String(length=64)),
    Column('is_enabled', Boolean, default=ColumnDefault(True)),
    Column('registered_on', DateTime),
    Column('email', String(length=120)),
    Column('email_confirmed', Boolean),
    Column('confirmed_at', DateTime),
    Column('phone_num', Integer),
    Column('password', String(length=54)),
    Column('reset_password_token', String(length=100), default=ColumnDefault('')),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['user'].columns['firstname'].drop()
    pre_meta.tables['user'].columns['lastname'].drop()
    post_meta.tables['user'].columns['first_name'].create()
    post_meta.tables['user'].columns['last_name'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['user'].columns['firstname'].create()
    pre_meta.tables['user'].columns['lastname'].create()
    post_meta.tables['user'].columns['first_name'].drop()
    post_meta.tables['user'].columns['last_name'].drop()
