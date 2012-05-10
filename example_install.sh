#!/bin/sh

INSTALL_DIR=${INSTALL_DIR:-/opt}
DJEEP_DIR=${DJEEP_DIR:-${INSTALL_DIR}/djeep}

apt-get update
apt-get -y upgrade
apt-get -y install git python-virtualenv mercurial gcc python-dev puppet puppetmaster dnsmasq screen

cd ${INSTALL_DIR}
git clone git://github.com/galstrom21/djeep.git
git clone git://github.com/willkelly/openstack-puppet.git

if [ -d /etc/puppet ]; then
    mv /etc/puppet /etc/puppet.orig
fi
mv ${INSTALL_DIR}/openstack-puppet /etc/puppet

cd /etc/puppet
echo '*' > /etc/puppet/autosign.conf
git submodule init
git submodule update
cp manifests/site.pp.sample manifests/site.pp
cd -


cd ${DJEEP_DIR}
./fetch_images.sh
python tools/install_venv.py
cp ${DJEEP_DIR}/local/etc/puppet/puppet.conf.sample /etc/puppet/puppet.conf
sed -i 's/\/path\/to/\/opt/' /etc/puppet/puppet.conf

cd ${DJEEP_DIR}
tools/with_venv.sh ./reset.sh
ln -s /etc/dnsmasq.conf ${DJEEP_DIR}/local/etc/dnsmasq.conf
touch /etc/ethers
ln -s /etc/ethers ${DJEEP_DIR}/local/etc/ethers
service dnsmasq restart
service puppetmaster restart
sed  -i 's/^exit 0//' /etc/rc.local 
echo "cd ${DJEEP_DIR}" >> /etc/rc.local
echo 'screen -d -m tools/with_venv.sh python manage.py runeventlet 0.0.0.0:8000' >> /etc/rc.local
screen -d -m tools/with_venv.sh python manage.py runeventlet 0.0.0.0:8000
