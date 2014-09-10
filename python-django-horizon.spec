%global release_name juno
%global milestone 3

%global with_compression 1
Name:       python-django-horizon
Version:    2014.2
Release:    0.4.b%{milestone}%{?dist}
Summary:    Django application for talking to Openstack

Group:      Development/Libraries
# Code in horizon/horizon/utils taken from django which is BSD
License:    ASL 2.0 and BSD
URL:        http://horizon.openstack.org/
Source0:    http://launchpad.net/horizon/%{release_name}/%{release_name}-%{milestone}/+download/horizon-%{version}.b%{milestone}.tar.gz
Source1:    openstack-dashboard.conf
Source2:    openstack-dashboard-httpd-2.4.conf

# demo config for separate logging
Source4:    openstack-dashboard-httpd-logging.conf

# logrotate config
Source5:    python-django-horizon-logrotate.conf

#
# patches_base=2014.2.b3
#
Patch0001: 0001-Don-t-access-the-net-while-building-docs.patch
Patch0002: 0002-disable-debug-move-web-root.patch
Patch0003: 0003-change-lockfile-location-to-tmp-and-also-add-localho.patch
Patch0004: 0004-Add-a-customization-module-based-on-RHOS.patch
Patch0005: 0005-move-RBAC-policy-files-and-checks-to-etc-openstack-d.patch
Patch0006: 0006-move-SECRET_KEY-secret_key_store-to-tmp.patch
Patch0007: 0007-RCUE-navbar-and-login-screen.patch
Patch0008: 0008-fix-flake8-issues.patch
Patch0009: 0009-remove-runtime-dep-to-python-pbr.patch
Patch0010: 0010-Add-Change-password-link-to-the-RCUE-theme.patch
Patch0011: 0011-.less-replaced-in-rcue.patch

#
# BuildArch needs to be located below patches in the spec file. Don't ask!
#

BuildArch:  noarch

BuildRequires:   Django
Requires:   Django


Requires:   python-dateutil
Requires:   pytz
Requires:   python-lockfile
Requires:   python-six >= 1.7.0

BuildRequires: python2-devel
BuildRequires: python-setuptools
BuildRequires: python-d2to1
BuildRequires: python-pbr >= 0.7.0
BuildRequires: python-lockfile
BuildRequires: python-eventlet
BuildRequires: git
BuildRequires: python-six >= 1.7.0

# for checks:
%if 0%{?rhel} == 0
BuildRequires:   python-django-nose >= 1.2
BuildRequires:   python-coverage
BuildRequires:   python-mox
BuildRequires:   python-nose-exclude
BuildRequires:   python-nose
BuildRequires:   python-selenium
%endif
BuildRequires:   python-netaddr
BuildRequires:   python-kombu
BuildRequires:   python-anyjson
BuildRequires:   python-iso8601


# additional provides to be consistent with other django packages
Provides: django-horizon = %{version}-%{release}

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
Requires:   python-django-horizon >= %{version}
Requires:   python-django-openstack-auth >= 1.1.6
Requires:   python-django-compressor >= 1.3
Requires:   python-django-appconf
%if %{?with_compression} > 0
Requires:   python-lesscpy
%endif

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
Requires:   python-django-pyscss
Requires:   python-XStatic
Requires:   python-XStatic-jQuery

Requires:   logrotate

BuildRequires: python-django-openstack-auth >= 1.1.6
BuildRequires: python-django-compressor >= 1.3
BuildRequires: python-django-appconf
BuildRequires: python-lesscpy
BuildRequires: python-oslo-config
BuildRequires: python-django-pyscss
BuildRequires: python-XStatic
BuildRequires: python-XStatic-jQuery

BuildRequires: pytz

%description -n openstack-dashboard
Openstack Dashboard is a web user interface for Openstack. The package
provides a reference implementation using the Django Horizon project,
mostly consisting of JavaScript and CSS to tie it altogether as a standalone
site.


