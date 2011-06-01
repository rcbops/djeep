from rolemapper import db

class TemplateVars(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(80), unique=True)
    value = db.Column(db.Text())

class HardwareInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mac_address = db.Column(db.String(80), unique=True)
    hardware_info = db.Column(db.Text())
    ip_address = db.Column(db.String(16), unique=True)
    netmask = db.Column(db.String(16))
    gateway = db.Column(db.String(16))
    hostname = db.Column(db.String(255), unique=True) # not quite right
    chef_role = db.Column(db.String(80))

def commit(*models):
    for m in models:
        db.session.add(m)
    db.session.commit()
