from sqlalchemy import *
from migrate import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Model = declarative_base()
meta = MetaData()

class Clusters(Model):
    __tablename__ = 'clusters'
    id = Column(Integer, primary_key = True)
    short_name = Column(String(40))
    display_name = Column(String(80))

class HardwareInfo(Model):
    __tablename__ = 'hardware_info'
    id = Column(Integer, primary_key=True)
    mac_address = Column(String(80), unique=True)
    hardware_info = Column(Text())
    ip_address = Column(String(16), unique=True)
    netmask = Column(String(16))
    gateway = Column(String(16))
    hostname = Column(String(255))
    kick_id = Column(Integer, ForeignKey('kick_targets.id')) # foreign keys?
    chef_role = Column(String(80))
    state     = Column(String(255), default="unmanaged")
    cluster_id = Column(Integer)

def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind migrate_engine
    # to your metadata
    meta.bind = migrate_engine
    Clusters.__table__.create(migrate_engine)

    Session = sessionmaker(bind = migrate_engine)
    new_cluster = Clusters(short_name = 'test', display_name = 'Default Cluster')
    session = Session()
    session.add(new_cluster)
    session.commit()

    HardwareInfo.__table__.metadata = meta

    # add the column, and update the rows
    HardwareInfo.__table__.c.cluster_id.create(HardwareInfo.__table__)
    
    conn = migrate_engine.connect()
    conn.execute(
    """
    UPDATE hardware_info SET cluster_id=1;
    """
    )

    clust = Table('clusters', meta, autoload=True,
                  autoload_with=migrate_engine)
    kick_targets = Table('kick_targets', meta, autoload=True,
                         autoload_with = migrate_engine)
    # add in the FK
    cons = ForeignKeyConstraint([HardwareInfo.__table__.c.cluster_id],
                                [clust.c.id])
    cons.create()

def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    meta.bind = migrate_engine
    kick_targets = Table('kick_targets', meta, autoload=True,
                         autoload_with = migrate_engine)

    HardwareInfo.__table__.metadata = meta    
    HardwareInfo.__table__.c.cluster_id.drop(HardwareInfo.__table__)

    Clusters.__table__.drop(migrate_engine)
