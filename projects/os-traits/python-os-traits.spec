%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%global with_doc 1

%global sname os-traits
%global pypi_name os_traits
%global common_desc \
OS-traits A library containing standardized trait strings. Traits are strings \
that represent a feature of some resource provider. This library contains the \
catalog of constants that have been standardized in the OpenStack community to \
refer to a particular hardware, virtualization, storage, network, or device \
trait.

%if 0%{?fedora}
%global with_python3 1
%endif

Name:           python-%{sname}
Version:        0.9.2
Release:        1woclouddevelop%{?dist}
Summary:        A library containing standardized trait strings

License:        ASL 2.0
URL:            https://docs.openstack.org/developer/os-traits/
Source0:        http://tarballs.openstack.org/%{sname}/%{sname}-%{upstream_version}.tar.gz
BuildArch:      noarch

BuildRequires:  git
BuildRequires:  openstack-macros

%description
%{common_desc}

%package -n     python2-%{sname}
Summary:        %{summary}
%{?python_provide:%python_provide python2-%{sname}}

Requires:       python2-pbr >= 2.0.0
Requires:       python2-six >= 1.10.0

BuildRequires:  python2-devel
BuildRequires:  python2-pbr
BuildRequires:  python2-setuptools

%description -n python2-%{sname}
%{common_desc}

%package -n     python2-%{sname}-tests
Summary:        %{summary}

# Required for the test suite
BuildRequires:  python2-subunit
BuildRequires:  python2-oslotest
BuildRequires:  python2-testtools
BuildRequires:  python2-stestr
%if 0%{?fedora} > 0
BuildRequires:  python2-testscenarios
%else
BuildRequires:  python-testscenarios
%endif

Requires:       python2-%{sname} = %{version}-%{release}
Requires:       python2-subunit
Requires:       python2-oslotest
Requires:       python2-testtools
Requires:       python2-stestr
%if 0%{?fedora} > 0
Requires:       python2-testscenarios
%else
Requires:       python-testscenarios
%endif

%description -n python2-%{sname}-tests
This package contains tests for python os-traits library.

%if 0%{?with_python3}
%package -n     python3-%{sname}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{sname}}

BuildRequires:  python3-devel
BuildRequires:  python3-pbr
BuildRequires:  python3-setuptools

Requires:       python3-pbr >= 2.0.0
Requires:       python3-six >= 1.10.0

%description -n python3-%{sname}
%{common_desc}

%package -n python3-%{sname}-tests
Summary:        %{summary}

# Required for the test suite
BuildRequires:  python3-subunit
BuildRequires:  python3-oslotest
BuildRequires:  python3-stestr
BuildRequires:  python3-testscenarios
BuildRequires:  python3-testtools

Requires:       python3-%{sname} = %{version}-%{release}
Requires:       python3-subunit
Requires:       python3-oslotest
Requires:       python3-stestr
Requires:       python3-testscenarios
Requires:       python3-testtools

%description -n python3-%{sname}-tests
This package contains tests for python os-traits library.
%endif


%if 0%{?with_doc}
%package -n python-%{sname}-doc
Summary:        os-traits documentation

BuildRequires:  python-sphinx
# FIXME: remove following line when a new release including https://review.openstack.org/#/c/479869/ is in u-c
BuildRequires:  python-oslo-sphinx
BuildRequires:  python-openstackdocstheme

%description -n python-%{sname}-doc
Documentation for os-traits
%endif

%prep
%autosetup -n %{sname}-%{upstream_version} -S git
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info
# remove requirements
%py_req_cleanup

%build
%py2_build
%if 0%{?with_python3}
%py3_build
%endif

%if 0%{?with_doc}
# generate html docs
%{__python2} setup.py build_sphinx -b html
# remove the sphinx build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
# Must do the subpackages' install first because the scripts in /usr/bin are
# overwritten with every setup.py install.
%if 0%{?with_python3}
%py3_install
%endif

%py2_install


%check
%{__python2} setup.py test
%if 0%{?with_python3}
%{__python3} setup.py test
%endif

%files -n python2-%{sname}
%license LICENSE
%doc README.rst
%{python2_sitelib}/%{pypi_name}
%{python2_sitelib}/%{pypi_name}-%{upstream_version}-py?.?.egg-info
%exclude %{python2_sitelib}/%{pypi_name}/tests

%files -n python2-%{sname}-tests
%{python2_sitelib}/%{pypi_name}/tests

%if 0%{?with_python3}
%files -n python3-%{sname}
%license LICENSE
%doc README.rst
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-%{upstream_version}-py?.?.egg-info
%exclude %{python3_sitelib}/%{pypi_name}/tests

%files -n python3-%{sname}-tests
%{python3_sitelib}/%{pypi_name}/tests
%endif

%if 0%{?with_doc}
%files -n python-%{sname}-doc
%license LICENSE
%doc doc/build/html
%endif

%changelog
* Thu Aug 16 2018 RDO <dev@lists.rdoproject.org> 0.9.0-1
- Update to 0.9.0

