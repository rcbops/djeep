This repository contains tools for bootstrapping a cloud from bare metal.

# Overview

0. Set up chef server
1. Launch the webservice for collecting hardware information
2. Build a PXE image that contains a configured hardware reporting agent
3. Launch dnsmasq to boot all hardware with that image
4. Navigate to webapp to tag discovered machines with chef roles
5. Dump new pxe images and configuration from webapp
6. Reboot machines to get new pxe that applies their chef roles

