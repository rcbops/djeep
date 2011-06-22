from sqlalchemy import *
from migrate import *
from sqlalchemy.ext.declarative import declarative_base

Model = declarative_base()
meta = MetaData()

class KickTargets(Model):
    __tablename__ = 'kick_targets'
    id = Column(Integer, primary_key = True)
    name = Column(String(40))
    pxeconfig = Column(String(40))
    kernel = Column(String(255))
    initrd = Column(String(255))
    preseed = Column(String(255))
    post_script = Column(String(255))
    firstboot = Column(String(255))

kt   = KickTargets.__table__
kt.metadata = meta
newcols = [ "firstboot" ]

def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind migrate_engine
    # to your metadata
    meta.bind = migrate_engine
    for c in kt.get_children():
        if c.name in newcols:
            c.create(kt)

    conn = migrate_engine.connect()
    conn.execute(
    """
    UPDATE kick_targets SET firstboot=post_script,post_script="";
    """
    )
def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    meta.bind = migrate_engine
    kt._bind = migrate_engine
    conn = migrate_engine.connect()
    conn.execute(
    """
    UPDATE kick_targets SET post_script=firstboot;
    """
    )
    for c in kt.get_children():
        if c.name in newcols:
            c.drop(kt)
