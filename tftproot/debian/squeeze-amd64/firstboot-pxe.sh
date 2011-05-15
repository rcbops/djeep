#!/bin/bash

### BEGIN INIT INFO
# Provides:          firstboot
# Required-Start:    $local_fs $network $syslog
# Required-Stop:     $local_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Firstboot actions
# Description:       Firstboot actions
### END INIT INFO

#set -e
#set -x

sleep 10

sed -i /etc/rc.local -e 's_/root/install.sh_exit 0_'

if [ -t 1 ]; then
    exec >/tmp/firstboot.log
    exec 2>&1
fi

apt-get install -y syslinux dnsmasq syslinux-common

SERVER_IP=`/sbin/ifconfig eth0 | grep "inet" | cut -d ':' -f2 | cut -d ' ' -f1`
GATEWAY_IP=`/sbin/route -n | grep "^0" | awk '{ print $2 }'`

cat > /etc/dnsmasq.conf <<EOF
dhcp-range=192.168.122.10,192.168.122.20,30m
dhcp-ignore=tag:!known
dhcp-option=3,${GATEWAY_IP}
dhcp-option-force=208,f1:00:74:7e
dhcp-option-force=210,/
dhcp-option-force=211,30i
dhcp-boot=pxelinux.0
enable-tftp
tftp-root=/srv/tftproot
EOF

mkdir -p /srv/tftproot

cp /usr/lib/syslinux/chain.c32 /usr/lib/syslinux/menu.c32 /usr/lib/syslinux/pxelinux.0 /srv/tftproot

mkdir /srv/tftproot/pxelinux.cfg
cat > /srv/tftproot/pxelinux.cfg/default <<EOF
default menu.c32
prompt 0
menu title PXE Boot
timeout 100
label local
  menu label Local Boot
  kernel chain.c32
  append hd0 0
EOF

# make debian distros

DEBIAN_DISTROS=squeeze
UBUNTU_DISTROS=maverick

ARCHES=amd64

for distro in ${DEBIAN_DISTROS}; do
    for arch in ${ARCHES}; do
	mkdir -p /srv/tftproot/debian/${distro}-${arch}

	wget http://mirrors.kernel.org/debian/dists/${distro}/main/installer-${arch}/current/images/netboot/debian-installer/${arch}/initrd.gz -O /srv/tftproot/debian/${distro}-${arch}/initrd.gz

	wget http://mirrors.kernel.org/debian/dists/${distro}/main/installer-${arch}/current/images/netboot/debian-installer/${arch}/linux -O /srv/tftproot/debian/${distro}-${arch}/linux

	cat >> /srv/tftproot/pxelinux.cfg/default <<EOF
label ${distro}-${arch}
  menu label Debian ${distro} (${arch}) installer
  kernel debian/${distro}-${arch}/linux
  append auto=true priority=critical vga=788 initrd=debian/${distro}-${arch}/initrd.gz languagechooser/language-name=English countrychooser/shortlist=US consol-keymaps-at/keymap=en preseed/url=tftp://${SERVER_IP}/debian/${distro}-${arch}/preseed.txt

EOF
    done
done

for distro in ${UBUNTU_DISTROS}; do
    for arch in ${ARCHES}; do
	mkdir -p /srv/tftproot/ubuntu/${distro}-${arch}

	wget http://mirrors.kernel.org/ubuntu/dists/${distro}/main/installer-${arch}/current/images/netboot/ubuntu-installer/${arch}/initrd.gz -O /srv/tftproot/ubuntu/${distro}-${arch}/initrd.gz

	wget http://mirrors.kernel.org/ubuntu/dists/${distro}/main/installer-${arch}/current/images/netboot/ubuntu-installer/${arch}/linux -O /srv/tftproot/ubuntu/${distro}-${arch}/linux

	cat >> /srv/tftproot/pxelinux.cfg/default <<EOF
label ${distro}-${arch}
  menu label Ubuntu ${distro} (${arch}) installer
  kernel ubuntu/${distro}-${arch}/linux
  append auto=true priority=critical vga=788 initrd=ubuntu/${distro}-${arch}/initrd.gz languagechooser/language-name=English countrychooser/shortlist=US consol-keymaps-at/keymap=en preseed/url=tftp://${SERVER_IP}/ubuntu/${distro}-${arch}/preseed.txt

EOF

    done
done



exit 0
