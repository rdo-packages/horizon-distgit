%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x2426b928085a020d8a90d0d879ab7008d0896c8a

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
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
%{?python_provide:%python_provide python3-django-horizon}

BuildRequires:   python3-django >= 3.2
Requires:   python3-django >= 3.2


Requires:   python3-pytz
Requires:   python3-pbr

BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: python3-pbr >= 2.0.0
BuildRequires: git-core
BuildRequires: gettext

# for checks:
BuildRequires:   python3-django-nose
BuildRequires:   python3-nose
BuildRequires:   python3-osprofiler
BuildRequires:   python3-iso8601
BuildRequires:   python3-pycodestyle
BuildRequires:   python3-mock

BuildRequires:   python3-nose-exclude
BuildRequires:   python3-selenium
BuildRequires:   python3-netaddr
BuildRequires:   python3-anyjson


# additional provides to be consistent with other django packages
Provides: django-horizon = %{epoch}:%{version}-%{release}
Obsoletes: python-django-openstack-auth < 4.0.0-1
Obsoletes: python2-django-openstack-auth < 4.0.0-1
# (TODO) remove following provides once the requirements have been fixed
# in all dashboard plugins
Provides: python-django-openstack-auth = %{epoch}:%{version}-%{release}
Provides: python2-django-openstack-auth = %{epoch}:%{version}-%{release}

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
Requires:   python3-django-compressor >= 2.4.1

%if 0%{rhosp} == 0
Requires:   openstack-dashboard-theme >= %{epoch}:%{version}-%{release}
%else
%{lua: ver = rpm.expand("%version");
if ver == "XXX" then rpm.define("version_major " .. "%{version}"); else x, y = string.find(ver, "%.");
maj = string.sub(ver, 1, x-1); rpm.define("version_major " .. maj .. ".0.0"); end}
Requires:   openstack-dashboard-theme >= %{epoch}:%{version_major}
%endif

Requires:   python3-iso8601
Requires:   python3-glanceclient >= 1:2.8.0
Requires:   python3-keystoneclient >= 1:3.22.0
Requires:   python3-keystoneauth1 >= 4.3.1
Requires:   python3-novaclient >= 1:9.1.0
Requires:   python3-neutronclient >= 8.1.0
Requires:   python3-cinderclient >= 8.0.0
Requires:   python3-swiftclient >= 3.2.0
Requires:   python3-netaddr
Requires:   python3-osprofiler >= 3.4.2
Requires:   python3-django-pyscss >= 2.0.2
Requires:   python3-XStatic
Requires:   python3-XStatic-Angular >= 1:1.5.8.0
Requires:   python3-XStatic-Angular-Bootstrap
Requires:   python3-XStatic-Angular-Schema-Form
Requires:   python3-XStatic-D3
Requires:   python3-XStatic-Font-Awesome
Requires:   python3-XStatic-JSEncrypt
Requires:   python3-XStatic-Jasmine
Requires:   python3-XStatic-Bootstrap-SCSS >= 3.3.7.1
Requires:   python3-XStatic-termjs
Requires:   python3-XStatic-smart-table
Requires:   python3-XStatic-Angular-Gettext
Requires:   python3-XStatic-Angular-FileUpload
Requires:   python3-XStatic-bootswatch
Requires:   python3-XStatic-roboto-fontface >= 0.5.0.0
Requires:   python3-XStatic-mdi
Requires:   python3-XStatic-objectpath
Requires:   python3-XStatic-tv4
Requires:   python3-django-debreach

Requires:   python3-scss >= 1.4.0
Requires:   fontawesome-fonts-web >= 4.1.0

Requires:   python3-oslo-concurrency >= 4.5.0
Requires:   python3-oslo-config >= 8.8.0
Requires:   python3-oslo-i18n >= 5.1.0
Requires:   python3-oslo-serialization >= 4.3.0
Requires:   python3-oslo-utils >= 4.12.0
Requires:   python3-oslo-upgradecheck >= 1.5.0
Requires:   python3-requests >= 2.25.1
Requires:   python3-oslo-policy >= 3.11.0
Requires:   python3-babel
Requires:   python3-futurist

Requires:   openssl
Requires:   logrotate

Requires:   python3-mod_wsgi
Requires:   python3-django-appconf
Requires:   python3-lesscpy
Requires:   python3-semantic_version >= 2.3.1
Requires:   python3-XStatic-jQuery
Requires:   python3-XStatic-Hogan
Requires:   python3-XStatic-JQuery-Migrate
Requires:   python3-XStatic-JQuery-TableSorter
Requires:   python3-XStatic-JQuery-quicksearch
Requires:   python3-XStatic-Rickshaw
Requires:   python3-XStatic-Spin
Requires:   python3-XStatic-jquery-ui
Requires:   python3-XStatic-Bootstrap-Datepicker
Requires:   python3-XStatic-Angular-lrdragndrop
Requires:   python3-XStatic-Magic-Search
# python3-yaml >= 6.0 is required, but not available
Requires:   python3-yaml >= 3.12
Requires:   python3-memcached
Requires:   python3-debtcollector >= 1.2.0

