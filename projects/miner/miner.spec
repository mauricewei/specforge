%global release_name rocky
%global with_doc 0
%global project miner

Name:             miner
Epoch:		  1
Version:          1.1.0
Release:          1wocloud6.0.0%{?dist}
Summary:          OpenStack Resource Management System(%{project})

License:          ASL 2.0
URL:              https://www.chinacloud.com.cn
Source0:          https://launchpad.net/%{project}/%{release_name}/%{version}/+download/%{project}-%{version}.tar.gz

#Source1:          %{project}-dist.conf
Source2:          %{project}.logrotate
Source3:          %{project}.cron
#Source4:          %{project}.sudoers

Source10:         %{name}-api.service
Source11:         %{name}-beat.service
Source12:         %{name}-patrol.service
Source13:         %{name}-sentry.service

BuildArch:        noarch
BuildRequires:    python2-devel
BuildRequires:    python-setuptools
BuildRequires:    python-pbr
BuildRequires:    python-d2to1
BuildRequires:    intltool

Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd
BuildRequires:    systemd

Requires(pre):    shadow-utils
Requires:         python-pbr

%description
OpenStack Resource Management System (codename %{project}) provisioning service.


%package -n       python-%{project}

Summary:          Python libraries for %{project}
Requires:         MySQL-python
Requires:         python-qpid
Requires:         python-kombu
Requires:         python-eventlet
Requires:         python-greenlet
Requires:         python-iso8601
Requires:         python-netaddr
Requires:         python-lxml
Requires:         python-webob >= 1.2
Requires:         python-migrate
Requires:         python-sqlalchemy
Requires:         python-paste-deploy
Requires:         python-routes
Requires:         python-novaclient
Requires:         python-cinderclient
Requires:         python-keystoneclient >= 0.4.1
Requires:         python-oslo-config >= 1:1.2.1
Requires:         python-oslo-concurrency
Requires:         python-oslo-messaging
Requires:         python-osprofiler
Requires:         python-jsonschema
Requires:         python-babel
Requires:         python-jinja2
Requires:         python-httplib2
Requires:         python-passlib

%description -n   python-%{project}
OpenStack Resource Management System (codename %{project}) provisioning service.

This package contains the %{project} python library.


%prep
%autosetup -n %{project}-%{version} -S git

# Avoid non-executable-script rpmlint while maintaining timestamps
find %{project} -name \*.py |
while read source; do
  if head -n1 "$source" | grep -F '/usr/bin/env'; then
    touch --ref="$source" "$source".ts
    sed -i '/\/usr\/bin\/env python/{d;q}' "$source"
    touch --ref="$source".ts "$source"
    rm "$source".ts
  fi
done

# Remove the requirements file so that pbr hooks don't add it
# to distutils requires_dist config
rm -rf {test-,}requirements.txt

%build
%{__python2} setup.py build

%install
%{__python2} setup.py install -O1 --skip-build --root %{buildroot}

# docs generation requires everything to be installed first
export PYTHONPATH="$( pwd ):$PYTHONPATH"


# Setup directories
%if 0%{?rhel} != 6
install -d -m 755 %{buildroot}%{_unitdir}
%endif
install -d -m 755 %{buildroot}%{_datadir}/%{project}
install -d -m 755 %{buildroot}%{_sharedstatedir}/%{project}
install -d -m 750 %{buildroot}%{_localstatedir}/log/%{project}

# Install config files

install -d -m 755 %{buildroot}%{_sysconfdir}/%{project}
install -p -D -m 644 etc/%{project}/api-paste.ini %{buildroot}%{_sysconfdir}/%{project}/api-paste.ini
install -p -D -m 644 etc/%{project}/miner.conf.sample %{buildroot}%{_sysconfdir}/%{project}/miner.conf.sample


