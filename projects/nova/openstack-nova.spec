%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%global with_doc 0
%global with_trans %{!?_without_trans:1}%{?_without_trans:0}
%global distro     RDO

%global common_desc \
OpenStack Compute (codename Nova) is open source software designed to \
provision and manage large networks of virtual machines, creating a \
redundant and scalable cloud computing platform. It gives you the \
software, control panels, and APIs required to orchestrate a cloud, \
including running instances, managing networks, and controlling access \
through users and projects. OpenStack Compute strives to be both \
hardware and hypervisor agnostic, currently supporting a variety of \
standard hardware configurations and seven major hypervisors.

Name:             openstack-nova
# Liberty semver reset
# https://review.openstack.org/#/q/I6a35fa0dda798fad93b804d00a46af80f08d475c,n,z
Epoch:            1
Version:          18.7.0
Release:          1woclouddevelop%{?dist}
Summary:          OpenStack Compute (nova)

License:          ASL 2.0
URL:              http://openstack.org/projects/compute/
Source0:          https://tarballs.openstack.org/nova/nova-%{upstream_version}.tar.gz

#

Source1:          nova-dist.conf
Source6:          nova.logrotate

Source10:         openstack-nova-api.service
Source12:         openstack-nova-compute.service
Source13:         openstack-nova-network.service
Source15:         openstack-nova-scheduler.service
Source18:         openstack-nova-xvpvncproxy.service
Source19:         openstack-nova-console.service
Source20:         openstack-nova-consoleauth.service
Source25:         openstack-nova-metadata-api.service
Source26:         openstack-nova-conductor.service
Source27:         openstack-nova-cells.service
Source28:         openstack-nova-spicehtml5proxy.service
Source29:         openstack-nova-novncproxy.service
Source31:         openstack-nova-serialproxy.service
Source32:         openstack-nova-os-compute-api.service

Source22:         nova-ifc-template
Source24:         nova-sudoers
Source30:         openstack-nova-novncproxy.sysconfig
Source33:         nova-placement-api.conf
Source34:         policy.json

Source35:         nova_migration-sudoers
Source36:         nova-ssh-config
Source37:         nova-migration-wrapper
Source38:         nova_migration_identity
Source39:         nova_migration_authorized_keys
Source40:         nova_migration-rootwrap.conf
Source41:         nova_migration-rootwrap_cold_migration

BuildArch:        noarch
BuildRequires:    openstack-macros
BuildRequires:    intltool
BuildRequires:    python2-devel
BuildRequires:    git
BuildRequires:    python2-sphinx
BuildRequires:    python2-oslo-cache
#BuildRequires:    python2-openstackdocstheme
BuildRequires:    python2-os-traits
BuildRequires:    python2-setuptools
BuildRequires:    python2-netaddr
BuildRequires:    python2-pbr
BuildRequires:    python-d2to1
BuildRequires:    python2-six
BuildRequires:    python2-oslo-i18n
BuildRequires:    python2-cryptography >= 2.1
BuildRequires:    python2-oslo-policy
# Required for unit tests
BuildRequires:    python2-barbicanclient
BuildRequires:    python-ddt
BuildRequires:    python2-ironicclient
BuildRequires:    python2-mox3
BuildRequires:    python2-os-testr
BuildRequires:    python2-os-vif
BuildRequires:    python2-oslo-rootwrap
BuildRequires:    python2-oslotest
BuildRequires:    python2-osprofiler
BuildRequires:    python-requests-mock
BuildRequires:    python2-subunit
BuildRequires:    python2-testrepository
BuildRequires:    python2-testresources
BuildRequires:    python2-testscenarios
BuildRequires:    python2-tooz
BuildRequires:    python2-oslo-vmware
BuildRequires:    python2-cursive
BuildRequires:    python2-os-service-types
# Required by build_sphinx for man and doc building
#BuildRequires:    python2-sphinxcontrib-actdiag
#BuildRequires:    python2-sphinxcontrib-seqdiag

Requires:         openstack-nova-compute = %{epoch}:%{version}-%{release}
Requires:         openstack-nova-scheduler = %{epoch}:%{version}-%{release}
Requires:         openstack-nova-api = %{epoch}:%{version}-%{release}
Requires:         openstack-nova-network = %{epoch}:%{version}-%{release}
Requires:         openstack-nova-conductor = %{epoch}:%{version}-%{release}
Requires:         openstack-nova-console = %{epoch}:%{version}-%{release}
Requires:         openstack-nova-cells = %{epoch}:%{version}-%{release}
Requires:         openstack-nova-novncproxy = %{epoch}:%{version}-%{release}
Requires:         openstack-nova-placement-api = %{epoch}:%{version}-%{release}
Requires:         openstack-nova-migration = %{epoch}:%{version}-%{release}


