install

# Forces the text installer to be used
text
#cmdline

# Specifies the system language
lang en_US

# Specifies the keyboard layout
keyboard us

# Skips the display of any GUI during install
skipx

# Specifies where the install files are located
# FIXME(shep): this will default to mirror.rackspace.com if not set
#    should probably define a general case mirror url
url --url http://{{ ubuntu_mirror }}/centos/6.4/os/x86_64

# configure the network for dhcp
network --onboot yes --bootproto dhcp --noipv6 yes --hostname {{ host.hostname }}

# Set the root password
rootpw --iscrypted {{ root_cryptpw }}

# Create a non-privileged user account
user --name={{ default_username }} --iscrypted --password={{ default_cryptpw }}

# Disable the default firewall rules
firewall --disabled

# Setup security
authconfig --enableshadow --passalgo=sha512

# Configure SELinux level
selinux --disabled

# Set the timezone
# FIXME(shep): should probably be US/Central
timezone --utc America/Chicago

# Create the bootloader in the MBR
bootloader --location=mbr --append=""

# Wipe all partitions and build them with the info below
clearpart --all --initlabel

# Disk partitioning info
zerombr

# Create primary partitions
part /boot --fstype ext3 --size=500 --asprimary --ondisk={{ install_drive }}
part swap --size=4096 --asprimary --ondisk={{ install_drive }}
part / --fstype=ext4 --asprimary --size=10240 --grow --ondisk={{ install_drive }}

# Reboot when installed
reboot

# Disable firstboot
firsboot --disable

# Install the Core software packages, aka "minimal"
%packages --excludedocs
@core
bash
wget
curl
%end

#%pre --log=/tmp/pre-install.log
#%end

%post --log=/tmp/post-install.log
##########
echo "Configuring sudo access for {{ default_username }}"
echo "{{ default_username }}            ALL=(ALL)       NOPASSWD: ALL" > /etc/sudoers.d/{{ default_username }}
##########

##########
echo "Grabing the post_script from djeep"
curl -skS http://{{site.webservice_host}}:{{site.webservice_port}}/post_script/{{host.id}} | bash
##########
%end
