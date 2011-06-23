import os 
import sys
from rolemapper import models
from rolemapper.config import SQLALCHEMY_DATABASE_URI as db
from migrate.versioning.api import *
from migrate.exceptions import DatabaseNotControlledError

repo = "rolemapper/migration"
try: 
    db_version(db, repo)
except DatabaseNotControlledError:
    if os.path.exists(db):
        print "%s already exists without versioning.  Please either start " + \
              "fresh or use the migration tools to set an appropriate " + \
              "version in your database." % db
    version_control(db, repo)
upgrade(db,repo)
#models.db.create_all()


# dummy up some sample values
default_kvs = {
    'domainname': 'lab',
    'nameserver': '192.168.122.1',
    'gateway': '192.168.122.1',
    'webservice_host': '192.168.122.2',
    'webservice_port': '5000',
    'chef_url': 'http://192.168.122.3:4000', # or opscode
}

for key in default_kvs:
    if models.TemplateVars.query.filter(
            models.TemplateVars.key == key).first() is None:
        models.commit(models.TemplateVars(key=key, value=default_kvs[key]))

if models.Clusters.query.first() is None:
    models.commit(models.Clusters(short_name = "test",
                                 display_name = "Default Cluster"))
    
if models.KickTargets.query.first() is None:
    models.commit(models.KickTargets(name = 'Boot to HDD',
                                     pxeconfig = 'hdd',
                                     kernel = '',
                                     initrd = '',
                                     preseed = '',
                                     post_script = '',
                                     firstboot = ''))

    models.commit(models.KickTargets(name = 'Defaults (maverick amd64)',
                                     pxeconfig = 'ubuntu',
                                     kernel = 'ubuntu/maverick-amd64/linux',
                                     initrd = 'ubuntu/maverick-amd64/initrd.gz',
                                     preseed = 'maverick-amd64-preseed.txt',
                                     post_script = 'debian.sh',
                                     firstboot = 'none.sh'))

    models.commit(models.KickTargets(name = 'Puppet Client (maverick amd64)',
                                     pxeconfig = 'ubuntu',
                                     kernel = 'ubuntu/maverick-amd64/linux',
                                     initrd = 'ubuntu/maverick-amd64/initrd.gz',
                                     preseed = 'maverick-amd64-preseed.txt',
                                     post_script = 'debian.sh',
                                     firstboot = 'puppet-client.sh'))

if models.HardwareInfo.query.first() is None:
    models.commit(models.HardwareInfo(mac_address = '00:00:00:00:00:00',
                                      hardware_info = '{}',
                                      ip_address = '192.168.122.100',
                                      netmask = '255.255.255.0',
                                      gateway = '192.168.122.1',
                                      hostname = 'host-n01',
                                      kick_id = 1,
                                      cluster_id = 1,
                                      chef_role = 'chef_server'))