%description
%{common_desc}

%package common
Summary:          Components common to all OpenStack Nova services
Obsoletes:        openstack-nova-cert <= 1:16.0.0-1

Requires:         python-nova = %{epoch}:%{version}-%{release}
%{?systemd_requires}
Requires(pre):    shadow-utils
BuildRequires:    systemd
# Required to build nova.conf.sample
BuildRequires:    python2-castellan >= 0.16.0
BuildRequires:    python2-glanceclient
BuildRequires:    python2-keystonemiddleware
BuildRequires:    python-lxml
BuildRequires:    python2-microversion-parse >= 0.2.1
BuildRequires:    python2-os-brick
BuildRequires:    python2-oslo-db
BuildRequires:    python2-oslo-reports
BuildRequires:    python2-oslo-service
BuildRequires:    python2-oslo-versionedobjects
BuildRequires:    python2-paramiko
BuildRequires:    python-websockify
# Required to compile translation files
BuildRequires:    python2-babel

# remove old service subpackage
Obsoletes: %{name}-objectstore


%description common
%{common_desc}

This package contains scripts, config and dependencies shared
between all the OpenStack nova services.


%package compute
Summary:          OpenStack Nova Virtual Machine control service

Requires:         openstack-nova-common = %{epoch}:%{version}-%{release}
Requires:         curl
Requires:         iscsi-initiator-utils
Requires:         iptables
Requires:         iptables-services
Requires:         ipmitool
Requires:         python-libguestfs
Requires:         libvirt-python
Requires:         libvirt-daemon-kvm
Requires:         /usr/bin/virsh
%if 0%{?rhel}==0
Requires:         libvirt-daemon-lxc
%endif
Requires:         openssh-clients
Requires:         rsync
Requires:         lvm2
Requires:         python2-cinderclient >= 3.3.0
Requires:         genisoimage
# Ensure that the _right_ versions of QEMU binary and libvirt are
# shipped based on distribution.
%if 0%{?fedora}
Requires(pre): qemu-kvm >= 2.10.0
Requires(pre): libvirt-python >= 3.9.0
Requires(pre): libvirt-daemon-kvm >= 3.9.0
%endif
# NOTE-1: CentOS package is called 'qemu-kvm-ev', but it has a
#         compatiblity "Provides: qemu-kvm-rhev", so it'll do the right
#         thing, that's why we're not special-casing CentOS here.
# NOTE-2: Explicitly conditionalize on RHEL-7, as we have to
#         re-evaluate the QEMU and libvirt version strings for each RHOS
#         / RHEL release.
# NOTE-3: We're using "Requires(pre)" (instead of "Requires") as a
#         safety check -- to guarantee when Nova, in the %pre" section,
#         adds the 'nova' user to the 'qemu' and 'libvirt' groups, those
#         groups are guaranteed to exist.
%if 0%{?rhel} == 7
Requires(pre): qemu-kvm-rhev >= 2.10.0
Requires(pre): libvirt-python >= 3.9.0
Requires(pre): libvirt-daemon-kvm >= 3.9.0
%endif
Requires:         bridge-utils
Requires:         sg3_utils
Requires:         sysfsutils
Requires:         libosinfo

%description compute
%{common_desc}

This package contains the Nova service for controlling Virtual Machines.


%package network
Summary:          OpenStack Nova Network control service

Requires:         openstack-nova-common = %{epoch}:%{version}-%{release}
Requires:         radvd
Requires:         bridge-utils
Requires:         dnsmasq
Requires:         dnsmasq-utils
Requires:         ebtables
Requires:         conntrack-tools

%description network
%{common_desc}

This package contains the Nova service for controlling networking.


%package scheduler
Summary:          OpenStack Nova VM distribution service

Requires:         openstack-nova-common = %{epoch}:%{version}-%{release}

%description scheduler
%{common_desc}

This package contains the service for scheduling where
to run Virtual Machines in the cloud.


%package api
Summary:          OpenStack Nova API services

Requires:         openstack-nova-common = %{epoch}:%{version}-%{release}
Requires:         python2-cinderclient >= 3.3.0