%package doc
Summary:    Documentation for Django Horizon
Group:      Documentation

Requires:   %{name} = %{version}-%{release}
%if 0%{?rhel}==6
BuildRequires: python-sphinx10
%else
BuildRequires: python-sphinx >= 1.1.3
%endif

# Doc building basically means we have to mirror Requires:
BuildRequires: python-dateutil
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
BuildRequires: python-oslo-sphinx

%description doc
Documentation for the Django Horizon application for talking with Openstack

%package -n openstack-dashboard-theme
Summary: OpenStack web user interface reference implementation theme module
Requires: openstack-dashboard = %{version}

%description -n openstack-dashboard-theme
Customization module for OpenStack Dashboard to provide a branded logo.

%prep
%setup -q -n horizon-%{version}.b%{milestone}
# Use git to manage patches.
# http://rwmj.wordpress.com/2011/08/09/nice-rpm-git-patch-management-trick/
git init
git config user.email "python-django-horizon-owner@fedoraproject.org"
git config user.name "python-django-horizon"
git add .
git commit -a -q -m "%{version} baseline"
git am %{patches}

# remove unnecessary .po files
find . -name "django*.po" -exec rm -f '{}' \;

sed -i s/REDHATVERSION/%{version}/ horizon/version.py
sed -i s/REDHATRELEASE/%{release}/ horizon/version.py

# Remove the requirements file so that pbr hooks don't add it
# to distutils requires_dist config
rm -rf {test-,}requirements.txt tools/{pip,test}-requires

# make doc build compatible with python-oslo-sphinx RPM
sed -i 's/oslosphinx/oslo.sphinx/' doc/source/conf.py

# drop config snippet
cp -p %{SOURCE4} .

%if 0%{?with_compression} > 0
# set COMPRESS_OFFLINE=True
sed -i 's:COMPRESS_OFFLINE = False:COMPRESS_OFFLINE = True:' openstack_dashboard/settings.py
%else
# set COMPRESS_OFFLINE=False
sed -i 's:COMPRESS_OFFLINE = True:COMPRESS_OFFLINE = False:' openstack_dashboard/settings.py
%endif



%build
%{__python} setup.py build

# compress css, js etc.
cp openstack_dashboard/local/local_settings.py.example openstack_dashboard/local/local_settings.py
# dirty hack to make SECRET_KEY work:
#sed -i 's:^SECRET_KEY =.*:SECRET_KEY = "badcafe":' openstack_dashboard/local/local_settings.py
%{__python} manage.py collectstatic --noinput 

# offline compression
%if 0%{?with_compression} > 0
%{__python} manage.py compress 
cp -a static/dashboard %{_builddir}
%endif

cp -a static/dashboard %{_builddir}

# build docs
export PYTHONPATH="$( pwd ):$PYTHONPATH"
%if 0%{?rhel}==6
sphinx-1.0-build -b html doc/source html
%else
sphinx-build -b html doc/source html
%endif

# undo hack
cp openstack_dashboard/local/local_settings.py.example openstack_dashboard/local/local_settings.py

# Fix hidden-file-or-dir warnings
rm -fr html/.doctrees html/.buildinfo

%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

# drop httpd-conf snippet
%if 0%{?rhel} <7 && 0%{?fedora} <18
install -m 0644 -D -p %{SOURCE1} %{buildroot}%{_sysconfdir}/httpd/conf.d/openstack-dashboard.conf
%else
# httpd-2.4 changed the syntax
install -m 0644 -D -p %{SOURCE2} %{buildroot}%{_sysconfdir}/httpd/conf.d/openstack-dashboard.conf
%endif
install -d -m 755 %{buildroot}%{_datadir}/openstack-dashboard
install -d -m 755 %{buildroot}%{_sharedstatedir}/openstack-dashboard
install -d -m 755 %{buildroot}%{_sysconfdir}/openstack-dashboard


# Copy everything to /usr/share
mv %{buildroot}%{python_sitelib}/openstack_dashboard \
   %{buildroot}%{_datadir}/openstack-dashboard
