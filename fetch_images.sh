#!/bin/bash

# You should be able to run me to fetch all the appropriate kernels
# and initrds from somewhere

# I should also be made into a manage.py command

wget http://c752981.r81.cf2.rackcdn.com/syslinux-needful.tar.gz -qO- |
    tar xzC local/tftproot
wget http://c752981.r81.cf2.rackcdn.com/maverick.tar.gz -qO- |
    tar xzC local/tftproot
