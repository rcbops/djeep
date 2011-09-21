#!/bin/sh
apt-get update
apt-get upgrade
apt-get -y install git python-virtualenv mercurial gcc python-dev puppet puppetmaster dns\
masq screen
git clone git://github.com/willkelly/djeep.git
git clone git://github.com/willkelly/openstack-puppet.git
mv /etc/puppet /etc/puppet.orig
mv openstack-puppet /etc/puppet

cd /etc/puppet
echo '*' > /etc/puppet/autosign.conf
git submodule init
git submodule update
cp manifests/site.pp.sample manifests/site.pp
cd -

mv djeep /opt
cd /opt/djeep
./fetch_images.sh
python tools/install_venv.py
cp /opt/djeep/etc/puppet/puppet.conf.sample /etc/puppet/puppet.conf
sed -i 's/\/path\/to/\/opt/' /etc/puppet/puppet.conf
cd /opt/djeep
tools/with_venv.sh ./reset.sh
ln -s /etc/dnsmasq.conf /opt/djeep/etc/dnsmasq.conf
touch /etc/ethers
ln -s /etc/ethers /opt/djeep/etc/ethers
service dnsmasq restart
service puppetmaster restart
screen -d -m tools/with_venv.sh python manage.py runeventlet 0.0.0.0:8000

