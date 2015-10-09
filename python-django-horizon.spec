%global release_series liberty
%global release_name %{?release_series}-rc2
%global service horizon
%global milestone .0rc2


%global with_compression 1

Name:       python-django-horizon

# Liberty semver reset
# https://review.openstack.org/#/q/I6a35fa0dda798fad93b804d00a46af80f08d475c,n,z
Epoch:      1
Version:    8.0.0
Release:    0.1%{?milestone}%{?dist}
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
Summary:    Django application for talking to Openstack

Group:      Development/Libraries
# Code in horizon/horizon/utils taken from django which is BSD
License:    ASL 2.0 and BSD
URL:        http://horizon.openstack.org/
# https://launchpad.net/horizon/liberty/liberty-rc2/+download/horizon-8.0.0.0b3.tar.gz
Source0:    https://launchpad.net/%{service}/liberty/%{release_name}/+download/%{service}-%{upstream_version}.tar.gz
Source2:    openstack-dashboard-httpd-2.4.conf

# systemd snippet to collect static files and compress on httpd restart
Source3:    python-django-horizon-systemd.conf

# demo config for separate logging
Source4:    openstack-dashboard-httpd-logging.conf

# logrotate config
Source5:    python-django-horizon-logrotate.conf


#
# patches_base=8.0.0.0rc2
Patch0001: 0001-disable-debug-move-web-root.patch
Patch0002: 0002-remove-runtime-dep-to-python-pbr.patch
Patch0003: 0003-Add-a-customization-module-based-on-RHOS.patch
Patch0004: 0004-fix-credentials-boxes-when-selecting-WebSSO.patch

#
# BuildArch needs to be located below patches in the spec file. Don't ask!
#

BuildArch:  noarch

BuildRequires:   python-django
Requires:   python-django


Requires:   pytz
Requires:   python-lockfile
Requires:   python-six >= 1.9.0
Requires:   python-pbr

BuildRequires: python2-devel
BuildRequires: python-setuptools
BuildRequires: python-pbr >= 0.10.8
BuildRequires: python-lockfile
BuildRequires: python-eventlet
BuildRequires: git
BuildRequires: python-six >= 1.9.0
BuildRequires: gettext

# for checks:
%if 0%{?rhel} == 0
BuildRequires:   python-django-nose >= 1.2
BuildRequires:   python-coverage
BuildRequires:   python-mox3
BuildRequires:   python-mock
BuildRequires:   python-nose-exclude
BuildRequires:   python-nose
BuildRequires:   python-selenium
%endif
BuildRequires:   python-netaddr
BuildRequires:   python-kombu
BuildRequires:   python-anyjson
BuildRequires:   python-iso8601

# additional provides to be consistent with other django packages
Provides: django-horizon = %{epoch}:%{version}-%{release}

%description
Horizon is a Django application for providing Openstack UI components.
It allows performing site administrator (viewing account resource usage,
configuring users, accounts, quotas, flavors, etc.) and end user
operations (start/stop/delete instances, create/restore snapshots, view
instance VNC console, etc.)


%package -n openstack-dashboard
Summary:    Openstack web user interface reference implementation
Group:      Applications/System

Requires:   httpd
Requires:   mod_wsgi
Requires:   %{name} = %{epoch}:%{version}-%{release}
Requires:   python-django-openstack-auth >= 1.1.7
Requires:   python-django-compressor >= 1.4
Requires:   python-django-appconf
Requires:   python-lesscpy

