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

ADMIN_PASS=secret

cat <<EOF | debconf-set-selections
chef-solr chef-solr/amqp_password password ${ADMIN_PASS}
chef-server-webui chef-server-webui/admin_password password ${ADMIN_PASS}
EOF

apt-get install -y chef chef-server git-core
knife configure -i -y --defaults -r='' -u openstack
cd /root; git clone https://github.com/openstack/openstack-cookbooks.git
knife cookbook upload -o /root/openstack-cookbooks/cookbooks -a

exit 0
