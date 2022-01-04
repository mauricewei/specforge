%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global common_desc kubeos-ansible

Name:             kubeos-ansible
Epoch:            1
Version:          1.0.4
Release:          2woclouddevelop%{?dist}
Summary:          Kubeos-ansible
License:          ASL 2.0
URL:              http://172.20.2.149/devops/kubeos-ansible.git
Source0:          kubeos-ansible-%{upstream_version}.tar.gz
BuildArch:        noarch
Summary:          Kubeos-ansible Project

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

install -p -D -m 0644 etc/kubeos/globals.yml %{buildroot}%{_sysconfdir}/kubeos/globals.yml
install -p -D -m 0644 etc/kubeos/passwords.yml %{buildroot}%{_sysconfdir}/kubeos/passwords.yml
install -p -D -m 0644 tools/auto_ssh_host_ip %{buildroot}%{_sysconfdir}/kubeos/auto_ssh_host_ip
install -p -D -m 0644 ansible/inventory/multinode %{buildroot}%{_sysconfdir}/kubeos/multinode

%files
%license LICENSE
%{_bindir}/kubeos-ansible
%{_bindir}/kubeos-genpwd
%{_bindir}/kubeos-mergepwd
%{_bindir}/kubeos-auto-ssh
%dir %{_sysconfdir}/kubeos
%config(noreplace) %{_sysconfdir}/kubeos/globals.yml
%config(noreplace) %{_sysconfdir}/kubeos/passwords.yml
%config(noreplace) %{_sysconfdir}/kubeos/auto_ssh_host_ip
%config(noreplace) %{_sysconfdir}/kubeos/multinode
%{_usr}/share/kubeos-ansible/*
%{python2_sitelib}/kubeos_ansible/*
%{python2_sitelib}/kubeos_ansible-*.egg-info

%changelog
