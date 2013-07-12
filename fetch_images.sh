#!/bin/bash

# You should be able to run me to fetch all the appropriate kernels
# and initrds from somewhere

# I should also be made into a manage.py command
OLDPWD="$PWD"
cd "$(dirname $0)"

echo "Downloading syslinux 6.01"
wget https://www.kernel.org/pub/linux/utils/boot/syslinux/syslinux-6.01.tar.bz2 -qO- | tar xj

cd local/tftproot
ln -s ../../syslinux-6.01/bios/core/pxelinux.0
ln -s ../../syslinux-6.01/bios/com32/menu/menu.c32
ln -s ../../syslinux-6.01/bios/com32/mboot/mboot.c32
ln -s ../../syslinux-6.01/bios/com32/chain/chain.c32
mkdir ubuntu
cd ubuntu

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
cd $OLDPWD
