#!/bin/sh


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

apt-get install -y puppet
/etc/init.d/puppet stop

cat > /etc/puppet/puppet.conf <<EOF
[main]
logdir=/var/log/puppet
vardir=/var/lib/puppet
ssldir=/var/lib/puppet/ssl
rundir=/var/run/puppet
factpath=$vardir/lib/facter
templatedir=$confdir/templates
prerun_command=/etc/puppet/etckeeper-commit-pre
postrun_command=/etc/puppet/etckeeper-commit-post
server = {{ site.puppet_server }}

[master]
# These are needed when the puppetmaster is run by passenger
# and can safely be removed if webrick is used.
ssl_client_header = SSL_CLIENT_S_DN
ssl_client_verify_header = SSL_CLIENT_VERIFY
EOF

/etc/init.d/puppet start

exit 0
