%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global common_desc sunshine-ansible

%define _binaries_in_noarch_packages_terminate_build 0

Name:             sunshine-ansible
Epoch:            1
Version:          2.2.10
Release:          1wocloudmaster%{?dist}
Summary:          Sunshine-ansible
License:          ASL 2.0
URL:              http://172.20.2.149/devops/sunshine-ansible.git
Source0:          sunshine-ansible-%{upstream_version}.tar.gz
BuildArch:        noarch
Summary:          Sunshine-ansible Project

BuildRequires:    python2-devel
BuildRequires:    python2-pbr
BuildRequires:    python2-setuptools
Requires:         ansible >= 2.4
Requires:         python2-oslo-utils >= 3.33.0
Requires:         expect


%description
%{common_desc}

%description
%{common_desc}

%prep
%setup -q

# Let RPM handle the requirements
%py_req_cleanup

%build
%{__python2} setup.py build

%install
%{__python2} setup.py install -O1 --skip-build --root %{buildroot}

install -p -D -m 0644 etc/sunshine/globals.yml %{buildroot}%{_sysconfdir}/sunshine/globals.yml
install -p -D -m 0644 etc/sunshine/passwords.yml %{buildroot}%{_sysconfdir}/sunshine/passwords.yml
install -p -D -m 0644 tools/auto_ssh_host_ip %{buildroot}%{_sysconfdir}/sunshine/auto_ssh_host_ip
install -p -D -m 0644 ansible/inventory/multinode %{buildroot}%{_sysconfdir}/sunshine/multinode

%files
%license LICENSE
%{_bindir}/sunshine-ansible
%{_bindir}/sunshine-genpwd
%{_bindir}/sunshine-mergepwd
%{_bindir}/sunshine-auto-ssh
%dir %{_sysconfdir}/sunshine
%config(noreplace) %{_sysconfdir}/sunshine/globals.yml
%config(noreplace) %{_sysconfdir}/sunshine/passwords.yml
%config(noreplace) %{_sysconfdir}/sunshine/auto_ssh_host_ip
%config(noreplace) %{_sysconfdir}/sunshine/multinode
%{_usr}/share/sunshine-ansible/*
%{python2_sitelib}/sunshine_ansible/*
%{python2_sitelib}/sunshine_ansible-*.egg-info

%changelog
