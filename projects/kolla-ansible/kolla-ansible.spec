%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global common_desc kolla-ansible

Name:             kolla-ansible
Epoch:            1
Version:          2.2.10
Release:          1wocloudmaster%{?dist}
Summary:          Kolla-ansible
License:          ASL 2.0
URL:              http://172.20.2.149/devops/kolla-ansible.git
Source0:          kolla-ansible-%{upstream_version}.tar.gz
BuildArch:        noarch
Summary:          Kolla-ansible Project

BuildRequires:    python2-devel
BuildRequires:    python2-pbr
BuildRequires:    python2-setuptools
Requires:         ansible >= 2.4
Requires:         ansible <= 2.8.5
Requires:         python2-oslo-utils >= 3.33.0
Requires:         expect
Requires:         python2-pbr
Requires:         docker-ce
Requires:         docker-ce-cli
Requires:         python2-six
Requires:         python2-oslo-config
Requires:         python2-netaddr
Requires:         python2-cryptography
Requires:         python2-jmespath


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

install -p -D -m 0644 etc/kolla/globals.yml %{buildroot}%{_sysconfdir}/kolla/globals.yml
install -p -D -m 0644 etc/kolla/passwords.yml %{buildroot}%{_sysconfdir}/kolla/passwords.yml
install -p -D -m 0644 tools/auto_ssh_host_ip %{buildroot}%{_sysconfdir}/kolla/auto_ssh_host_ip
install -p -D -m 0644 ansible/inventory/multinode %{buildroot}%{_sysconfdir}/kolla/multinode

%files
%license LICENSE
%{_bindir}/kolla-ansible
%{_bindir}/kolla-genpwd
%{_bindir}/kolla-mergepwd
%{_bindir}/kolla-auto-ssh
%dir %{_sysconfdir}/kolla
%config(noreplace) %{_sysconfdir}/kolla/globals.yml
%config(noreplace) %{_sysconfdir}/kolla/passwords.yml
%config(noreplace) %{_sysconfdir}/kolla/auto_ssh_host_ip
%config(noreplace) %{_sysconfdir}/kolla/multinode
%{_usr}/share/kolla-ansible/*
%{python2_sitelib}/kolla_ansible/*
%{python2_sitelib}/kolla_ansible-*.egg-info

%changelog
