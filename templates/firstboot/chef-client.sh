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

# Check if we have network access before continuing
until ping -q -w 1 -c 1 `ip r | grep default | cut -d ' ' -f 3` > /dev/null; do
  sleep 5
done

# Download and install the chef-client
if [ ! -f /usr/bin/chef-client ]; then
    bash < <(curl -s  http://www.opscode.com/chef/install.sh)
fi

# Create the required directories
mkdir -p /etc/chef /var/log/chef

# Create the chef client configuration
cat > /etc/chef/client.rb <<EOF
log_level	:info
log_location	STDOUT

chef_server_url	'{{ site.chef_server_url }}'
environment '{{ site.chef_environment }}'

{% if site.validation_client_name %}
    validation_client_name '{{ site.validation_client_name }}'
{% endif %}
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

# Get the chef validator certificate
wget -O /etc/chef/validation.pem http://{{site.webservice_host}}:{{site.webservice_port}}/media/chef_validators/{{site.chef_validation_pem}}

# Configure chef-client upstart
cp /opt/chef/embedded/lib/ruby/gems/1.9.1/gems/chef-`dpkg-query --show chef | awk '{print $2}' | awk -F- '{print $1}'`/distro/debian/etc/init/chef-client.conf /etc/init/
ln -s /lib/init/upstart-job /etc/init.d/chef-client

# If a role is assigned, use it
{% if host.role %}
cat > /etc/chef/firstboot.json <<EOF
{ "run_list":
    [
      "role[{{host.role}}]"
    ]
}
EOF
chef-client -j /etc/chef/firstboot.json
{% endif %}

# Start the chef-client service
service chef-client start
