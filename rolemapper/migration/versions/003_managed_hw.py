from sqlalchemy import *
from migrate import *
from sqlalchemy.ext.declarative import declarative_base

Model = declarative_base()
meta = MetaData()
class HardwareInfo(Model):
    __tablename__ = 'hardware_info'
    id = Column(Integer, primary_key=True)
    mac_address = Column(String(80), unique=True)
    hardware_info = Column(Text())
    ip_address = Column(String(16), unique=True)
    netmask = Column(String(16))
    gateway = Column(String(16))
    hostname = Column(String(255), unique=True) # not quite right
    kick_id = Column(Integer, ForeignKey('kick_targets.id')) # foreign keys?
    kick_target = relationship('KickTargets')
    chef_role = Column(String(80))
    managed = Column(Boolean())

hi   = hi.__table__
hi.metadata = meta
newcols = [ "managed" ]

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
    UPDATE hardware_info SET managed=True;
    """
    )
def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    meta.bind = migrate_engine
    kt._bind = migrate_engine
    for c in kt.get_children():
        if c.name in newcols:
            c.drop(kt)
