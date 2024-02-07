%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x2426b928085a020d8a90d0d879ab7008d0896c8a

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
# we are excluding some runtime reqs from automatic generator
%global excluded_reqs enmerkar pymongo
# we are excluding some BRs from automatic generator
%global excluded_brs doc8 bandit pre-commit hacking flake8-import-order bashate nodeenv pytest-django pytest-html xvfbwrapper
# Exclude sphinx from BRs if docs are disabled
%if ! 0%{?with_doc}
%global excluded_brs %{excluded_brs} sphinx openstackdocstheme
%endif
%global rhosp 0

%global with_doc 1

Name:       python-django-horizon
# Liberty semver reset
# https://review.openstack.org/#/q/I6a35fa0dda798fad93b804d00a46af80f08d475c,n,z
Epoch:      1
Version:    XXX
Release:    XXX
Summary:    Django application for talking to Openstack

Group:      Development/Libraries
# Code in horizon/horizon/utils taken from django which is BSD
License:    ASL 2.0 and BSD
URL:        http://horizon.openstack.org/
Source0:    https://tarballs.openstack.org/horizon/horizon-%{upstream_version}.tar.gz
Source2:    openstack-dashboard-httpd-2.4.conf
Source3:    python-django-horizon-systemd.conf

# demo config for separate logging
Source4:    openstack-dashboard-httpd-logging.conf

# logrotate config
Source5:    python-django-horizon-logrotate.conf
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        https://tarballs.openstack.org/horizon/horizon-%{upstream_version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif


#
# BuildArch needs to be located below patches in the spec file. Don't ask!
#

BuildArch:  noarch

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
BuildRequires:  openstack-macros
%endif

%description
Horizon is a Django application for providing Openstack UI components.
It allows performing site administrator (viewing account resource usage,
configuring users, accounts, quotas, flavors, etc.) and end user
operations (start/stop/delete instances, create/restore snapshots, view
instance VNC console, etc.)

%package -n     python3-django-horizon
Summary:    Django application for talking to Openstack


BuildRequires: python3-devel
BuildRequires: pyproject-rpm-macros
BuildRequires: git-core
BuildRequires: gettext


# additional provides to be consistent with other django packages
Provides: django-horizon = %{epoch}:%{version}-%{release}

%description -n python3-django-horizon
Horizon is a Django application for providing Openstack UI components.
It allows performing site administrator (viewing account resource usage,
configuring users, accounts, quotas, flavors, etc.) and end user
operations (start/stop/delete instances, create/restore snapshots, view
instance VNC console, etc.)


%package -n openstack-dashboard
Summary:    Openstack web user interface reference implementation
Group:      Applications/System

Requires:   httpd
Requires:   python3-django-horizon = %{epoch}:%{version}-%{release}
%if 0%{rhosp} == 0
Requires:   openstack-dashboard-theme >= %{epoch}:%{version}-%{release}
%else
%{lua: ver = rpm.expand("%version");
if ver == "XXX" then rpm.define("version_major " .. "%{version}"); else x, y = string.find(ver, "%.");
maj = string.sub(ver, 1, x-1); rpm.define("version_major " .. maj .. ".0.0"); end}
Requires:   openstack-dashboard-theme >= %{epoch}:%{version_major}
%endif

Requires:   fontawesome-fonts-web >= 4.1.0

Requires:   openssl
Requires:   logrotate
Requires:   python3-mod_wsgi
Requires:   python3-memcached

BuildRequires: fontawesome-fonts-web >= 4.1.0
BuildRequires: systemd


%description -n openstack-dashboard
Openstack Dashboard is a web user interface for Openstack. The package
provides a reference implementation using the Django Horizon project,
mostly consisting of JavaScript and CSS to tie it altogether as a standalone
site.

%if 0%{?with_doc}
%package doc
Summary:    Documentation for Django Horizon
Group:      Documentation

Requires:   python3-django-horizon = %{epoch}:%{version}-%{release}
%description doc
Documentation for the Django Horizon application for talking with Openstack
%endif

%if 0%{rhosp} == 0
%package -n openstack-dashboard-theme
Summary: OpenStack web user interface reference implementation theme module
Requires: openstack-dashboard = %{epoch}:%{version}-%{release}

%description -n openstack-dashboard-theme
Customization module for OpenStack Dashboard to provide a branded logo.
%endif

%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -n horizon-%{upstream_version} -S git