Requires:   python-glanceclient
Requires:   python-keystoneclient >= 0.7.0
Requires:   python-novaclient >= 2.15.0
Requires:   python-neutronclient
Requires:   python-cinderclient >= 1.0.6
Requires:   python-swiftclient
Requires:   python-heatclient
Requires:   python-ceilometerclient
Requires:   python-troveclient >= 1.0.0
Requires:   python-saharaclient
Requires:   python-netaddr
Requires:   python-oslo-config
Requires:   python-eventlet
Requires:   python-django-pyscss >= 1.0.5
Requires:   python-XStatic
Requires:   python-XStatic-jQuery
Requires:   python-XStatic-Angular >= 1:1.3.7
Requires:   python-XStatic-Angular-Mock
Requires:   python-XStatic-Angular-Bootstrap
Requires:   python-XStatic-D3
Requires:   python-XStatic-Font-Awesome >= 4.1.0.0-4
Requires:   python-XStatic-Hogan
Requires:   python-XStatic-JQuery-Migrate
Requires:   python-XStatic-JQuery-TableSorter
Requires:   python-XStatic-JQuery-quicksearch
Requires:   python-XStatic-JSEncrypt
Requires:   python-XStatic-Jasmine
Requires:   python-XStatic-QUnit
Requires:   python-XStatic-Rickshaw
Requires:   python-XStatic-Spin
Requires:   python-XStatic-jquery-ui
Requires:   python-XStatic-Bootstrap-Datepicker
Requires:   python-XStatic-Bootstrap-SCSS
Requires:   python-XStatic-termjs
Requires:   python-XStatic-smart-table
Requires:   python-XStatic-Angular-lrdragndrop
Requires:   python-XStatic-Magic-Search
Requires:   python-XStatic-Angular-Gettext
Requires:   python-XStatic-Magic-Search
Requires:   python-XStatic-bootswatch
Requires:   python-XStatic-roboto-fontface
Requires:   python-XStatic-mdi

Requires:   python-scss >= 1.2.1
Requires:   fontawesome-fonts-web >= 4.1.0

Requires:   python-oslo-concurrency
Requires:   python-oslo-config
Requires:   python-oslo-i18n
Requires:   python-oslo-serialization
Requires:   python-oslo-utils
Requires:   python-oslo-policy
Requires:   python-babel
Requires:   python-pint

Requires:   openssl
Requires:   logrotate

BuildRequires: python-django-openstack-auth >= 1.2.0
BuildRequires: python-django-compressor >= 1.4
BuildRequires: python-django-appconf
BuildRequires: python-lesscpy
BuildRequires: python-django-pyscss >= 1.0.5
BuildRequires: python-XStatic
BuildRequires: python-XStatic-jQuery
BuildRequires: python-XStatic-Angular >= 1:1.3.7
BuildRequires: python-XStatic-Angular-Mock
BuildRequires: python-XStatic-Angular-Bootstrap
BuildRequires: python-XStatic-D3
BuildRequires: python-XStatic-Font-Awesome
BuildRequires: python-XStatic-Hogan
BuildRequires: python-XStatic-JQuery-Migrate
BuildRequires: python-XStatic-JQuery-TableSorter
BuildRequires: python-XStatic-JQuery-quicksearch
BuildRequires: python-XStatic-JSEncrypt
BuildRequires: python-XStatic-Jasmine
BuildRequires: python-XStatic-QUnit
BuildRequires: python-XStatic-Rickshaw
BuildRequires: python-XStatic-Spin
BuildRequires: python-XStatic-jquery-ui
BuildRequires: python-XStatic-Bootstrap-Datepicker
BuildRequires: python-XStatic-Bootstrap-SCSS
BuildRequires: python-XStatic-termjs
BuildRequires: python-XStatic-smart-table
BuildRequires: python-XStatic-Angular-lrdragndrop
BuildRequires: python-XStatic-Magic-Search
BuildRequires: python-XStatic-Angular-Gettext
BuildRequires: python-XStatic-bootswatch
BuildRequires: python-XStatic-roboto-fontface
BuildRequires: python-XStatic-mdi
# bootstrap-scss requires at least python-scss >= 1.2.1
BuildRequires: python-scss >= 1.2.1
BuildRequires: fontawesome-fonts-web >= 4.1.0
BuildRequires: python-oslo-concurrency
BuildRequires: python-oslo-config >= 1.9.3
BuildRequires: python-oslo-i18n
BuildRequires: python-oslo-serialization
BuildRequires: python-oslo-utils >= 1.4.0
BuildRequires: python-babel
BuildRequires: python-pint

