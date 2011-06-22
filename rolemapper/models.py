from rolemapper import db
import sqlalchemy.types as types
import subprocess

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
    state     = db.Column(db.String(255), default="unmanaged")
    def on_change(self):
        """update conf/etc/ethers, conf/etc/hosts, and pxelinux config, and send sighup to dnsmasq"""
        from jinja2 import Environment, PackageLoader
        env = Environment(loader=PackageLoader('rolemapper', 'templates'))
        ethers_f = "/etc/ethers"
        hosts_f  = "/etc/hosts"
        boot_f  = "tftproot/pxelinux.cfg/01-%s" % (
                      self.mac_address.replace(":","-").lower())
        ethers_t = env.get_template("etc/ethers")
        hosts_t = env.get_template("etc/hosts")
        boot_t  = env.get_template("pxeconfig/%s" % (
                                   self.kick_target.pxeconfig))
        kvpairs = TemplateVars.query.all()
        site =  dict(zip([x.key for x in kvpairs], [x.value for x in kvpairs]))
        hardware = HardwareInfo.query.all()
        ethers = []
        hosts = []

        for h in hardware:
            hosts.append(dict(ip=h.ip_address, host=h.hostname))
            ethers.append(dict(mac=h.mac_address, host=h.hostname))

        with open(ethers_f,"w") as f:
            f.write(ethers_t.render(ethers=ethers))
        with open(hosts_f,"w") as f:
            f.write(hosts_t.render(hosts=hosts))
        with open(boot_f,"w") as f:
            f.write(boot_t.render(host=self, site=site))
        subprocess.call("kill -hup $(pgrep dnsmasq)", shell=True)
class KickTargets(db.Model):
    __tablename__ = 'kick_targets'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(40))
    pxeconfig = db.Column(db.String(40))
    kernel = db.Column(db.String(255))
    initrd = db.Column(db.String(255))
    preseed = db.Column(db.String(255))
    post_script = db.Column(db.String(255))
    firstboot = db.Column(db.String(255))

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

