%if 0%{?fedora}
%global with_python3 1
%endif

%global srcname netmiko
%global sum Multi-vendor library to simplify Paramiko SSH connections to network devices

Name:           python-%{srcname}
Version:        2.1.0
Release:        2wocloud6.0.0%{?dist}
Summary:        %{sum}

License:        MIT
URL:            https://pypi.python.org/pypi/%{srcname}
Source0:        https://pypi.io/packages/source/n/%{srcname}/%{srcname}-%{version}.tar.gz

BuildArch:      noarch

%description
%{sum}


%package -n python2-%{srcname}
Summary:        %{sum}
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
Requires:       python2-paramiko >= 2.0.0
Requires:       python2-scp >= 0.10.0
Requires:       PyYAML
Requires:       python2-pyserial
Requires:       python2-textfsm

%{?python_provide:%python_provide python2-%{srcname}}

%description -n python2-%{srcname}
%{sum} - package for Python 2.


%if 0%{?with_python3}

%package -n python3-%{srcname}
Summary:        %{sum}
BuildRequires:  python3-devel
Requires:       python3-paramiko >= 2.0.0
Requires:       python3-scp >= 0.10.0
Requires:       python3-PyYAML
Requires:       python3-pyserial
Requires:       python3-textfsm
%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-%{srcname}
%{sum} - package for Python 3.

%endif

# FIXME: build the documentation, when upstream starts shipping its sources:
# https://github.com/ktbyers/netmiko/issues/507


%prep
%autosetup -n %{srcname}-%{version}

%build
%py2_build

%if 0%{?with_python3}
%py3_build
%endif

%install
%py2_install

%if 0%{?with_python3}
%py3_install
%endif

%check
# FIXME: run unit tests, when upstream starts shipping them:
# https://github.com/ktbyers/netmiko/issues/508


%files -n python2-%{srcname}
%license LICENSE
%doc README.md
%{python2_sitelib}/*

%if 0%{?with_python3}

%files -n python3-%{srcname}
%license LICENSE
%doc README.md
%{python3_sitelib}/*

%endif


%changelog
* Fri Mar 16 2018 Alan Pevec <alan.pevec@redhat.com> 2.1.0-1
- Update to 2.1.0 (rhbz#1532228)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jan 4 2018 Dmitry Tantsur <divius.inside@gmail.com> - 1.4.3-1
- Update to 1.4.3

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jul 24 2017 Dmitry Tantsur <divius.inside@gmail.com> - 1.4.2-1
- Update to 1.4.2

* Mon Jul 24 2017 Dmitry Tantsur <divius.inside@gmail.com> - 1.4.1-1
- Initial packaging (#1465006)