BuildRequires: pytz
BuildRequires: systemd

%description -n openstack-dashboard
Openstack Dashboard is a web user interface for Openstack. The package
provides a reference implementation using the Django Horizon project,
mostly consisting of JavaScript and CSS to tie it altogether as a standalone
site.


%package doc
Summary:    Documentation for Django Horizon
Group:      Documentation

Requires:   %{name} = %{epoch}:%{version}-%{release}
BuildRequires: python-sphinx >= 1.1.3

# Doc building basically means we have to mirror Requires:
BuildRequires: python-glanceclient
BuildRequires: python-keystoneclient
BuildRequires: python-novaclient >= 2.15.0
BuildRequires: python-neutronclient
BuildRequires: python-cinderclient
BuildRequires: python-swiftclient
BuildRequires: python-heatclient
BuildRequires: python-ceilometerclient
BuildRequires: python-troveclient >= 1.0.0
BuildRequires: python-saharaclient
BuildRequires: python-oslo-sphinx >= 2.3.0

%description doc
Documentation for the Django Horizon application for talking with Openstack

%package -n openstack-dashboard-theme
Summary: OpenStack web user interface reference implementation theme module
Requires: openstack-dashboard = %{epoch}:%{version}-%{release}

%description -n openstack-dashboard-theme
Customization module for OpenStack Dashboard to provide a branded logo.

%prep
%setup -q -n horizon-%{upstream_version}

# Use git to manage patches.
# http://rwmj.wordpress.com/2011/08/09/nice-rpm-git-patch-management-trick/
git init
git config user.email "python-django-horizon-owner@fedoraproject.org"
git config user.name "python-django-horizon"
git add .
git commit -a -q -m "%{version} baseline"
git am %{patches}

# remove unnecessary .mo files
# they will be generated later during package build
find . -name "django*.mo" -exec rm -f '{}' \;

# Remove the requirements file so that pbr hooks don't add it
# to distutils requires_dist config
rm -rf {test-,}requirements.txt tools/{pip,test}-requires

# drop config snippet
cp -p %{SOURCE4} .

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



