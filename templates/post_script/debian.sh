#!/bin/bash

curl -skS http://{{site.webservice_host}}:{{site.webservice_port}}/firstboot/{{host.id}} > /root/install.sh

if [ -s /root/install.sh ]; then
    chmod +x /root/install.sh
    sed -i /etc/rc.local -e 's_exit 0_/root/install.sh_'
fi

echo "{{host.hostname}}" > /etc/hostname
#curl -H 'Content-Type: application/json' http://{{site.webservice_host}}:{{site.webservice_port}}/admin/hardware/edit/{{host.id}} -d'{ "kick_id": 1 }'
