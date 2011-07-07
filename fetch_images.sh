#!/bin/bash

# You should be able to run me to fetch all the appropriate kernels
# and initrds from somewhere

# I should also be made into a manage.py command

wget http://c222662.r62.cf1.rackcdn.com/syslinux-needful.tar.gz -qO- |
    tar xzC tftproot
wget http://c222662.r62.cf1.rackcdn.com/maverick.tar.gz -qO- |
    tar xzC tftproot