cp manage.py %{buildroot}%{_datadir}/openstack-dashboard
rm -rf %{buildroot}%{python_sitelib}/openstack_dashboard

# move customization stuff to /usr/share
mv openstack_dashboard/dashboards/theme %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/dashboards/
mv openstack_dashboard/enabled/_99_customization.py %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/enabled


# Move config to /etc, symlink it back to /usr/share
mv %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/local/local_settings.py.example %{buildroot}%{_sysconfdir}/openstack-dashboard/local_settings
ln -s ../../../../../%{_sysconfdir}/openstack-dashboard/local_settings %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/local/local_settings.py

mv %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/conf/*.json %{buildroot}%{_sysconfdir}/openstack-dashboard

%if 0%{?rhel} > 6 || 0%{?fedora} >= 16
%find_lang django
%find_lang djangojs
%else
# Handling locale files
# This is adapted from the %%find_lang macro, which cannot be directly
# used since Django locale files are not located in %%{_datadir}
#
# The rest of the packaging guideline still apply -- do not list
# locale files by hand!
(cd $RPM_BUILD_ROOT && find . -name 'django*.mo') | %{__sed} -e 's|^.||' |
%{__sed} -e \
   's:\(.*/locale/\)\([^/_]\+\)\(.*\.mo$\):%lang(\2) \1\2\3:' \
      >> django.lang
%endif

grep "\/usr\/share\/openstack-dashboard" django.lang > dashboard.lang
grep "\/site-packages\/horizon" django.lang > horizon.lang

%if 0%{?rhel} > 6 || 0%{?fedora} >= 16
cat djangojs.lang >> horizon.lang
%endif

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
#sed -i 's:^SECRET_KEY =.*:SECRET_KEY = "badcafe":' openstack_dashboard/local/local_settings.py

# until django-1.6 support for tests is enabled, disable tests
./run_tests.sh -N -P
%endif