%description api
%{common_desc}

This package contains the Nova services providing programmatic access.

%package conductor
Summary:          OpenStack Nova Conductor services

Requires:         openstack-nova-common = %{epoch}:%{version}-%{release}

%description conductor
%{common_desc}

This package contains the Nova services providing database access for
the compute service

%package console
Summary:          OpenStack Nova console access services

Requires:         openstack-nova-common = %{epoch}:%{version}-%{release}
Requires:         python-websockify >= 0.8.0

%description console
%{common_desc}

This package contains the Nova services providing
console access services to Virtual Machines.

%package cells
Summary:          OpenStack Nova Cells services

Requires:         openstack-nova-common = %{epoch}:%{version}-%{release}

%description cells
%{common_desc}

This package contains the Nova Cells service providing additional
scaling and (geographic) distribution for compute services.

%package novncproxy
Summary:          OpenStack Nova noVNC proxy service

Requires:         openstack-nova-common = %{epoch}:%{version}-%{release}
Requires:         novnc
Requires:         python-websockify >= 0.8.0


%description novncproxy
%{common_desc}

This package contains the Nova noVNC Proxy service that can proxy
VNC traffic over browser websockets connections.

%package spicehtml5proxy
Summary:          OpenStack Nova Spice HTML5 console access service

Requires:         openstack-nova-common = %{epoch}:%{version}-%{release}
Requires:         python-websockify >= 0.8.0

%description spicehtml5proxy
%{common_desc}

This package contains the Nova services providing the
spice HTML5 console access service to Virtual Machines.

%package serialproxy
Summary:          OpenStack Nova serial console access service

Requires:         openstack-nova-common = %{epoch}:%{version}-%{release}
Requires:         python-websockify >= 0.8.0

%description serialproxy
%{common_desc}

This package contains the Nova services providing the
serial console access service to Virtual Machines.

%package placement-api
Summary:          OpenStack Nova Placement APIservice

Requires:         openstack-nova-common = %{epoch}:%{version}-%{release}
Requires:         httpd
Requires:         mod_wsgi

%description placement-api
%{common_desc}

This package contains the Nova placement service, which will initially
allow for the management of resource providers.

%package migration
Summary:          OpenStack Nova Migration

Requires:         openstack-nova-compute = %{epoch}:%{version}-%{release}

%description migration
%{common_desc}

This package contains scripts and config to support VM migration in Nova.

%package -n       python-nova
Summary:          Nova Python libraries

Requires:         openssl
# Require openssh for ssh-keygen
Requires:         openssh
Requires:         sudo

Requires:         python2-paramiko >= 2.0.0

Requires:         python-decorator >= 3.4.0
Requires:         python-enum34
Requires:         python2-eventlet >= 0.18.2
Requires:         python2-iso8601 >= 0.1.11
Requires:         python2-netaddr >= 0.7.18
Requires:         python-lxml >= 3.2.1
Requires:         python2-boto
Requires:         python-ldap
Requires:         python2-stevedore >= 1.20.0

Requires:         python-memcached

Requires:         python2-sqlalchemy >= 1.0.10
Requires:         python-migrate >= 0.11.0
Requires:         python2-alembic >= 0.8.0

Requires:         python-paste
Requires:         python-paste-deploy >= 1.5.0
Requires:         python2-routes >= 2.3.1
Requires:         python-webob >= 1.8.2

