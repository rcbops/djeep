#!/bin/bash

echo "{{host.hostname}}" > /etc/hostname
curl http://{{site.webservice_host}}:{{site.webservice_port}}/api/host/{{host.id}} -H "Content-type: application/json" -d '{"local_boot": 1}' -X "PUT"
curl http://{{site.webservice_host}}:{{site.webservice_port}}/api/host/{{host.id}}/puppet_sig -X "DELETE"

