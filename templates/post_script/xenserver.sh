#!/bin/sh

wget http://{{site.webservice_host}}:{{site.webservice_port}}/api/host/{{host.id}} --header="Content-type: application/json" --header='X-Real-Http-Data: {"kick_target_id": 1}' --header="X-Real-Http-Method: PUT"
wget http://{{site.webservice_host}}:{{site.webservice_port}}/api/host/{{host.id}}/puppet_sig --header="X-Real-Http-Method: DELETE"
