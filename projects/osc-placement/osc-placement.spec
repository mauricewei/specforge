%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%if 0%{?fedora}
%global with_python3 1
%endif

%global sname osc-placement

Name:           osc-placement
Version:        1.5.0
Release:        1wocloud6.1.0%{?dist}
Summary:        Python client for Placement

License:        ASL 2.0
URL:            https://pypi.python.org/pypi/osc-placement/
Source0:        https://tarballs.openstack.org/osc-placement/osc-placement-%{version}%{?milestone}.tar.gz
BuildArch:      noarch


%description
A python and command line client library for Placement.


%package -n python2-%{sname}
Summary:        Python client for Placement

BuildRequires:  python2-devel
BuildRequires:  python-pbr >= 2.0.0
BuildRequires:  python-setuptools

Requires:       python-openstackclient >= 3.3.0
Requires:       python-keystoneauth1 >= 3.1.0
Requires:       python-pbr >= 2.0.0
Requires:       python-six >= 1.9.0

%{?python_provide:%python_provide python2-%{sname}}

%description -n python2-%{sname}
A python and command line client library for Placement.


%if 0%{?with_python3}
%package -n python3-%{sname}
Summary:        Python client for Placement

BuildRequires:  python3-devel
BuildRequires:  python3-pbr >= 2.0.0
BuildRequires:  python3-setuptools

Requires:       python3-openstackclient >= 3.3.0
Requires:       python3-keystoneauth1 >= 3.1.0
Requires:       python3-pbr >= 2.0.0
Requires:       python3-six >= 1.9.0

%{?python_provide:%python_provide python3-%{sname}}

%description -n python3-%{sname}
A python and command line client library for Placement.
%endif

%prep
%setup -q -n %{name}-%{upstream_version}

# Remove the requirements file so that pbr hooks don't add it
# to distutils requires_dist config
rm -rf {test-,}requirements.txt tools/{pip,test}-requires

%build
%py2_build
%if 0%{?with_python3}
%py3_build
%endif


%install
%if 0%{?with_python3}
%py3_install
%endif

%py2_install


%files -n python2-%{sname}
%doc README.rst
%license LICENSE
%{python2_sitelib}/osc_placement*

%if 0%{?with_python3}
%files -n python3-%{sname}
%doc README.rst
%license LICENSE
%{python3_sitelib}/osc_placement*
%endif


%changelog
* Mon Jun 4 2018 xulei <xulei@cmss.chinamobile.com> 1.1.1-1
- Update to 1.1.1-1
