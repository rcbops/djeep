#!/bin/bash

curl -skS http://{{site.webservice_host}}:{{site.webservice_port}}/firstboot/{{host.id}} > /root/install.sh

if [ -s /root/install.sh ]; then
    chmod +x /root/install.sh
    sed -i /etc/rc.local -e 's_exit 0_/root/install.sh_'
fi

echo "{{host.hostname}}" > /etc/hostname
curl http://{{site.webservice_host}}:{{site.webservice_port}}/api/host/{{host.id}} -H "Content-type: application/json" -d '{"local_boot": 1}' -X "PUT"
curl http://{{site.webservice_host}}:{{site.webservice_port}}/api/host/{{host.id}}/puppet_sig -X "DELETE"