# customize default settings
# WAS [PATCH] disable debug, move web root
sed -i "/^DEBUG =.*/c\DEBUG = False" openstack_dashboard/local/local_settings.py.example
sed -i "/^WEBROOT =.*/c\WEBROOT = '/dashboard/'" openstack_dashboard/local/local_settings.py.example
sed -i "/^.*ALLOWED_HOSTS =.*/c\ALLOWED_HOSTS = ['horizon.example.com', 'localhost']" openstack_dashboard/local/local_settings.py.example
sed -i "/^.*LOCAL_PATH =.*/c\LOCAL_PATH = '/tmp'" openstack_dashboard/local/local_settings.py.example
sed -i "/^.*POLICY_FILES_PATH =.*/c\POLICY_FILES_PATH = '/etc/openstack-dashboard'" openstack_dashboard/local/local_settings.py.example

sed -i "/^BIN_DIR = .*/c\BIN_DIR = '/usr/bin'" openstack_dashboard/settings.py
sed -i "/^COMPRESS_PARSER = .*/a COMPRESS_OFFLINE = True" openstack_dashboard/settings.py

# set COMPRESS_OFFLINE=True
sed -i 's:COMPRESS_OFFLINE.=.False:COMPRESS_OFFLINE = True:' openstack_dashboard/settings.py

# Set help_url
%if 0%{?rhosp}
sed -i "s;'help_url': \"https://docs.openstack.org/\";'help_url': \"https://access.redhat.com/documentation/en/red-hat-openstack-platform/\";" openstack_dashboard/settings.py
%endif