%build
# compile message strings
cd horizon && django-admin compilemessages && cd ..
cd openstack_dashboard && django-admin compilemessages && cd ..
# Dist tarball is missing .mo files so they're not listed in distributed egg metadata.
# Removing egg-info and letting PBR regenerate it was working around that issue
# but PBR cannot regenerate complete SOURCES.txt so some other files wont't get installed.
# Further reading why not remove upstream egg metadata:
# https://github.com/emonty/python-oslo-messaging/commit/f632684eb2d582253601e8da7ffdb8e55396e924
# https://fedorahosted.org/fpc/ticket/488
echo >> horizon.egg-info/SOURCES.txt
ls */locale/*/LC_MESSAGES/django*mo >> horizon.egg-info/SOURCES.txt
%{__python} setup.py build

# compress css, js etc.
cp openstack_dashboard/local/local_settings.py.example openstack_dashboard/local/local_settings.py

# get it ready for compressing later in puppet-horizon
%{__python} manage.py collectstatic --noinput
%{__python} manage.py compress --force


# build docs
export PYTHONPATH="$( pwd ):$PYTHONPATH"
sphinx-build -b html doc/source html

# undo hack
cp openstack_dashboard/local/local_settings.py.example openstack_dashboard/local/local_settings.py

# Fix hidden-file-or-dir warnings
rm -fr html/.doctrees html/.buildinfo

%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

# drop httpd-conf snippet
install -m 0644 -D -p %{SOURCE2} %{buildroot}%{_sysconfdir}/httpd/conf.d/openstack-dashboard.conf
install -d -m 755 %{buildroot}%{_datadir}/openstack-dashboard
install -d -m 755 %{buildroot}%{_sharedstatedir}/openstack-dashboard
install -d -m 755 %{buildroot}%{_sysconfdir}/openstack-dashboard

# create directory for systemd snippet
mkdir -p %{buildroot}%{_unitdir}/httpd.service.d/
cp %{SOURCE3} %{buildroot}%{_unitdir}/httpd.service.d/openstack-dashboard.conf


# create directory for systemd snippet
mkdir -p %{buildroot}%{_unitdir}/httpd.service.d/
cp %{SOURCE3} %{buildroot}%{_unitdir}/httpd.service.d/openstack-dashboard.conf

# Copy everything to /usr/share
mv %{buildroot}%{python_sitelib}/openstack_dashboard \
   %{buildroot}%{_datadir}/openstack-dashboard
cp manage.py %{buildroot}%{_datadir}/openstack-dashboard
rm -rf %{buildroot}%{python_sitelib}/openstack_dashboard

# remove unnecessary .po files
find %{buildroot} -name django.po -exec rm '{}' \;
find %{buildroot} -name djangojs.po -exec rm '{}' \;

# Move config to /etc, symlink it back to /usr/share
mv %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/local/local_settings.py.example %{buildroot}%{_sysconfdir}/openstack-dashboard/local_settings
ln -s ../../../../../%{_sysconfdir}/openstack-dashboard/local_settings %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/local/local_settings.py

mv %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/conf/*.json %{buildroot}%{_sysconfdir}/openstack-dashboard

%find_lang django
%find_lang djangojs

grep "\/usr\/share\/openstack-dashboard" django.lang > dashboard.lang
grep "\/site-packages\/horizon" django.lang > horizon.lang

cat djangojs.lang >> horizon.lang

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


%check
# don't run tests on rhel
%if 0%{?rhel} == 0
# currently fails due to python-oslo-serialization issue
#./run_tests.sh -N -P
%endif

%post -n openstack-dashboard
# ugly hack to set a unique SECRET_KEY
sed -i "/^from horizon.utils import secret_key$/d" /etc/openstack-dashboard/local_settings
sed -i "/^SECRET_KEY.*$/{N;s/^.*$/SECRET_KEY='`openssl rand -hex 10`'/}" /etc/openstack-dashboard/local_settings
# reload systemd unit files
systemctl daemon-reload >/dev/null 2>&1 || :

%postun
# update systemd unit files
%{systemd_postun}

%files -f horizon.lang
%doc README.rst openstack-dashboard-httpd-logging.conf
%license LICENSE
%dir %{python_sitelib}/horizon
%{python_sitelib}/horizon/*.py*
%{python_sitelib}/horizon/browsers
%{python_sitelib}/horizon/conf
%{python_sitelib}/horizon/contrib
%{python_sitelib}/horizon/forms
%{python_sitelib}/horizon/locale/*.pot
%{python_sitelib}/horizon/management
%{python_sitelib}/horizon/static
%{python_sitelib}/horizon/tables
%{python_sitelib}/horizon/tabs
%{python_sitelib}/horizon/templates
%{python_sitelib}/horizon/templatetags
%{python_sitelib}/horizon/test
%{python_sitelib}/horizon/utils
%{python_sitelib}/horizon/workflows
%{python_sitelib}/horizon/karma.conf.js
%{python_sitelib}/*.egg-info

%files -n openstack-dashboard -f dashboard.lang
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
%{_datadir}/openstack-dashboard/openstack_dashboard/wsgi
%dir %{_datadir}/openstack-dashboard/openstack_dashboard
%dir %{_datadir}/openstack-dashboard/openstack_dashboard/locale
%dir %{_datadir}/openstack-dashboard/openstack_dashboard/locale/??
%dir %{_datadir}/openstack-dashboard/openstack_dashboard/locale/??_??
%dir %{_datadir}/openstack-dashboard/openstack_dashboard/locale/??/LC_MESSAGES
%dir %{_datadir}/openstack-dashboard/openstack_dashboard/locale/??_??/LC_MESSAGES
%{_datadir}/openstack-dashboard/openstack_dashboard/locale/*.pot
%{_datadir}/openstack-dashboard/openstack_dashboard/.eslintrc

%dir %attr(0750, root, apache) %{_sysconfdir}/openstack-dashboard
%dir %attr(0750, apache, apache) %{_sharedstatedir}/openstack-dashboard
%dir %attr(0750, apache, apache) %{_var}/log/horizon
%config(noreplace) %{_sysconfdir}/httpd/conf.d/openstack-dashboard.conf
%config(noreplace) %attr(0640, root, apache) %{_sysconfdir}/openstack-dashboard/local_settings
%config(noreplace) %attr(0640, root, apache) %{_sysconfdir}/openstack-dashboard/ceilometer_policy.json
%config(noreplace) %attr(0640, root, apache) %{_sysconfdir}/openstack-dashboard/cinder_policy.json
%config(noreplace) %attr(0640, root, apache) %{_sysconfdir}/openstack-dashboard/keystone_policy.json
%config(noreplace) %attr(0640, root, apache) %{_sysconfdir}/openstack-dashboard/nova_policy.json
%config(noreplace) %attr(0640, root, apache) %{_sysconfdir}/openstack-dashboard/glance_policy.json
%config(noreplace) %attr(0640, root, apache) %{_sysconfdir}/openstack-dashboard/neutron_policy.json
%config(noreplace) %attr(0640, root, apache) %{_sysconfdir}/openstack-dashboard/heat_policy.json
%{_sysconfdir}/logrotate.d/openstack-dashboard
%config(noreplace) %attr(444,root,root) %{_sysconfdir}/logrotate.d/openstack-dashboard
%attr(755,root,root) %dir %{_unitdir}/httpd.service.d
%config(noreplace) %{_unitdir}/httpd.service.d/openstack-dashboard.conf

%files doc
%doc html

%files -n openstack-dashboard-theme
%{_datadir}/openstack-dashboard/openstack_dashboard/dashboards/theme
%{_datadir}/openstack-dashboard/openstack_dashboard/enabled/_99_customization.*

%changelog
* Fri Oct 09 2015 Matthias Runge <mrunge@redhat.com> - 1:8.0.0-0.1.0rc2
- rc2

* Wed Sep 30 2015 Matthias Runge <mrunge@redhat.com> - 1:8.0.0-0.1.0rc1
- rc1
- cherry-picking RCUE fixes

* Thu Sep 17 2015 Matthias Runge <mrunge@redhat.com> - 1:8.0.0-0.1.0b3
- liberty pre-release

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2015.1.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu May 28 2015 Matthias Runge <mrunge@redhat.com> - 2015.1.0-7
- CVE-2015-3988 python-django-horizon: persistent XSS in Horizon metadata

* Thu May 21 2015 Matthias Runge <mrunge@redhat.com> - 2015.1.0-6
- add AUTH_USER_MODEL reference (rhbz#1221117)

* Fri May 08 2015 Matthias Runge <mrunge@redhat.com> - 2015.1.0-5
- fix region selector in -theme
- honor moved webroot a little better (rhbz#1218627)
- make sure, systemd service is reloaded (rhbz#1219006)

* Wed May 06 2015 Matthias Runge <mrunge@redhat.com> - 2015.1.0-3
- theme fixes

* Fri May 01 2015  2015.1.0-2
- Fixing data processing operations for alternate webroots (sahara)
  https://bugs.launchpad.net/horizon/+bug/1450535

* Thu Apr 30 2015 Alan Pevec <alan.pevec@redhat.com> 2015.1.0-1
- OpenStack Kilo release
