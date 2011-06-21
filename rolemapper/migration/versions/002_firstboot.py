from sqlalchemy import *
from migrate import *
from rolemapper import db
from sqlalchemy.ext.declarative import declarative_base

meta = MetaData()
kt   = Table('kick_targets', meta)

def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind migrate_engine
    # to your metadata
    meta.bind = migrate_engine
    col = Column('firstboot', String(255))
    col.create(kt)

def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pass

