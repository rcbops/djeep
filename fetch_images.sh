#!/bin/bash

# You should be able to run me to fetch all the appropriate kernels
# and initrds from somewhere

# I should also be made into a manage.py command
OLDPWD="$PWD"
cd "$(dirname $0)"

echo "Downloading syslinux 6.01"
wget https://www.kernel.org/pub/linux/utils/boot/syslinux/syslinux-6.01.tar.bz2 -qO- | tar xj

cd local/tftproot
for s in core/pxelinux.0 com32/menu/menu.c32 com32/mboot/mboot.c32 com32/chain/chain.c32 \
                         com32/elflink/ldlinux/ldlinux.c32 com32/libutil/libutil.c32 \
                         com32/lib/libcom32.c32; do 
    ln -s "../../syslinux-6.0.1/bios/${s}"
done
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
