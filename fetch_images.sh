#!/bin/bash

# You should be able to run me to fetch all the appropriate kernels
# and initrds from somewhere

# I should also be made into a manage.py command

wget http://c752981.r81.cf2.rackcdn.com/syslinux-needful.tar.gz -qO- |
    tar xzC local/tftproot

mkdir local/tftproot/ubuntu
cd local/tftproot/ubuntu

echo "Grabbing example-preseed.txt from 12.04"
wget https://help.ubuntu.com/12.04/installation-guide/example-preseed.txt -qO preseed.txt

# Replace incorrect preseed options
echo "fixing up the preseed.txt"
sed -i 's/mirror\/http\/hostname string archive.ubuntu.com/mirror\/http\/hostname string mirrors.kernel.org/' preseed.txt
sed -i 's/tasksel tasksel\/first multiselect ubuntu-desktop/tasksel tasksel\/first multiselect/' preseed.txt

# Append missing preseed options
cat >> preseed.txt <<EOF
d-i console-setup/layoutcode string u
d-i partman/default_filesystem string ext3
d-i partman-partitioning/confirm_write_new_label boolean true
d-i passwd/root-login boolean true
d-i passwd/root-password-crypted password $6$jyyLCMqW$7nSLacOYqUIUr5JYERuSIu7dphHz0/tL50rp.wHRksILe6D0wLgmFlxZQRsejsxM2Ti64rI43ekeA9rmy1PTV0
d-i passwd/user-fullname string Demo User
d-i passwd/username string demo
d-i passwd/user-password password demo
d-i passwd/user-password-again password demo
d-i user-setup/allow-password-weak boolean true
d-i apt-setup/restricted boolean true
d-i apt-setup/universe boolean tru
d-i pkgsel/include string openssh-server
popularity-contest popularity-contest/participate boolean false
d-i grub-installer/grub2_instead_of_grub_legacy boolean false
EOF

images=( maverick natty oneiric precise)
for image in ${images[@]}; do
    echo "Grabbing files for ${image}"
    mkdir "${image}-amd64";
    cp preseed.txt ${image}-amd64/${image}-amd64-preseed.txt;
    files=( initrd.gz linux )
    for file in ${files[@]}; do
        wget "http://archive.ubuntu.com/ubuntu/dists/${image}/main/installer-amd64/current/images/netboot/ubuntu-installer/amd64/${file}" -q -P ${image}-amd64;
    done;
done;
