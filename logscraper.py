#!/usr/bin/python

import sys
import socket

hostname = socket.gethostname()

if len(sys.argv) == 2:
    log_file = open(sys.argv[1],"r")
else:
    log_file = sys.stdin

while 1:
    line = log_file.readline()
    if not line:
        break
    line = line[line.find(hostname):]
    (syslog_stuff, msg) = [ x.strip() for x in line.split(":",1) ]
    if msg.find("DHCPDISCOVER") >= 0 and msg.find("ignored") > 0:
        print msg.split()[1]
    if msg.find("DHCPDISCOVER") >= 0 and msg.find("no address available") > 0:
        print msg.split()[2]