Requires:         python2-babel >= 2.3.4
Requires:         python2-castellan >= 0.16.0
Requires:         python2-cryptography >= 2.1
Requires:         python2-cursive >= 0.2.1
Requires:         python2-glanceclient >= 1:2.8.0
Requires:         python2-greenlet >= 0.4.10
Requires:         python2-keystonemiddleware >= 4.17.0
Requires:         python2-keystoneauth1 >= 3.9.0
Requires:         python2-jinja2
Requires:         python2-jsonschema >= 2.6.0
Requires:         python2-microversion-parse >= 0.2.1
Requires:         python-netifaces >= 0.10.4
Requires:         python2-neutronclient >= 6.7.0
Requires:         python2-novaclient >= 2.30.1
Requires:         python2-os-brick >= 2.5.0
Requires:         python2-os-traits >= 0.9.1
Requires:         python2-oslo-cache >= 1.26.0
Requires:         python2-oslo-concurrency >= 3.26.0
Requires:         python2-oslo-config >= 2:6.1.0
Requires:         python2-oslo-context >= 2.19.2
Requires:         python2-oslo-db >= 4.40.0
Requires:         python2-oslo-i18n >= 3.15.3
Requires:         python2-oslo-log >= 3.36.0
Requires:         python2-oslo-messaging >= 6.3.0
Requires:         python2-oslo-middleware >= 3.31.0
Requires:         python2-oslo-policy >= 1.35.0
Requires:         python2-oslo-privsep >= 1.23.0
Requires:         python2-oslo-reports >= 1.18.0
Requires:         python2-oslo-rootwrap >= 5.8.0
Requires:         python2-oslo-serialization >= 2.18.0
Requires:         python2-oslo-service >= 1.24.0
Requires:         python2-oslo-utils >= 3.33.0
Requires:         python2-oslo-versionedobjects >= 1.31.2
Requires:         python2-os-vif >= 1.7.0
Requires:         python2-oslo-vmware >= 1.16.0
Requires:         python2-pbr
Requires:         python2-prettytable >= 0.7.1
Requires:         python2-psutil
Requires:         python2-requests >= 2.14.2
Requires:         python2-rfc3986 >= 0.3.1
Requires:         python2-six >= 1.10.0
Requires:         python2-taskflow >= 2.16.0
Requires:         python2-tooz >= 1.58.0
Requires:         python2-os-service-types >= 1.2.0
Requires:         python2-futures >= 3.0.0
Requires:         python2-dateutil >= 2.5.3

%description -n   python-nova
%{common_desc}

This package contains the nova Python library.

%package -n python-nova-tests
Summary:        Nova tests
Requires:       openstack-nova = %{epoch}:%{version}-%{release}

%description -n python-nova-tests
%{common_desc}

This package contains the nova Python library.

%if 0%{?with_doc}
%package doc
Summary:          Documentation for OpenStack Compute

BuildRequires:    graphviz

# Required to build module documents
BuildRequires:    python2-boto
BuildRequires:    python2-eventlet
BuildRequires:    python2-barbicanclient
BuildRequires:    python2-cinderclient
BuildRequires:    python2-keystoneclient
BuildRequires:    python2-neutronclient
BuildRequires:    python2-os-win
BuildRequires:    python2-oslo-config
BuildRequires:    python2-oslo-log
BuildRequires:    python2-oslo-messaging
BuildRequires:    python2-oslo-utils
BuildRequires:    python-redis
BuildRequires:    python2-rfc3986 >= 0.3.1
BuildRequires:    python2-routes
BuildRequires:    python2-sphinxcontrib-actdiag
BuildRequires:    python2-sphinxcontrib-seqdiag
BuildRequires:    python2-sqlalchemy
BuildRequires:    python-webob
BuildRequires:    python-zmq
# while not strictly required, quiets the build down when building docs.
BuildRequires:    python-migrate, python-iso8601

%description      doc
%{common_desc}

This package contains documentation files for nova.
%endif

%prep
%autosetup -n nova-%{upstream_version} -S git

find . \( -name .gitignore -o -name .placeholder \) -delete

find nova -name \*.py -exec sed -i '/\/usr\/bin\/env python/{d;q}' {} +

# Remove the requirements file so that pbr hooks don't add it
# to distutils requiers_dist config
%py_req_cleanup

%build
PYTHONPATH=. oslo-config-generator --config-file=etc/nova/nova-config-generator.conf
# Generate a sample policy.yaml file for documentation purposes only
PYTHONPATH=. oslopolicy-sample-generator --config-file=etc/nova/nova-policy-generator.conf

%{__python2} setup.py build

# Generate i18n files
# (amoralej) we can remove '-D nova' once https://review.openstack.org/#/c/439500/ is merged
%{__python2} setup.py compile_catalog -d build/lib/nova/locale -D nova

# Avoid http://bugzilla.redhat.com/1059815. Remove when that is closed
sed -i 's|group/name|group;name|; s|\[DEFAULT\]/|DEFAULT;|' etc/nova/nova.conf.sample

# Programmatically update defaults in sample config
# which is installed at /etc/nova/nova.conf

#  First we ensure all values are commented in appropriate format.
#  Since icehouse, there was an uncommented keystone_authtoken section
#  at the end of the file which mimics but also conflicted with our
#  distro editing that had been done for many releases.
sed -i '/^[^#[]/{s/^/#/; s/ //g}; /^#[^ ]/s/ = /=/' etc/nova/nova.conf.sample

