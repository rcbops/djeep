from sqlalchemy import *
from migrate import *
from rolemapper import db
from sqlalchemy.ext.declarative import declarative_base

Model = declarative_base()

class TemplateVars(Model):
    __tablename__ = 'template_vars'
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(80), unique=True)
    value = db.Column(db.Text())

class HardwareInfo(Model):
    __tablename__ = 'hardware_info'
    id = db.Column(db.Integer, primary_key=True)
    mac_address = db.Column(db.String(80), unique=True)
    hardware_info = db.Column(db.Text())
    ip_address = db.Column(db.String(16), unique=True)
    netmask = db.Column(db.String(16))
    gateway = db.Column(db.String(16))
    hostname = db.Column(db.String(255), unique=True) # not quite right
    kick_id = db.Column(db.Integer, db.ForeignKey('kick_targets.id')) # foreign keys?
    kick_target = db.relationship('KickTargets')
    chef_role = db.Column(db.String(80))

class KickTargets(Model):
    __tablename__ = 'kick_targets'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(40))
    pxeconfig = db.Column(db.String(40))
    kernel = db.Column(db.String(255))
    initrd = db.Column(db.String(255))
    preseed = db.Column(db.String(255))
    post_script = db.Column(db.String(255))


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind migrate_engine
    # to your metadata
    TemplateVars.__table__.create(migrate_engine)
    HardwareInfo.__table__.create(migrate_engine)
    KickTargets.__table__.create(migrate_engine)
    pass

def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pass

