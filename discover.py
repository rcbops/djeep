#!/usr/bin/python

import subprocess
import urllib2
from urllib import urlencode
try:
    import json
except ImportError:
    import simplejson as json

cmdline_file = "/home/will/Scratch/cmdline"
discovery_url = "http://localhost:5000/admin/hardware/new"
hardware_cmd = ["/usr/bin/lshw", "-json"]

hardware_info = subprocess.check_output(hardware_cmd, stderr=subprocess.PIPE)
mac_address = [ x.split("=")[1] for x in 
    open(cmdline_file, "r").readline().strip().split()
    if x.find("macaddr=") == 0 ][0]

data = json.dumps(dict(mac_address=mac_address, 
                       hardware_info=hardware_info))
req = urllib2.Request(discovery_url, data, {"Content-Type": "text/json"})
print urllib2.open(req)
