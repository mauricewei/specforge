%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%global modulename vpp_statistics
%global servicename vpp-statistics
%global type L3VPP

%global common_desc This is a %{type} service plugin for Openstack Neutron (vpp-statistics) service.

%define major_version %(echo %{version} | awk 'BEGIN { FS=\".\"}; {print $1}')
%define next_version %(echo $((%{major_version} + 1)))
#%define debug_package %{nil}

Name:           openstack-%{servicename}
Version:        1.0.0
Release:        1woclouddevelop%{?dist}
Epoch:          1
Summary:        Openstack Networking %{type} plugin

License:        ASL 2.0
URL:            http://launchpad.net/neutron/
Source0:        https://tarballs.openstack.org/%{servicename}/%{servicename}-%{upstream_version}.tar.gz

#

BuildArch:      noarch
BuildRequires:  python2-devel
BuildRequires:  python2-pbr
BuildRequires:  git


%description
%{common_desc}


%package -n python-%{servicename}
Summary:        Neutron %{type} Python libraries
Group:          Applications/System

Requires:       python2-eventlet
Requires:       python2-netaddr >= 0.7.18
Requires:       python2-oslo-config >= 2:5.2.0
Requires:       python2-oslo-db >= 4.27.0
Requires:       python2-oslo-log >= 3.36.0
Requires:       python2-oslo-messaging >= 5.29.0
Requires:       python2-oslo-privsep >= 1.23.0
Requires:       python2-oslo-service >= 1.24.0
Requires:       python2-oslo-utils >= 3.33.0
Requires:       python2-pbr


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
install -d -m 755 %{buildroot}%{_sysconfdir}/vpp_statistics

# The generated config files are not moved automatically by setup.py
#mv etc/vpp_statistics/vpp_statistics.ini %{buildroot}%{_sysconfdir}/vpp_statistics
install -p -D -m 644 etc/vpp_statistics/vpp_statistics.ini %{buildroot}%{_sysconfdir}/vpp_statistics/vpp_statistics.ini

# Install Service
install -p -D -m 644 service_scripts/vpp-acl-statistics.service %{buildroot}%{_unitdir}/vpp-acl-statistics.service
install -p -D -m 644 service_scripts/vpp-vrf-statistics.service %{buildroot}%{_unitdir}/vpp-vrf-statistics.service

%files
%license LICENSE
%doc AUTHORS CONTRIBUTING.rst README.rst
%config(noreplace) %attr(0640, root, neutron) %{_sysconfdir}/vpp_statistics/vpp_statistics.ini
%config(noreplace) %attr(0640, root, neutron) %{_unitdir}/vpp-acl-statistics.service
%config(noreplace) %attr(0640, root, neutron) %{_unitdir}/vpp-vrf-statistics.service
%{_bindir}/vpp-acl
%{_bindir}/vpp-vrf

%files -n python-%{servicename}
%{python2_sitelib}/%{modulename}
%{python2_sitelib}/%{modulename}-%{version}-py%{python2_version}.egg-info
%exclude %{python2_sitelib}/%{modulename}/tests

%files -n python-%{servicename}-tests
%{python2_sitelib}/%{modulename}/tests
%{python2_sitelib}/%{modulename}_tests.egg-info


%changelog
