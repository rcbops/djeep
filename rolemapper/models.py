from rolemapper import db


class HardwareInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mac_address = db.Column(db.String(80), unique=True)
    hardware_info = db.Column(db.Text())
    chef_role = db.Column(db.String(80))


def commit(*models):
    for m in models:
        db.session.add(m)
    db.session.commit()