BuildRequires: python3-django-debreach
BuildRequires: python3-django-compressor >= 2.4.1
BuildRequires: python3-django-pyscss >= 2.0.2
BuildRequires: python3-XStatic
BuildRequires: python3-XStatic-Angular >= 1:1.5.8.0
BuildRequires: python3-XStatic-Angular-Bootstrap
BuildRequires: python3-XStatic-Angular-Schema-Form
BuildRequires: python3-XStatic-D3
BuildRequires: python3-XStatic-Font-Awesome
BuildRequires: python3-XStatic-JSEncrypt
BuildRequires: python3-XStatic-Jasmine
BuildRequires: python3-XStatic-Bootstrap-SCSS
BuildRequires: python3-XStatic-termjs
BuildRequires: python3-XStatic-smart-table
BuildRequires: python3-XStatic-Angular-FileUpload
BuildRequires: python3-XStatic-Angular-Gettext
BuildRequires: python3-XStatic-bootswatch
BuildRequires: python3-XStatic-roboto-fontface
BuildRequires: python3-XStatic-mdi
BuildRequires: python3-XStatic-objectpath
BuildRequires: python3-XStatic-tv4
# bootstrap-scss requires at least python-scss >= 1.2.1
BuildRequires: python3-scss >= 1.3.5
BuildRequires: fontawesome-fonts-web >= 4.1.0
BuildRequires: python3-oslo-concurrency
BuildRequires: python3-oslo-config
BuildRequires: python3-oslo-i18n
BuildRequires: python3-oslo-serialization
BuildRequires: python3-oslo-utils
BuildRequires: python3-oslo-policy
BuildRequires: python3-babel

BuildRequires: python3-pytz
BuildRequires: systemd

BuildRequires: python3-django-appconf
BuildRequires: python3-lesscpy
BuildRequires: python3-semantic_version
BuildRequires: python3-XStatic-jQuery
BuildRequires: python3-XStatic-Hogan
BuildRequires: python3-XStatic-JQuery-Migrate
BuildRequires: python3-XStatic-JQuery-TableSorter
BuildRequires: python3-XStatic-JQuery-quicksearch
BuildRequires: python3-XStatic-Rickshaw
BuildRequires: python3-XStatic-Spin
BuildRequires: python3-XStatic-jquery-ui
BuildRequires: python3-XStatic-Bootstrap-Datepicker
BuildRequires: python3-XStatic-Angular-lrdragndrop
BuildRequires: python3-XStatic-Magic-Search
BuildRequires: python3-pint
BuildRequires: python3-memcached
BuildRequires: python3-glanceclient
BuildRequires: python3-keystoneclient
BuildRequires: python3-novaclient >= 1:9.1.0
BuildRequires: python3-neutronclient
BuildRequires: python3-cinderclient
BuildRequires: python3-swiftclient
BuildRequires: python3-pytest

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
BuildRequires: python3-sphinx >= 1.1.3

# Doc building basically means we have to mirror Requires:
BuildRequires: python3-openstackdocstheme

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
# Let RPM handle the dependencies
rm -f {,test-}requirements.txt

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

# Fix manage.py shebang
sed -i 's/\/usr\/bin\/env python/\/usr\/bin\/env python3/' manage.py

# Fix python executable depending on python version
sed -i 's/\/usr\/bin\/python /\/usr\/bin\/python3 /g' %{SOURCE3}

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
%{py3_build}

# compress css, js etc.
cp openstack_dashboard/local/local_settings.py.example openstack_dashboard/local/local_settings.py
# get it ready for compressing later in puppet-horizon
%{__python3} manage.py collectstatic --noinput --clear
%{__python3} manage.py compress --force

%if 0%{?with_doc}
# build docs
export PYTHONPATH=.
sphinx-build -b html doc/source html
# Fix hidden-file-or-dir warnings
rm -fr html/.doctrees html/.buildinfo
%endif
# undo hack
cp openstack_dashboard/local/local_settings.py.example openstack_dashboard/local/local_settings.py


%install
%{py3_install}

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

%check
# NOTE(jpena): we do not want to run hacking tests in check
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
%{python3_sitelib}/*.egg-info
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
%doc html
%license LICENSE
%endif

%if 0%{rhosp} == 0
%files -n openstack-dashboard-theme
#%{_datadir}/openstack-dashboard/openstack_dashboard/dashboards/theme
#%{_datadir}/openstack-dashboard/openstack_dashboard/enabled/_99_customization.*
%endif

%changelog

