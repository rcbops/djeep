#!/usr/bin/python

import sys
import socket
import urllib2

try:
    import json
except ImportError:
    import simplejson as json

def main():
    hostname = socket.gethostname()

    if len(sys.argv) == 2:
        log_file = open(sys.argv[1],"r")
    else:
        log_file = sys.stdin
    
    macs = set("")
    
    while 1:
        line = log_file.readline()
        if not line:
            break
        mac = ""
        line = line[line.find(hostname):]
        (syslog_stuff, msg) = [ x.strip() for x in line.split(":",1) ]
        if msg.find("DHCPDISCOVER") >= 0 and msg.find("ignored") > 0:
            mac = msg.split()[1]
        if msg.find("DHCPDISCOVER") >= 0 and msg.find("no address available") > 0:
            parts = msg.split()
            idx = parts.index("no") - 1
            mac = msg.split()[idx]
        if not mac in macs:
            macs.add(mac)
            register_mac(mac)

def register_mac(mac,url="http://localhost:5000/admin/hardware/new"):
    data = json.dumps(dict(mac_address=mac))
    req = urllib2.Request(url, data, {"Content-Type": "application/json"})
    try:
        urllib2.urlopen(req)
    except urllib2.HTTPError, e:
        #ignore error
        pass
                
if __name__=="__main__":
    main()
