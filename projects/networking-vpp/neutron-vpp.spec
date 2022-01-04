%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%global modulename networking_vpp
%global servicename networking-vpp
%global type L3VPP

%global common_desc This is a %{type} service plugin for Openstack Neutron (Networking) service.

%define major_version %(echo %{version} | awk 'BEGIN { FS=\".\"}; {print $1}')
%define next_version %(echo $((%{major_version} + 1)))
#%define debug_package %{nil}

Name:           openstack-%{servicename}
Version:        13.0.0
Release:        1woclouddevelop%{?dist}
Epoch:          1
Summary:        Openstack Networking %{type} plugin

License:        ASL 2.0
URL:            http://launchpad.net/neutron/
Source0:        https://tarballs.openstack.org/%{servicename}/%{servicename}-%{upstream_version}.tar.gz

#

BuildArch:      noarch
BuildRequires:  python2-devel
BuildRequires:  python-neutron >= %{epoch}:%{major_version}
BuildConflicts: python-neutron >= %{epoch}:%{next_version}
BuildRequires:  python2-pbr
BuildRequires:  git

Requires:       ipset
Requires:       iptables
Requires:       python-%{servicename} = %{epoch}:%{version}-%{release}
Requires:       openstack-neutron >= %{epoch}:%{major_version}
Conflicts:      openstack-neutron >= %{epoch}:%{next_version}

%description
%{common_desc}


%package -n python-%{servicename}
Summary:        Neutron %{type} Python libraries
Group:          Applications/System

Requires:       python-neutron >= %{epoch}:%{major_version}
Conflicts:      python-neutron >= %{epoch}:%{next_version}
Requires:       python2-alembic >= 0.8.10
Requires:       python2-eventlet
Requires:       python2-netaddr >= 0.7.18
Requires:       python-neutron-lib >= 1.18.0
Requires:       python2-oslo-config >= 2:5.2.0
Requires:       python2-oslo-db >= 4.27.0
Requires:       python2-oslo-log >= 3.36.0
Requires:       python2-oslo-messaging >= 5.29.0
Requires:       python2-oslo-privsep >= 1.23.0
Requires:       python2-oslo-service >= 1.24.0
Requires:       python2-oslo-utils >= 3.33.0
Requires:       python2-pbr
Requires:       python2-pyroute2
Requires:       python2-requests
Requires:       python2-six >= 1.10.0
Requires:       python2-sqlalchemy >= 1.0.10
Requires:       python-zmq >= 14.3.1
Requires:       python-lxml >= 4.6.3
Requires:       python2-ncclient >= 0.4.7


%description -n python-%{servicename}
%{common_desc}

This package contains the Neutron %{type} Python library.


%package -n python-%{servicename}-tests
Summary:        Neutron %{type} tests
Group:          Applications/System

Requires:       python-%{servicename} = %{epoch}:%{version}-%{release}


%description -n python-%{servicename}-tests
%{common_desc}

This package contains Neutron %{type} test files.


%prep
%autosetup -n %{servicename}-%{upstream_version} -S git

# Let's handle dependencies ourselves
%py_req_cleanup

# Kill egg-info in order to generate new SOURCES.txt
rm -rf %{modulename}.egg-info

%build
export PBR_VERSION=%{version}
export SKIP_PIP_INSTALL=1
%{__python2} setup.py build

%install
export PBR_VERSION=%{version}
export SKIP_PIP_INSTALL=1
%{__python2} setup.py install -O1 --skip-build --root %{buildroot}

# Create fake egg-info for the tempest plugin
%py2_entrypoint %{modulename} %{servicename}

# Move config files to proper location
install -d -m 755 %{buildroot}%{_sysconfdir}/neutron

# The generated config files are not moved automatically by setup.py
mv etc/neutron/networking_vpp.ini %{buildroot}%{_sysconfdir}/neutron

# Create and populate distribution configuration directory for VPP agent
mkdir -p %{buildroot}%{_datadir}/neutron/server
ln -s %{_sysconfdir}/neutron/networking_vpp.ini %{buildroot}%{_datadir}/neutron/server/networking_vpp.conf

%files
%license LICENSE
%{_bindir}/neutron-vpp-manage
%doc AUTHORS CONTRIBUTING.rst README.rst
%config(noreplace) %attr(0640, root, neutron) %{_sysconfdir}/neutron/networking_vpp.ini
%{_datadir}/neutron/server/networking_vpp.conf

%files -n python-%{servicename}
%{python2_sitelib}/%{modulename}
%{python2_sitelib}/%{modulename}-%{version}-py%{python2_version}.egg-info
%exclude %{python2_sitelib}/%{modulename}/tests

%files -n python-%{servicename}-tests
%{python2_sitelib}/%{modulename}/tests
%{python2_sitelib}/%{modulename}_tests.egg-info


%changelog




