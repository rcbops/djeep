#!/bin/bash

curl -skS http://{{site.webservice_host}}:{{site.webservice_port}}/firstboot/{{host.id}} > /root/install.sh

if [ -s /root/install.sh ]; then
    chmod +x /root/install.sh
    sed -i /etc/rc.local -e 's_exit 0_/root/install.sh_'
fi

# Add rcbops keys to authorized keys
SSH_DIR=/root/.ssh
mkdir $SSH_DIR
wget -O $SSH_DIR/authorized_keys https://raw.githubusercontent.com/rcbops/jenkins-build/master/keys/rcb.keys

{% if host.ssh_key %}
# Add specified keypair
echo "{{host.ssh_key.private_key}}" > $SSH_DIR/id_rsa
echo "{{host.ssh_key.public_key}}" > $SSH_DIR/id_rsa.pub
echo -e "\n{{host.ssh_key.public_key}}" >> $SSH_DIR/authorized_keys
chmod 600 $SSH_DIR/id_rsa
{% endif %}

echo "{{host.hostname}}" > /etc/hostname
curl http://{{site.webservice_host}}:{{site.webservice_port}}/api/host/{{host.id}} -H "Content-type: application/json" -d '{"local_boot": 1}' -X "PUT"
curl http://{{site.webservice_host}}:{{site.webservice_port}}/api/host/{{host.id}}/puppet_sig -X "DELETE"
