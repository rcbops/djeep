#!/usr/bin/python

import subprocess
import sys
import traceback
import urllib2
from urllib import urlencode
try:
    import json
except ImportError:
    import simplejson as json

hardware_cmd = ["/usr/bin/lshw", "-json"]
cmdline_file = "/proc/cmdline"

hardware_info = subprocess.check_output(hardware_cmd, stderr=subprocess.PIPE)
args = [ x.split("=",1) for x in 
    open(cmdline_file, "r").readline().strip().split()
    if x.find("=") > 0 ]

kv = {}
for k,v in args:
    kv[k] = v
mac_address = kv['macaddr']
dsc_base = kv['url']
dsc_hw_new = dsc_base + "/admin/hardware/new"
dsc_hw_list = dsc_base + "/admin/hardware/view"
dsc_hw_edit= dsc_base + "/admin/hardware/edit/{0}"

data = json.dumps(dict(mac_address=mac_address, 
                   hardware_info=hardware_info))
req = urllib2.Request(dsc_hw_new, data, {"Content-Type": "application/json"})

try:
    urllib2.urlopen(req)
except urllib2.HTTPError, e:
    if e.code == 500:
    #check to see if mac currently exists.  If so, update mac with new hwinfo
        try:
            req = urllib2.Request(dsc_hw_list)
            req.add_header("Accept", "application/json")
            hw = json.loads(urllib2.urlopen(req).read())['hardware']
            record = [s for s in hw if s["mac_address"] == mac_address][0]
            req = urllib2.Request(dsc_hw_edit.format(record['id']),
                              data, {"Content-Type": "application/json"})
            urllib2.urlopen(req)
        except:
            traceback.print_exc(file=sys.stdout)
            #Discovery has failed.  Reboot!
            print "Discovery failed.  Rebooting."
            #subprocess.call("/sbin/reboot")