# Install init scripts
%if 0%{?rhel} == 6
install -p -D -m 755 %{SOURCE20} %{buildroot}%{_initrddir}/%{name}-api
install -p -D -m 755 %{SOURCE21} %{buildroot}%{_initrddir}/%{name}-beat
install -p -D -m 755 %{SOURCE22} %{buildroot}%{_initrddir}/%{name}-patrol
install -p -D -m 755 %{SOURCE23} %{buildroot}%{_initrddir}/%{name}-sentry
install -p -m 755 %{SOURCE30} %{SOURCE31} %{SOURCE32} %{SOURCE33} %{buildroot}%{_datadir}/%{project}
%else
install -p -m 644 %{SOURCE10} %{SOURCE11} %{SOURCE12} %{SOURCE13} %{buildroot}%{_unitdir}
%endif

# Install logrotate
install -p -D -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

# Install Cron
install -p -D -m 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/cron.d/%{name}

# Install pid directory
install -d -m 755 %{buildroot}%{_localstatedir}/run/%{project}

# Install Service
install -p -D -m 644 %{SOURCE10} %{buildroot}%{_unitdir}/miner-api.service
install -p -D -m 644 %{SOURCE11} %{buildroot}%{_unitdir}/miner-beat.service
install -p -D -m 644 %{SOURCE12} %{buildroot}%{_unitdir}/miner-patrol.service
install -p -D -m 644 %{SOURCE13} %{buildroot}%{_unitdir}/miner-sentry.service


# Remove unneeded in production stuff

rm -fr %{buildroot}%{python_sitelib}/%{project}/tests/
rm -fr %{buildroot}%{python_sitelib}/run_tests.*


%pre

USERNAME=%{project}
GROUPNAME=$USERNAME
HOMEDIR=%{_sharedstatedir}/$USERNAME
getent group $GROUPNAME >/dev/null || groupadd -r $GROUPNAME
getent passwd $USERNAME >/dev/null || \
  useradd -r -g $GROUPNAME -G $GROUPNAME -d $HOMEDIR -s /sbin/nologin \
    -c "$USERNAME Daemons" $USERNAME
exit 0

%post
%systemd_post miner-api.service
%systemd_post miner-beat.service
%systemd_post miner-patrol.service
%systemd_post warm-sentry.service

%preun
%systemd_preun miner-api.service
%systemd_preun miner-beat.service
%systemd_preun miner-patrol.service
%systemd_preun warm-sentry.service

%postun
%systemd_postun_with_restart miner-api.service
%systemd_postun_with_restart miner-beat.service
%systemd_postun_with_restart miner-patrol.service
%systemd_postun_with_restart warm-sentry.service

%files
%license LICENSE

%{_bindir}/miner-manage
%{_bindir}/miner-api
%{_bindir}/miner-beat
%{_bindir}/miner-patrol
%{_bindir}/miner-sentry

%{_unitdir}/miner-api.service
%{_unitdir}/miner-beat.service
%{_unitdir}/miner-patrol.service
%{_unitdir}/miner-sentry.service

%dir %{_sysconfdir}/%{project}
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%config(noreplace) %{_sysconfdir}/cron.d/%{name}
%config(noreplace) %attr(0640, root, %{project}) %{_sysconfdir}/%{project}/api-paste.ini
%config(noreplace) %attr(0640, root, %{project}) %{_sysconfdir}/%{project}/%{project}.conf.sample

%dir %attr(0750, %{project}, root) %{_localstatedir}/log/%{project}
%dir %attr(0755, %{project}, root) %{_localstatedir}/run/%{project}


%defattr(-, %{project}, %{project}, -)
%dir %{_sharedstatedir}/%{project}


%files -n python-%{project}
%license LICENSE
%{python_sitelib}/%{project}
%{python_sitelib}/%{project}-%{version}*.egg-info

%changelog
* Wed Nov 20 2019 renminmin <renmm6@chinaunicom.cn> - 2019.11.20
- Wocloud Rocky Release 1.0
