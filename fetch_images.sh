#!/bin/bash

# You should be able to run me to fetch all the appropriate kernels
# and initrds from somewhere

# I should also be made into a manage.py command

wget http://c752981.r81.cf2.rackcdn.com/syslinux-needful.tar.gz -qO- |
    tar xzC local/tftproot

mkdir local/tftproot/ubuntu
cd local/tftproot/ubuntu

images=( maverick natty oneiric precise)
for image in ${images[@]}; do
    echo "Grabbing files for ${image}"
    mkdir "${image}-amd64";
    # cp preseed.txt ../../../templates/preseed/${image}-amd64-preseed.txt;
    files=( initrd.gz linux )
    for file in ${files[@]}; do
        wget "http://archive.ubuntu.com/ubuntu/dists/${image}/main/installer-amd64/current/images/netboot/ubuntu-installer/amd64/${file}" -q -P ${image}-amd64;
    done;
done;
