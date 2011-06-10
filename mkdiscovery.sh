#!/bin/bash

mkdir discovery
debootstrap sid discovery/
chroot discovery /bin/bash -c 'apt-get update'
chroot discovery /bin/bash -c 'apt-get install -y python-flask linux-image-amd64'
chroot discovery /bin/bash -c 'ln -s /sbin/init init'
mv discovery/boot/vmlinuz* .
rm discovery/initrd.img
rm discovery/boot/*
rm discovery/etc/udev/rules.d/70-persistent-net.rules
cat <<EOF > discovery/etc/network/interfaces
auto lo
iface lo inet loopback

auto eth0
iface eth0 inet dhcp
EOF
echo discovery > discovery/etc/hostname
chroot discovery bash -c "echo root:$(cat rootpass.txt)|chpasswd"
wget https://raw.github.com/rpedde/os-kick/master/discover.py -o discovery/usr/bin
chmod 755 discovery/usr/bin/discover.py
cat << EOF > discovery/etc/rc.local
#!/bin/sh -e
/usr/bin/discover.py
exit 0
EOF

cd discovery
find . | cpio -H newc -o > ../rootfs
cd ..
if [ -f rootfs.gz ]; then rm -f rootfs.gz; fi
gzip rootfs
