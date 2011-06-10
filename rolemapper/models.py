from rolemapper import db

class TemplateVars(db.Model):
    __tablename__ = 'template_vars'
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(80), unique=True)
    value = db.Column(db.Text())

class HardwareInfo(db.Model):
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
                                  

class KickTargets(db.Model):
    __tablename__ = 'kick_targets'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(40))
    pxeconfig = db.Column(db.String(40))
    kernel = db.Column(db.String(255))
    initrd = db.Column(db.String(255))
    preseed = db.Column(db.String(255))
    post_script = db.Column(db.String(255))

    def __repr__(self):
        return self.name

def commit(*models):
    for m in models:
        db.session.add(m)
    db.session.flush()

ModelList = {
    "keys": TemplateVars,
    "hardware": HardwareInfo,
    "targets": KickTargets
}

