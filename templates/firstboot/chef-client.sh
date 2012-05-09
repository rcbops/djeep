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

if [ ! -f /usr/bin/chef-client ]; then
    bash < <(curl -s http://s3.amazonaws.com/opscode-full-stack/install.sh)
fi

mkdir -p /etc/chef

cat > /etc/chef/client.rb <<EOF
log_level	:info
log_location	STDOUT

chef_server_url	'{{ site.chef_server_url }}'
validation_client_name	'{{ site.validation_client_name }}'
environment '{{ site.chef_environment }}'

{% if site.http_proxy %}
    http_proxy '{{ site.http_proxy|safe }}'
{% endif %}
{% if site.https_proxy %}
    https_proxy '{{ site.https_proxy|safe }}'
{% endif %}
{% if site.http_proxy_user %}
    http_proxy_user '{{ site.http_proxy_user|safe }}'
{% endif %}
{% if site.http_proxy_pass %}
    http_proxy_pass '{{ site.http_proxy_pass|safe }}'
{% endif %}
EOF

wget -O /etc/chef/validation.pem http://{{site.webservice_host}}:{{site.webservice_port}}/media/chef_validators/{{site.chef_validation_pem}}

/usr/bin/chef-client
