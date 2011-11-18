#!/bin/sh
apt-get update
apt-get -y upgrade
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
cp /opt/djeep/local/etc/puppet/puppet.conf.sample /etc/puppet/puppet.conf
sed -i 's/\/path\/to/\/opt/' /etc/puppet/puppet.conf
cd /opt/djeep
tools/with_venv.sh ./reset.sh
ln -s /etc/dnsmasq.conf /opt/djeep/local/etc/dnsmasq.conf
touch /etc/ethers
ln -s /etc/ethers /opt/djeep/local/etc/ethers
service dnsmasq restart
service puppetmaster restart
sed  -i 's/^exit 0//' /etc/rc.local 
echo 'cd /opt/djeep' >> /etc/rc.local
echo 'screen -d -m tools/with_venv.sh python manage.py runeventlet 0.0.0.0:8000' >> /etc/rc.local
screen -d -m tools/with_venv.sh python manage.py runeventlet 0.0.0.0:8000

