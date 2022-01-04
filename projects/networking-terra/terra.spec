%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

Summary: UNKNOWN
Name: networking-terra
Version: 13.4.1.20210823144723.c93ee3drc0
Release: 1woclouddevelop%{?dist}
Source0: https://pypi.io/packages/source/p/%{name}/%{name}-%{version}.tar.gz
License: UNKNOWN
Group: Development/Libraries
Prefix: %{_prefix}
BuildArch: noarch
Vendor: UNKNOWN <UNKNOWN>

Requires: python2-chardet
Requires: python2-oauthlib
Requires: python2-requests-oauthlib

%description
UNKNOWN

%prep
%setup -n %{name}-%{upstream_version} -n %{name}-%{upstream_version}

%build
python setup.py build

%install
python setup.py install --single-version-externally-managed -O1 --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES
# Move config files to proper location
install -d -m 755 %{buildroot}%{_sysconfdir}/neutron
pwd
# The generated config files are not moved automatically by setup.py
mv etc/neutron/*.ini %{buildroot}%{_sysconfdir}/neutron

# Make sure neutron-server loads new configuration file
mkdir -p %{buildroot}/%{_datadir}/neutron/server
ln -s %{_sysconfdir}/neutron/terra.ini %{buildroot}%{_datadir}/neutron/server/terra.conf

%clean
rm -rf $RPM_BUILD_ROOT

%files
%config(noreplace) %attr(0640, root, neutron) %{_sysconfdir}/neutron/terra.ini
%config(noreplace) %attr(0640, root, neutron) %{_sysconfdir}/neutron/terra_taas.ini
%{_datadir}/neutron/server/terra.conf
%{python2_sitelib}/networking_terra
%{python2_sitelib}/*.egg-info
%defattr(-,root,root)
