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
touch '/tmp/none'

exit 0
