from sqlalchemy import *
from migrate import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Model = declarative_base()
meta = MetaData()
class HardwareInfo(Model):
    __tablename__ = 'hardware_info'
    id = Column(Integer, primary_key = True)
    state = Column(String(255), default="unmanaged")

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


hi   = HardwareInfo.__table__
hi.metadata = meta
newcols = [ "state" ]

def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind migrate_engine
    # to your metadata
    meta.bind = migrate_engine
    for c in hi.get_children():
        if c.name in newcols:
            c.create(hi)

    conn = migrate_engine.connect()
    conn.execute(
    """
    UPDATE hardware_info SET state="managed";
    """
    )
def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    meta.bind = migrate_engine
    for c in hi.get_children():
        if c.name in newcols:
            c.drop(hi)
