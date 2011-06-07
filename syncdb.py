from rolemapper import models

models.db.create_all()

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

if models.HardwareInfo.query.first() is None:
    models.commit(models.HardwareInfo(mac_address = '00:00:00:00:00:00',
                                      hardware_info = '{}',
                                      ip_address = '192.168.122.100',
                                      netmask = '255.255.255.0',
                                      gateway = '192.168.122.1',
                                      hostname = 'host-n01',
                                      chef_role = 'chef_server'))