#  TODO: Make this more robust
#  Note it only edits the first occurrence, so assumes a section ordering in sample
#  and also doesn't support multi-valued variables like dhcpbridge_flagfile.
while read name eq value; do
  test "$name" && test "$value" || continue
  sed -i "0,/^# *$name=/{s!^# *$name=.*!#$name=$value!}" etc/nova/nova.conf.sample
done < %{SOURCE1}

%install
%{__python2} setup.py install -O1 --skip-build --root %{buildroot}

export PYTHONPATH=.
%if 0%{?with_doc}
sphinx-build -b html doc/source doc/build/html
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%if 0%{?with_doc}
sphinx-build -b man doc/source doc/build/man
mkdir -p %{buildroot}%{_mandir}/man1
install -p -D -m 644 doc/build/man/*.1 %{buildroot}%{_mandir}/man1/
%endif

# Setup directories
install -d -m 755 %{buildroot}%{_sharedstatedir}/nova
install -d -m 755 %{buildroot}%{_sharedstatedir}/nova/buckets
install -d -m 755 %{buildroot}%{_sharedstatedir}/nova/instances
install -d -m 755 %{buildroot}%{_sharedstatedir}/nova/keys
install -d -m 755 %{buildroot}%{_sharedstatedir}/nova/networks
install -d -m 755 %{buildroot}%{_sharedstatedir}/nova/tmp
install -d -m 750 %{buildroot}%{_localstatedir}/log/nova
install -d -m 700 %{buildroot}%{_sharedstatedir}/nova/.ssh

# Install config files
install -d -m 755 %{buildroot}%{_sysconfdir}/nova
install -p -D -m 640 %{SOURCE1} %{buildroot}%{_datarootdir}/nova/nova-dist.conf
install -p -D -m 640 etc/nova/nova.conf.sample  %{buildroot}%{_sysconfdir}/nova/nova.conf
install -p -D -m 640 etc/nova/rootwrap.conf %{buildroot}%{_sysconfdir}/nova/rootwrap.conf
install -p -D -m 640 etc/nova/api-paste.ini %{buildroot}%{_sysconfdir}/nova/api-paste.ini
install -p -D -m 640 %{SOURCE33} %{buildroot}%{_sysconfdir}/httpd/conf.d/00-nova-placement-api.conf
install -d -m 755 %{buildroot}%{_sysconfdir}/nova/migration
install -p -D -m 600 %{SOURCE38} %{buildroot}%{_sysconfdir}/nova/migration/identity
install -p -D -m 644 %{SOURCE39} %{buildroot}%{_sysconfdir}/nova/migration/authorized_keys
install -p -D -m 640 %{SOURCE40} %{buildroot}%{_sysconfdir}/nova/migration/rootwrap.conf
install -d -m 755 %{buildroot}%{_sysconfdir}/nova/migration/rootwrap.d
install -p -D -m 640 %{SOURCE41} %{buildroot}%{_sysconfdir}/nova/migration/rootwrap.d/cold_migration.filters

# Install empty policy.json file to cover rpm updates with untouched policy files.
install -p -D -m 640 %{SOURCE34} %{buildroot}%{_sysconfdir}/nova/policy.json

# Install version info file
cat > %{buildroot}%{_sysconfdir}/nova/release <<EOF
[Nova]
vendor = %{distro}
product = OpenStack Compute
package = %{release}
EOF

# Install initscripts for Nova services
install -p -D -m 644 %{SOURCE10} %{buildroot}%{_unitdir}/openstack-nova-api.service
install -p -D -m 644 %{SOURCE12} %{buildroot}%{_unitdir}/openstack-nova-compute.service
install -p -D -m 644 %{SOURCE13} %{buildroot}%{_unitdir}/openstack-nova-network.service
install -p -D -m 644 %{SOURCE15} %{buildroot}%{_unitdir}/openstack-nova-scheduler.service
install -p -D -m 644 %{SOURCE18} %{buildroot}%{_unitdir}/openstack-nova-xvpvncproxy.service
install -p -D -m 644 %{SOURCE19} %{buildroot}%{_unitdir}/openstack-nova-console.service
install -p -D -m 644 %{SOURCE20} %{buildroot}%{_unitdir}/openstack-nova-consoleauth.service
install -p -D -m 644 %{SOURCE25} %{buildroot}%{_unitdir}/openstack-nova-metadata-api.service
install -p -D -m 644 %{SOURCE26} %{buildroot}%{_unitdir}/openstack-nova-conductor.service
install -p -D -m 644 %{SOURCE27} %{buildroot}%{_unitdir}/openstack-nova-cells.service
install -p -D -m 644 %{SOURCE28} %{buildroot}%{_unitdir}/openstack-nova-spicehtml5proxy.service
install -p -D -m 644 %{SOURCE29} %{buildroot}%{_unitdir}/openstack-nova-novncproxy.service
install -p -D -m 644 %{SOURCE31} %{buildroot}%{_unitdir}/openstack-nova-serialproxy.service
install -p -D -m 644 %{SOURCE32} %{buildroot}%{_unitdir}/openstack-nova-os-compute-api.service

# Install sudoers
install -p -D -m 440 %{SOURCE24} %{buildroot}%{_sysconfdir}/sudoers.d/nova
install -p -D -m 440 %{SOURCE35} %{buildroot}%{_sysconfdir}/sudoers.d/nova_migration

# Install nova ssh client config for migration
install -p -D -m 600 %{SOURCE36} %{buildroot}%{_sharedstatedir}/nova/.ssh/config

# Install nova migration ssh wrapper command
install -p -D -m 755 %{SOURCE37} %{buildroot}%{_bindir}/nova-migration-wrapper

# Install logrotate
install -p -D -m 644 %{SOURCE6} %{buildroot}%{_sysconfdir}/logrotate.d/openstack-nova

# Install pid directory
install -d -m 755 %{buildroot}%{_localstatedir}/run/nova

# Install template files
install -p -D -m 644 %{SOURCE22} %{buildroot}%{_datarootdir}/nova/interfaces.template

# Install rootwrap files in /usr/share/nova/rootwrap
mkdir -p %{buildroot}%{_datarootdir}/nova/rootwrap/
install -p -D -m 644 etc/nova/rootwrap.d/* %{buildroot}%{_datarootdir}/nova/rootwrap/

# Install novncproxy service options template
install -d %{buildroot}%{_sysconfdir}/sysconfig
install -p -m 0644 %{SOURCE30} %{buildroot}%{_sysconfdir}/sysconfig/openstack-nova-novncproxy

# Install i18n .mo files (.po and .pot are not required)
install -d -m 755 %{buildroot}%{_datadir}
rm -f %{buildroot}%{python2_sitelib}/nova/locale/*/LC_*/nova*po
rm -f %{buildroot}%{python2_sitelib}/nova/locale/*pot
mv %{buildroot}%{python2_sitelib}/nova/locale %{buildroot}%{_datadir}/locale

# Find language files
%find_lang nova --all-name

# Remove unneeded in production stuff
rm -f %{buildroot}%{_bindir}/nova-debug
rm -fr %{buildroot}%{python2_sitelib}/run_tests.*
rm -f %{buildroot}%{_bindir}/nova-combined
rm -f %{buildroot}/usr/share/doc/nova/README*

# Remove duplicated configuration files deployed at /usr/etc
rm -rf %{buildroot}%{_prefix}/etc/nova

# FIXME(jpena): unit tests are taking too long in the current DLRN infra
# Until we have a better architecture, let's not run them when under DLRN
%if 0%{!?dlrn}
%check
# create a fake os_xenapi with just enough to load the unit tests
mkdir -p os_xenapi

touch os_xenapi/__init__.py

cat > os_xenapi/client.py <<EOF
class session:
    def XenAPISession():
        pass
XenAPI = None
exception = None
EOF

# Limit the number of concurrent workers to 2
OS_TEST_PATH=./nova/tests/unit ostestr -c 2 --black-regex 'xenapi|test_compute_xen'
rm -rf os_xenapi
%endif

%pre common
getent group nova >/dev/null || groupadd -r nova --gid 162
if ! getent passwd nova >/dev/null; then
  useradd -u 162 -r -g nova -G nova,nobody -d %{_sharedstatedir}/nova -s /sbin/nologin -c "OpenStack Nova Daemons" nova
fi
exit 0

%pre compute
usermod -a -G qemu nova
usermod -a -G libvirt nova
%pre migration
getent group nova_migration >/dev/null || groupadd -r nova_migration
getent passwd nova_migration >/dev/null || \
    useradd -r -g nova_migration -d / -s /bin/bash -c "OpenStack Nova Migration" nova_migration
exit 0

%post compute
%systemd_post %{name}-compute.service
%post network
%systemd_post %{name}-network.service
%post scheduler
%systemd_post %{name}-scheduler.service
%post api
%systemd_post %{name}-api.service %{name}-metadata-api.service %{name}-os-compute-api.service
%post conductor
%systemd_post %{name}-conductor.service
%post console
%systemd_post %{name}-console.service %{name}-consoleauth.service %{name}-xvpvncproxy.service
%post cells
%systemd_post %{name}-cells.service
%post novncproxy
%systemd_post %{name}-novncproxy.service
%post spicehtml5proxy
%systemd_post %{name}-spicehtml5proxy.service
%post serialproxy
%systemd_post %{name}-serialproxy.service

%preun compute
%systemd_preun %{name}-compute.service
%preun network
%systemd_preun %{name}-network.service
%preun scheduler
%systemd_preun %{name}-scheduler.service
%preun api
%systemd_preun %{name}-api.service %{name}-metadata-api.service %{name}-os-compute-api.service
%preun conductor
%systemd_preun %{name}-conductor.service
%preun console
%systemd_preun %{name}-console.service %{name}-consoleauth.service %{name}-xvpvncproxy.service
%preun cells
%systemd_preun %{name}-cells.service
%preun novncproxy
%systemd_preun %{name}-novncproxy.service
%preun spicehtml5proxy
%systemd_preun %{name}-spicehtml5proxy.service
%preun serialproxy
%systemd_preun %{name}-serialproxy.service

%postun compute
%systemd_postun_with_restart %{name}-compute.service
%postun network
%systemd_postun_with_restart %{name}-network.service
%postun scheduler
%systemd_postun_with_restart %{name}-scheduler.service
%postun api
%systemd_postun_with_restart %{name}-api.service %{name}-metadata-api.service %{name}-os-compute-api.service
%postun conductor
%systemd_postun_with_restart %{name}-conductor.service
%postun console
%systemd_postun_with_restart %{name}-console.service %{name}-consoleauth.service %{name}-xvpvncproxy.service
%postun cells
%systemd_postun_with_restart %{name}-cells.service
%postun novncproxy
%systemd_postun_with_restart %{name}-novncproxy.service
%postun spicehtml5proxy
%systemd_postun_with_restart %{name}-spicehtml5proxy.service
%postun serialproxy
%systemd_postun_with_restart %{name}-serialproxy.service

%files

%files common -f nova.lang
%license LICENSE
%doc etc/nova/policy.yaml.sample
%dir %{_datarootdir}/nova
%attr(-, root, nova) %{_datarootdir}/nova/nova-dist.conf
%{_datarootdir}/nova/interfaces.template
%{_datarootdir}/nova/rootwrap/network.filters
%dir %{_sysconfdir}/nova
%{_sysconfdir}/nova/release
%config(noreplace) %attr(-, root, nova) %{_sysconfdir}/nova/nova.conf
%config(noreplace) %attr(-, root, nova) %{_sysconfdir}/nova/api-paste.ini
%config(noreplace) %attr(-, root, nova) %{_sysconfdir}/nova/rootwrap.conf
%config(noreplace) %attr(-, root, nova) %{_sysconfdir}/nova/policy.json
%config(noreplace) %{_sysconfdir}/logrotate.d/openstack-nova
%config(noreplace) %{_sysconfdir}/sudoers.d/nova

%dir %attr(0750, nova, root) %{_localstatedir}/log/nova
%dir %attr(0755, nova, root) %{_localstatedir}/run/nova

%{_bindir}/nova-manage
%{_bindir}/nova-policy
%{_bindir}/nova-rootwrap
%{_bindir}/nova-rootwrap-daemon
%{_bindir}/nova-status

%if 0%{?with_doc}
%{_mandir}/man1/nova*.1.gz
%endif

%defattr(-, nova, nova, -)
%dir %{_sharedstatedir}/nova
%dir %{_sharedstatedir}/nova/buckets
%dir %{_sharedstatedir}/nova/instances
%dir %{_sharedstatedir}/nova/keys
%dir %{_sharedstatedir}/nova/networks
%dir %{_sharedstatedir}/nova/tmp

%files compute
%{_bindir}/nova-compute
%{_unitdir}/openstack-nova-compute.service
%{_datarootdir}/nova/rootwrap/compute.filters

%files network
%{_bindir}/nova-network
%{_bindir}/nova-dhcpbridge
%{_unitdir}/openstack-nova-network.service

%files scheduler
%{_bindir}/nova-scheduler
%{_unitdir}/openstack-nova-scheduler.service

%files api
%{_bindir}/nova-api*
%{_bindir}/nova-metadata-wsgi
%{_unitdir}/openstack-nova-*api.service
%{_datarootdir}/nova/rootwrap/api-metadata.filters

%files conductor
%{_bindir}/nova-conductor
%{_unitdir}/openstack-nova-conductor.service

%files console
%{_bindir}/nova-console*
%{_bindir}/nova-xvpvncproxy
%{_unitdir}/openstack-nova-console*.service
%{_unitdir}/openstack-nova-xvpvncproxy.service

%files cells
%{_bindir}/nova-cells
%{_unitdir}/openstack-nova-cells.service

%files novncproxy
%{_bindir}/nova-novncproxy
%{_unitdir}/openstack-nova-novncproxy.service
%config(noreplace) %{_sysconfdir}/sysconfig/openstack-nova-novncproxy

%files spicehtml5proxy
%{_bindir}/nova-spicehtml5proxy
%{_unitdir}/openstack-nova-spicehtml5proxy.service

%files serialproxy
%{_bindir}/nova-serialproxy
%{_unitdir}/openstack-nova-serialproxy.service

%files placement-api
%config(noreplace) %{_sysconfdir}/httpd/conf.d/00-nova-placement-api.conf
%{_bindir}/nova-placement-api

%files migration
%{_bindir}/nova-migration-wrapper
%config(noreplace) %{_sysconfdir}/sudoers.d/nova_migration
%dir %attr(0700, nova, nova) %{_sharedstatedir}/nova/.ssh
%attr(0600, nova, nova) %{_sharedstatedir}/nova/.ssh/config
%dir %{_sysconfdir}/nova/migration
%config(noreplace) %attr(0640, root, nova_migration) %{_sysconfdir}/nova/migration/authorized_keys
%config(noreplace) %attr(0600, nova, nova) %{_sysconfdir}/nova/migration/identity
%config(noreplace) %attr(0640, root, root) %{_sysconfdir}/nova/migration/rootwrap.conf
%dir %{_sysconfdir}/nova/migration/rootwrap.d
%config(noreplace) %attr(0640, root, root) %{_sysconfdir}/nova/migration/rootwrap.d/cold_migration.filters

%files -n python-nova
%license LICENSE
%{python2_sitelib}/nova
%{python2_sitelib}/nova-*.egg-info
%exclude %{python2_sitelib}/nova/tests

%files -n python-nova-tests
%license LICENSE
%{python2_sitelib}/nova/tests

%if 0%{?with_doc}
%files doc
%license LICENSE
%doc doc/build/html
%endif

%changelog
* Thu Oct 10 2019 RDO <dev@lists.rdoproject.org> 1:18.2.3-1
- Update to 18.2.3

* Mon Aug 12 2019 RDO <dev@lists.rdoproject.org> 1:18.2.2-1
- Update to 18.2.2

* Tue Jun 18 2019 RDO <dev@lists.rdoproject.org> 1:18.2.1-1
- Update to 18.2.1

* Sun Mar 24 2019 RDO <dev@lists.rdoproject.org> 1:18.2.0-1
- Update to 18.2.0

* Wed Dec 19 2018 RDO <dev@lists.rdoproject.org> 1:18.1.0-1
- Update to 18.1.0

* Tue Nov 06 2018 RDO <dev@lists.rdoproject.org> 1:18.0.3-1
- Update to 18.0.3

* Mon Oct 08 2018 RDO <dev@lists.rdoproject.org> 1:18.0.2-1
- Update to 18.0.2

* Mon Sep 24 2018 RDO <dev@lists.rdoproject.org> 1:18.0.1-1
- Update to 18.0.1

* Wed Sep 19 2018 RDO <dev@lists.rdoproject.org> 1:18.0.0-2
- Update python2-oslo-db requirement to 4.40.0 or later

* Thu Aug 30 2018 RDO <dev@lists.rdoproject.org> 1:18.0.0-1
- Update to 18.0.0

* Fri Aug 24 2018 RDO <dev@lists.rdoproject.org> 1:18.0.0-0.3.0rc2
- Update to 18.0.0.0rc3

* Thu Aug 23 2018 RDO <dev@lists.rdoproject.org> 1:18.0.0-0.2.0rc1
- Update to 18.0.0.0rc2

* Thu Aug 16 2018 RDO <dev@lists.rdoproject.org> 1:18.0.0-0.1.0rc1
- Update to 18.0.0.0rc1

