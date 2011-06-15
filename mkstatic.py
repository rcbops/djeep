import flask
from rolemapper import app,db
from rolemapper import models
from jinja2 import Environment, PackageLoader
import os

env = Environment(loader=PackageLoader('rolemapper', 'templates'))

def generate_hw_templates(outdir="conf/etc"):
    generate_ethers()
    generate_hosts()
    generate_pxelinux()
        
def generate_ethers(outdir="conf/etc", outfile="ethers"):
    t = env.get_template("etc/ethers")
    ethers = []
    for m in models.HardwareInfo.query.all():
         ethers.append(dict(mac=m.mac_address,host=m.hostname))
    with open("%s/%s" %(outdir, outfile),"w") as out:
        out.write(t.render(ethers=ethers))
    
def generate_hosts(outdir="conf/etc", outfile="hosts"):
    t = env.get_template("etc/hosts")
    hosts = []
    for h in models.HardwareInfo.query.all():
        hosts.append(dict(ip=h.ip_address, host=h.hostname))
    with open("%s/%s" % (outdir, outfile), "w") as out:
        out.write(t.render(hosts=hosts))

def generate_pxelinux(outdir="tftproot/pxelinux.cfg"):
    kvpairs = models.TemplateVars.query.all()
    site = dict(zip([x.key for x in kvpairs], [x.value for x in kvpairs]))
    for host in models.HardwareInfo.query.all():
        t = env.get_template("pxeconfig/%s" % host.kick_target.pxeconfig)
        outfile = host.mac_address.replace(":","-").lower()
        with open("%s/%s" % (outdir, outfile), "w") as out:
            out.write(t.render(host=host,site=site))

def generate_all_templates():
    generate_hw_templates()

if __name__=="__main__":
    generate_all_templates()