%files -f horizon.lang
%doc LICENSE README.rst openstack-dashboard-httpd-logging.conf
%dir %{python_sitelib}/horizon
%{python_sitelib}/horizon/*.py*
%{python_sitelib}/horizon/browsers
%{python_sitelib}/horizon/conf
%{python_sitelib}/horizon/forms
%{python_sitelib}/horizon/management
%{python_sitelib}/horizon/static
%{python_sitelib}/horizon/tables
%{python_sitelib}/horizon/tabs
%{python_sitelib}/horizon/templates
%{python_sitelib}/horizon/templatetags
%{python_sitelib}/horizon/test
%{python_sitelib}/horizon/utils
%{python_sitelib}/horizon/workflows
%{python_sitelib}/*.egg-info

%files -n openstack-dashboard -f dashboard.lang
%dir %{_datadir}/openstack-dashboard/
%{_datadir}/openstack-dashboard/*.py*
%{_datadir}/openstack-dashboard/static
%{_datadir}/openstack-dashboard/openstack_dashboard/*.py*
%{_datadir}/openstack-dashboard/openstack_dashboard/api
%{_datadir}/openstack-dashboard/openstack_dashboard/dashboards/admin
%{_datadir}/openstack-dashboard/openstack_dashboard/dashboards/project
%{_datadir}/openstack-dashboard/openstack_dashboard/dashboards/router
%{_datadir}/openstack-dashboard/openstack_dashboard/dashboards/settings
%{_datadir}/openstack-dashboard/openstack_dashboard/dashboards/__init__.py*
%{_datadir}/openstack-dashboard/openstack_dashboard/enabled
%exclude %{_datadir}/openstack-dashboard/openstack_dashboard/enabled/_99_customization.*
%{_datadir}/openstack-dashboard/openstack_dashboard/local
%{_datadir}/openstack-dashboard/openstack_dashboard/openstack
%{_datadir}/openstack-dashboard/openstack_dashboard/static
%{_datadir}/openstack-dashboard/openstack_dashboard/templates
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

%dir %attr(0750, root, apache) %{_sysconfdir}/openstack-dashboard
%dir %attr(0750, apache, apache) %{_sharedstatedir}/openstack-dashboard
%dir %attr(0750, apache, apache) %{_var}/log/horizon
%config(noreplace) %{_sysconfdir}/httpd/conf.d/openstack-dashboard.conf
%config(noreplace) %attr(0640, root, apache) %{_sysconfdir}/openstack-dashboard/local_settings
%config(noreplace) %attr(0640, root, apache) %{_sysconfdir}/openstack-dashboard/cinder_policy.json
%config(noreplace) %attr(0640, root, apache) %{_sysconfdir}/openstack-dashboard/keystone_policy.json
%config(noreplace) %attr(0640, root, apache) %{_sysconfdir}/openstack-dashboard/nova_policy.json
%config(noreplace) %attr(0640, root, apache) %{_sysconfdir}/openstack-dashboard/glance_policy.json
%config(noreplace) %attr(0640, root, apache) %{_sysconfdir}/openstack-dashboard/neutron_policy.json
%config(noreplace) %attr(0640, root, apache) %{_sysconfdir}/openstack-dashboard/heat_policy.json
%{_sysconfdir}/logrotate.d/openstack-dashboard

%files doc
%doc html

%files -n openstack-dashboard-theme
%{_datadir}/openstack-dashboard/openstack_dashboard/dashboards/theme
%{_datadir}/openstack-dashboard/openstack_dashboard/enabled/_99_customization.*

%changelog
* Tue Sep 09 2014 Matthias Runge <mrunge@redhat.com> - 2014.2-0.3.b2
- add logrotate script

* Thu Jul 31 2014 Matthias Runge <mrunge@redhat.com> 2014.2-0.2
- rebase to Juno-2

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2014.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 05 2014 Matthias Runge <mrunge@redhat.com> - 2014.1-4
- fix typo
- Add missing comma in Volume ResourceWrapper class

* Fri May 02 2014 Alan Pevec <apevec@redhat.com> - 2014.1-3
- remove requirement to python-pbr

* Fri Apr 18 2014 Matthias Runge <mrunge@redhat.com> - 2014.1-1
- rebase to 2014.1

* Tue Apr 08 2014 Matthias Runge <mrunge@redhat.com> - 2014.1-0.14.rc2
- rebase to 2014.1.rc2

* Tue Apr 08 2014 Matthias Runge <mrunge@redhat.com> - 2014.1-0.13.rc1
- own openstack_dashboard/enabled/_99_customization.py? in the right
  package (rhbz#1085344)

* Fri Apr 04 2014 Matthias Runge <mrunge@redhat.com> - 2014.1-0.12.rc1
- rebase to horizon-2014.1.rc1
- remove runtime requirement to mox (rhbz#1080326)

* Wed Apr 02 2014 Matthias Runge <mrunge@redhat.com> - 2014.1-0.11.b3
- No images/javascript in horizon dashboard (rhbz#1081612)
- skip selenium tests during build

* Tue Apr 01 2014 Matthias Runge <mrunge@redhat.com> - 2014.1-0.10.b3
- Failed to create a tenant (rhbz#1082646)
- add Red Hat Access to the upper right corner based on RCUE (rhbz#1069316)
- lower keystoneclient requirement until rc-1 build

* Fri Mar 28 2014 Matthias Runge <mrunge@redhat.com> - 2014.1-0.9.b3
- re-enable tests
- increase requirements versions

* Thu Mar 27 2014 Matthias Runge <mrunge@redhat.com> - 2014.1-0.8.b3
- disable tests until lp bug 1298332 is resolved

* Thu Mar 27 2014 Matthias Runge <mrunge@redhat.com> - 2014.1-0.7.b3
- cleanup and re-enable tests

* Wed Mar 26 2014 Matthias Runge <mrunge@redhat.com> - 2014.1-0.6.b3
- move theme to dashboards/theme

* Tue Mar 25 2014 Pádraig Brady <pbrady@redhat.com> - 2014.1-0.5.b3
- add dependency on python-mox

* Thu Mar 13 2014 Matthias Runge <mrunge@redhat.com> - 2014.1-0.4.b3
- remove hard selenium requirement for tests

* Fri Mar 07 2014 Matthias Runge <mrunge@redhat.com> - 2014.1-0.3.b3
- rebase to 2014.1.b3

* Sun Feb 02 2014 Matthias Runge <mrunge@redhat.com> - 2014.1-0.2b2
- rebase to 2014.1.b2
- make compression conditional

* Fri Dec 06 2013 Matthias Runge <mrunge@redhat.com> - 2014.1-0.1b1
- rebase to 2014.1.b1

* Mon Dec 02 2013 Matthias Runge <mrunge@redhat.com> - 2013.2-4
- fixes CVE-2013-6406 (rhbz#1035913)

* Wed Nov 13 2013 Matthias Runge <mrunge@redhat.com> - 2013.2-3
- add requirement python-pbr

* Fri Oct 18 2013 Matthias Runge <mrunge@redhat.com> - 2013.2-2
- update to Horizon-2013.2 release
- require python-eventlet
- create /var/log/horizon

* Thu Oct 17 2013 Matthias Runge <mrunge@redhat.com> - 2013.2.0.15.rc3
- rebase to Havana rc3

* Tue Oct 15 2013 Matthias Runge <mrunge@redhat.com> - 2013.2-0.14.rc2
- rebase to Havana-rc2

* Fri Oct 04 2013 Matthias Runge <mrunge@redhat.com> - 2013.2-0.12.rc1
- update to Havana-rc1
- move secret_keystone to /var/lib/openstack-dashboard

* Thu Sep 19 2013 Matthias Runge <mrunge@redhat.com> - 2013.2-0.11b3
- add BuildRequires python-eventlet to fix ./manage.py issue during build
- fix import in rhteme.less

* Mon Sep 09 2013 Matthias Runge <mrunge@redhat.com> - 2013.2-0.10b3
- Havana-3 snapshot
- drop node.js and node-less from buildrequirements
- add runtime requirement python-lesscpy
- own openstack_dashboard dir
- fix keystore handling issue

* Wed Aug 28 2013 Matthias Runge <mrunge@redhat.com> - 2013.2-0.8b2
- add a -custom subpackage to use a custom logo

* Mon Aug 26 2013 Matthias Runge <mrunge@redhat.com> - 2013.2-0.7b2
- enable tests in check section (rhbz#856182)

* Wed Aug 07 2013 Matthias Runge <mrunge@redhat.com> - 2013.2-0.5b2
- move requirements from horizon to openstack-dashboard package
- introduce explicit requirements for dependencies

* Thu Jul 25 2013 Matthias Runge <mrunge@redhat.com> - 2013.2-0.4b2
- havana-2
- change requirements from python-quantumclient to neutronclient
- require python-ceilometerclient
- add requirement python-lockfile, change lockfile location to /tmp

* Thu Jun 06 2013 Matthias Runge <mrunge@redhat.com> - 2013.2-0.2b1
- havana doesn't require explicitly Django-1.4

* Fri May 31 2013 Matthias Runge <mrunge@redhat.com> - 2013.2-0.1b1
- prepare for havana-1

* Mon May 13 2013 Matthias Runge <mrunge@redhat.com> - 2013.1.1-1
- change buildrequires from lessjs to nodejs-less
- update to 2013.1.1

* Fri Apr 05 2013 Matthias Runge <mrunge@redhat.com> - 2013.1-2
- explicitly require python-django14

* Fri Apr 05 2013 Matthias Runge <mrunge@redhat.com> - 2013.1-1
- update to 2013.1 

* Fri Mar 08 2013 Matthias Runge <mrunge@redhat.com> - 2013.1-0.6.g3
- fix syntax error in config

* Wed Feb 27 2013 Matthias Runge <mrunge@redhat.com> - 2013.1-0.5.g3
- update to grizzly-3

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2013.1-0.4.g2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jan 19 2013 Matthias Runge <mrunge@redhat.com> - 2013.1-0.4.g2
- update to grizzly-2
- fix compression during build

* Mon Jan 07 2013 Matthias Runge <mrunge@redhat.com> - 2013.1-0.3.g1
- use nodejs/lessjs to compress

* Fri Dec 14 2012 Matthias Runge <mrunge@redhat.com> - 2013.1-0.2.g1
- add config example snippet to enable logging to separate files

* Thu Nov 29 2012 Matthias Runge <mrunge@redhat.com> - 2013.1-0.1.g1
- update to grizzly-1 milestone

* Tue Nov 13 2012 Matthias Runge <mrunge@redhat.com> - 2012.2-4
- drop dependency to python-cloudfiles
- fix /etc/openstack-dashboard permission CVE-2012-5474 (rhbz#873120)

* Mon Oct 22 2012 Matthias Runge <mrunge@redhat.com> - 2012.2-3
- require Django14 for EPEL6
- finally move login/logout to /dashboard/auth/login
- adapt httpd config to httpd-2.4 (bz 868408)

* Mon Oct 15 2012 Matthias Runge <mrunge@redhat.com> - 2012.2-2
- fix static img, static fonts issue

* Wed Sep 26 2012 Matthias Runge <mrunge@redhat.com> - 2012.2-0.10.rc2
- more el6 compatibility

* Tue Sep 25 2012 Matthias Runge <mrunge@redhat.com> - 2012.2-0.9.rc2
- remove %%post section

* Mon Sep 24 2012 Matthias Runge <mrunge@redhat.com> - 2012.2-0.8.rc2
- also require pytz

* Fri Sep 21 2012 Matthias Runge <mrunge@redhat.com> - 2012.2-0.7.rc2
- update to release folsom rc2

* Fri Sep 21 2012 Matthias Runge <mrunge@redhat.com> - 2012.2-0.6.rc1
- fix compressing issue

* Mon Sep 17 2012 Matthias Runge <mrunge@redhat.com> - 2012.2-0.5.rc1
- update to folsom rc1
- require python-django instead of Django
- add requirements to python-django-compressor, python-django-openstack-auth
- add requirements to python-swiftclient
- use compressed js, css files

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2012.2-0.4.f1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 26 2012 Matthias Runge <mrunge@matthias-runge.de> - 2012.2-0.3.f1
- add additional provides django-horizon

* Wed Jun 06 2012 Pádraig Brady <P@draigBrady.com> - 2012.2-0.2.f1
- Update to folsom milestone 1

* Wed May 09 2012 Alan Pevec <apevec@redhat.com> - 2012.1-4
- Remove the currently uneeded dependency on python-django-nose

* Thu May 03 2012 Pádraig Brady <P@draigBrady.com> - 2012.1-3
- CVE-2012-2144 session reuse vulnerability

* Tue Apr 17 2012 Pádraig Brady <P@draigBrady.com> - 2012.1-2
- CVE-2012-2094 XSS vulnerability in Horizon log viewer
- Configure the default database to use

* Mon Apr 09 2012 Cole Robinson <crobinso@redhat.com> - 2012.1-1
- Update to essex final release
- Package manage.py (bz 808219)
- Properly access all needed javascript (bz 807567)

* Sat Mar 03 2012 Cole Robinson <crobinso@redhat.com> - 2012.1-0.1.rc1
- Update to rc1 snapshot
- Drop no longer needed packages
- Change default URL to http://localhost/dashboard
- Add dep on newly packaged python-django-nose
- Fix static content viewing (patch from Jan van Eldik) (bz 788567)

* Mon Jan 30 2012 Cole Robinson <crobinso@redhat.com> - 2012.1-0.1.e3
- Initial package