sed -i /^[[:space:]]*-c{env:.*_CONSTRAINTS_FILE.*/d tox.ini
sed -i "s/^deps = -c{env:.*_CONSTRAINTS_FILE.*/deps =/" tox.ini
sed -i /^minversion.*/d tox.ini
sed -i /^requires.*virtualenv.*/d tox.ini
sed -i '/^[\ ]*hacking>=.*/d' tox.ini
sed -i '/^[\ ]*doc8 doc\/source/d' tox.ini
# requirements-override-centos C9S is providing pyyaml-5.4.1 while package requires >= 6.0
sed -i "s/PyYAML.*/PyYAML/" requirements.txt
# requirements-override-centos C9S is providing six-1.15 while package requires >= 1.16
sed -i "s/six.*/six/" requirements.txt

# uncap some XStatic deps we don't provide yet in RDO
sed -i 's/^\(XStatic\)>=.*/\1/' requirements.txt
sed -i 's/^\(XStatic-Angular\)>=.*/\1/' requirements.txt
sed -i 's/^\(XStatic-JQuery-Migrate\)>=.*/\1/' requirements.txt
sed -i 's/^\(XStatic-jquery-ui\)>=.*/\1/' requirements.txt
sed -i 's/^\(XStatic-jQuery\)>=.*/\1/' requirements.txt

# Exclude some bad-known BRs
for pkg in %{excluded_brs}; do
  for reqfile in doc/requirements.txt test-requirements.txt; do
    if [ -f $reqfile ]; then
      sed -i /^${pkg}.*/d $reqfile
    fi
  done
done

# Automatic BR generation
# Exclude some bad-known runtime reqs
for pkg in %{excluded_reqs}; do
  sed -i /^${pkg}.*/d requirements.txt
done

%generate_buildrequires
%if 0%{?with_doc}
  %pyproject_buildrequires -t -e %{default_toxenv},docs
%else
  %pyproject_buildrequires -t -e %{default_toxenv}
%endif

%build
# compile message strings
cd horizon && django-admin compilemessages && cd ..
cd openstack_dashboard && django-admin compilemessages && cd ..
%pyproject_wheel

# compress css, js etc.
cp openstack_dashboard/local/local_settings.py.example openstack_dashboard/local/local_settings.py
# get it ready for compressing later in puppet-horizon
%{__python3} manage.py collectstatic --noinput --clear
%{__python3} manage.py compress --force

%if 0%{?with_doc}
# build docs
%tox -e docs
# Fix hidden-file-or-dir warnings
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif
# undo hack
cp openstack_dashboard/local/local_settings.py.example openstack_dashboard/local/local_settings.py


%install
%pyproject_install

# drop httpd-conf snippet
install -m 0644 -D -p %{SOURCE2} %{buildroot}%{_sysconfdir}/httpd/conf.d/openstack-dashboard.conf
install -d -m 755 %{buildroot}%{_datadir}/openstack-dashboard
install -d -m 755 %{buildroot}%{_sharedstatedir}/openstack-dashboard
install -d -m 755 %{buildroot}%{_sysconfdir}/openstack-dashboard

# drop config snippet
install -m 0644 -D -p %{SOURCE4} .

# create directory for systemd snippet
mkdir -p %{buildroot}%{_unitdir}/httpd.service.d/
cp %{SOURCE3} %{buildroot}%{_unitdir}/httpd.service.d/openstack-dashboard.conf


# Copy everything to /usr/share
mv %{buildroot}%{python3_sitelib}/openstack_dashboard \
   %{buildroot}%{_datadir}/openstack-dashboard
cp manage.py %{buildroot}%{_datadir}/openstack-dashboard
rm -rf %{buildroot}%{python3_sitelib}/openstack_dashboard

# remove unnecessary .po files
find %{buildroot} -name django.po -exec rm '{}' \;
find %{buildroot} -name djangojs.po -exec rm '{}' \;

# Move config to /etc, symlink it back to /usr/share
mv %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/local/local_settings.py.example %{buildroot}%{_sysconfdir}/openstack-dashboard/local_settings
ln -s ../../../../..%{_sysconfdir}/openstack-dashboard/local_settings %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/local/local_settings.py

%if 0%{?rhosp}
mkdir -p %{buildroot}%{_sysconfdir}/openstack-dashboard/local_settings.d
mv %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/local/local_settings.d/* %{buildroot}%{_sysconfdir}/openstack-dashboard/local_settings.d
rmdir %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/local/local_settings.d
ln -s ../../../../..%{_sysconfdir}/openstack-dashboard/local_settings.d %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/local/local_settings.d
%endif

mv %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/conf/default_policies %{buildroot}%{_sysconfdir}/openstack-dashboard
mv %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/conf/*.yaml %{buildroot}%{_sysconfdir}/openstack-dashboard
mv %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/conf/nova_policy.d %{buildroot}%{_sysconfdir}/openstack-dashboard

%find_lang django --all-name

grep "\/usr\/share\/openstack-dashboard" django.lang > dashboard.lang
grep "\/site-packages\/horizon" django.lang > horizon.lang

# copy static files to %{_datadir}/openstack-dashboard/static
mkdir -p %{buildroot}%{_datadir}/openstack-dashboard/static
cp -a openstack_dashboard/static/* %{buildroot}%{_datadir}/openstack-dashboard/static
cp -a horizon/static/* %{buildroot}%{_datadir}/openstack-dashboard/static
cp -a static/* %{buildroot}%{_datadir}/openstack-dashboard/static

# create /var/run/openstack-dashboard/ and own it
mkdir -p %{buildroot}%{_sharedstatedir}/openstack-dashboard

# create /var/log/horizon and own it
mkdir -p %{buildroot}%{_var}/log/horizon

# place logrotate config:
mkdir -p %{buildroot}%{_sysconfdir}/logrotate.d
cp -a %{SOURCE5} %{buildroot}%{_sysconfdir}/logrotate.d/openstack-dashboard

%py_byte_compile %{python3} %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard

%check
rm horizon/test/unit/hacking/test_checks.py
%{__python3} manage.py test horizon --settings=horizon.test.settings

%post -n openstack-dashboard
# ugly hack to set a unique SECRET_KEY
sed -i "/^from horizon.utils import secret_key$/d" /etc/openstack-dashboard/local_settings
sed -i "/^SECRET_KEY.*$/{N;s/^.*$/SECRET_KEY='`openssl rand -hex 10`'/}" /etc/openstack-dashboard/local_settings
# reload systemd unit files
systemctl daemon-reload >/dev/null 2>&1 || :

%postun
# update systemd unit files
systemctl daemon-reload >/dev/null 2>&1 || :

%files -n python3-django-horizon -f horizon.lang
%doc README.rst openstack-dashboard-httpd-logging.conf
%license LICENSE
%dir %{python3_sitelib}/horizon
%{python3_sitelib}/horizon/*.py*
%{python3_sitelib}/horizon/browsers
%{python3_sitelib}/horizon/conf
%{python3_sitelib}/horizon/contrib
%{python3_sitelib}/horizon/forms
%{python3_sitelib}/horizon/hacking
%{python3_sitelib}/horizon/management
%{python3_sitelib}/horizon/static
%{python3_sitelib}/horizon/tables
%{python3_sitelib}/horizon/tabs
%{python3_sitelib}/horizon/templates
%{python3_sitelib}/horizon/templatetags
%{python3_sitelib}/horizon/test
%{python3_sitelib}/horizon/utils
%{python3_sitelib}/horizon/workflows
%{python3_sitelib}/horizon/karma.conf.js
%{python3_sitelib}/horizon/middleware
%{python3_sitelib}/openstack_auth
%{python3_sitelib}/*.dist-info
%{python3_sitelib}/horizon/__pycache__

%files -n openstack-dashboard -f dashboard.lang
%license LICENSE
%dir %{_datadir}/openstack-dashboard/
%{_datadir}/openstack-dashboard/*.py*
%{_datadir}/openstack-dashboard/static
%{_datadir}/openstack-dashboard/openstack_dashboard/*.py*
%{_datadir}/openstack-dashboard/openstack_dashboard/api
%{_datadir}/openstack-dashboard/openstack_dashboard/contrib
%dir %{_datadir}/openstack-dashboard/openstack_dashboard/dashboards/
%{_datadir}/openstack-dashboard/openstack_dashboard/dashboards/admin
%{_datadir}/openstack-dashboard/openstack_dashboard/dashboards/identity
%{_datadir}/openstack-dashboard/openstack_dashboard/dashboards/project
%{_datadir}/openstack-dashboard/openstack_dashboard/dashboards/settings
%{_datadir}/openstack-dashboard/openstack_dashboard/dashboards/__init__.py*
%{_datadir}/openstack-dashboard/openstack_dashboard/django_pyscss_fix
%{_datadir}/openstack-dashboard/openstack_dashboard/enabled
%{_datadir}/openstack-dashboard/openstack_dashboard/karma.conf.js
%{_datadir}/openstack-dashboard/openstack_dashboard/local
%{_datadir}/openstack-dashboard/openstack_dashboard/management
%{_datadir}/openstack-dashboard/openstack_dashboard/static
%{_datadir}/openstack-dashboard/openstack_dashboard/templates
%{_datadir}/openstack-dashboard/openstack_dashboard/templatetags
%{_datadir}/openstack-dashboard/openstack_dashboard/themes
%{_datadir}/openstack-dashboard/openstack_dashboard/test
%{_datadir}/openstack-dashboard/openstack_dashboard/usage
%{_datadir}/openstack-dashboard/openstack_dashboard/utils
%dir %{_datadir}/openstack-dashboard/openstack_dashboard
%dir %{_datadir}/openstack-dashboard/openstack_dashboard/locale
%dir %{_datadir}/openstack-dashboard/openstack_dashboard/locale/??
%dir %{_datadir}/openstack-dashboard/openstack_dashboard/locale/??_??
%dir %{_datadir}/openstack-dashboard/openstack_dashboard/locale/??/LC_MESSAGES
%dir %{_datadir}/openstack-dashboard/openstack_dashboard/locale/??_??/LC_MESSAGES

%if 0%{?rhosp}
%dir %attr(0750, root, apache) %{_sysconfdir}/openstack-dashboard/local_settings.d/
%{_sysconfdir}/openstack-dashboard/local_settings.d/*.example
%endif

%{_datadir}/openstack-dashboard/openstack_dashboard/.eslintrc
%{_datadir}/openstack-dashboard/openstack_dashboard/__pycache__
%{_datadir}/openstack-dashboard/openstack_dashboard/dashboards/__pycache__

%dir %attr(0750, root, apache) %{_sysconfdir}/openstack-dashboard
%dir %attr(0750, apache, apache) %{_sharedstatedir}/openstack-dashboard
%dir %attr(0750, apache, apache) %{_var}/log/horizon
%config(noreplace) %{_sysconfdir}/httpd/conf.d/openstack-dashboard.conf
%config(noreplace) %attr(0640, root, apache) %{_sysconfdir}/openstack-dashboard/local_settings
%config(noreplace) %attr(0640, root, apache) %{_sysconfdir}/openstack-dashboard/default_policies/*.yaml
%config(noreplace) %attr(0640, root, apache) %{_sysconfdir}/openstack-dashboard/default_policies/README.txt
%config(noreplace) %attr(0640, root, apache) %{_sysconfdir}/openstack-dashboard/cinder_policy.yaml
%config(noreplace) %attr(0640, root, apache) %{_sysconfdir}/openstack-dashboard/keystone_policy.yaml
%config(noreplace) %attr(0640, root, apache) %{_sysconfdir}/openstack-dashboard/nova_policy.yaml
%config(noreplace) %attr(0640, root, apache) %{_sysconfdir}/openstack-dashboard/glance_policy.yaml
%config(noreplace) %attr(0640, root, apache) %{_sysconfdir}/openstack-dashboard/neutron_policy.yaml
%config(noreplace) %attr(0640, root, apache) %{_sysconfdir}/openstack-dashboard/nova_policy.d/api-extensions.yaml
%config(noreplace) %attr(0644, root, root) %{_sysconfdir}/logrotate.d/openstack-dashboard
%attr(755,root,root) %dir %{_unitdir}/httpd.service.d
%config(noreplace) %{_unitdir}/httpd.service.d/openstack-dashboard.conf

%if 0%{?with_doc}
%files doc
%doc doc/build/html
%license LICENSE
%endif

%if 0%{rhosp} == 0
%files -n openstack-dashboard-theme
#%{_datadir}/openstack-dashboard/openstack_dashboard/dashboards/theme
#%{_datadir}/openstack-dashboard/openstack_dashboard/enabled/_99_customization.*
%endif

%changelog

# REMOVEME: error caused by commit https://opendev.org/openstack/horizon/commit/8a3006756d09a39d9588336b0067cbbdca76bc38
