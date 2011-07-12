#!/bin/sh

rm djeep.sqlite
rm -rf rolemapper/migrations
python manage.py schemamigration rolemapper --initial
python manage.py syncdb --noinput
python manage.py migrate rolemapper
python manage.py loaddata rolemapper/fixtures/openstack_roles.yaml
python manage.py loaddata rolemapper/fixtures/demo_auth.yaml
python manage.py loaddata rolemapper/fixtures/demo_data.yaml
