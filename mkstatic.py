import flask
from rolemapper import app,db
from rolemapper import models
from jinja2 import Environment, PackageLoader
import os

env = Environment(loader=PackageLoader('rolemapper', 'templates'))

def generate_hw_templates(outdir="conf"):
    generate_ethers()
        
def generate_ethers(outdir="conf", outfile="ethers"):
    t = env.get_template("etc/ethers")
    mac_hosts = []
    for m in models.HardwareInfo.query.all():
         mac_hosts.append(dict(mac=m.mac_address,host=m.hostname))
    out = open("%s/%s" %(outdir, outfile),"w")
    out.write(t.render(mac_hosts=mac_hosts))

def generate_all_templates():
    generate_hw_templates()

if __name__=="__main__":
    generate_all_templates()
