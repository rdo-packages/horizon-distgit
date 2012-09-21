Name:       python-django-horizon
Version:    2012.2
Release:    0.6.rc1%{?dist}
Summary:    Django application for talking to Openstack

Group:      Development/Libraries
# Code in horizon/horizon/utils taken from django which is BSD
License:    ASL 2.0 and BSD
URL:        http://horizon.openstack.org/
BuildArch:  noarch

Source0:    http://launchpad.net/horizon/folsom/folsom-rc1/+download/horizon-2012.2~rc1.tar.gz
Source1:    openstack-dashboard.conf

# offline compressed css, js
Source2:    python-django-horizon-compressed-css.tar.gz

# change settings to use offline compression
Patch0:     python-django-horizon-dashboard-settings.patch
# disable debug also in local_settings.py
Patch1:     python-django-horizon-disable-debug.patch

# take variables out of compressed output
Patch2:     python-django-horizon-template_conf.patch
Requires:   python-django
Requires:   python-cloudfiles >= 1.7.9.3
Requires:   python-dateutil
Requires:   python-glanceclient
Requires:   python-keystoneclient 
Requires:   python-novaclient >= 2012.1
Requires:   python-quantumclient
Requires:   python-cinderclient
Requires:   python-swiftclient

BuildRequires: python2-devel
BuildRequires: python-setuptools

# for checks:
#BuildRequires:   python-django-nose
#BuildRequires:   python-cinderclient
#BuildRequires:   python-django-appconf
#BuildRequires:   python-django-openstack-auth
#BuildRequires:   python-django-compressor

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
Requires:   python-django-openstack-auth
Requires:   python-django-compressor

BuildRequires: python2-devel

%description -n openstack-dashboard
Openstack Dashboard is a web user interface for Openstack. The package
provides a reference implementation using the Django Horizon project,
mostly consisting of JavaScript and CSS to tie it altogether as a standalone
site.


%package doc
Summary:    Documentation for Django Horizon
Group:      Documentation

Requires:   %{name} = %{version}-%{release}

BuildRequires: python-sphinx >= 1.1.3

# Doc building basically means we have to mirror Requires:
BuildRequires: python-cloudfiles >= 1.7.9.3
BuildRequires: python-dateutil
BuildRequires: python-glanceclient
BuildRequires: python-keystoneclient
BuildRequires: python-novaclient >= 2012.1
BuildRequires: python-quantumclient

%description doc
Documentation for the Django Horizon application for talking with Openstack


%prep
%setup -q -n horizon-%{version}

# remove unnecessary .po files
find . -name "django*.po" -exec rm -f '{}' \;

# patch settings
%patch0 -p1
# disable debug also in local_settings.py
%patch1 -p1

# correct compressed output
%patch2 -p1

%build
%{__python} setup.py build

%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

install -m 0644 -D -p %{SOURCE1} %{buildroot}%{_sysconfdir}/httpd/conf.d/openstack-dashboard.conf

export PYTHONPATH="$( pwd ):$PYTHONPATH"
sphinx-build -b html doc/source html

# Fix hidden-file-or-dir warnings
rm -fr html/.doctrees html/.buildinfo

install -d -m 755 %{buildroot}%{_datadir}/openstack-dashboard
install -d -m 755 %{buildroot}%{_sharedstatedir}/openstack-dashboard
install -d -m 755 %{buildroot}%{_sysconfdir}/openstack-dashboard

# Copy everything to /usr/share
mv %{buildroot}%{python_sitelib}/openstack_dashboard \
   %{buildroot}%{_datadir}/openstack-dashboard
mv manage.py %{buildroot}%{_datadir}/openstack-dashboard
rm -rf %{buildroot}%{python_sitelib}/openstack_dashboard


# Move config to /etc, symlink it back to /usr/share
mv %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/local/local_settings.py.example %{buildroot}%{_sysconfdir}/openstack-dashboard/local_settings
ln -s %{_sysconfdir}/openstack-dashboard/local_settings %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/local/local_settings.py

%find_lang django
grep "\/usr\/share\/openstack-dashboard" django.lang > dashboard.lang
grep "\/site-packages\/horizon" django.lang > horizon.lang

# finally put compressed js, css to the right place
cd %{buildroot}%{_datadir}/openstack-dashboard
tar xzf %{SOURCE2}

%post -n openstack-dashboard
python %{_datadir}/openstack-dashboard/manage.py syncdb >/dev/null 2>&1 || :
python %{_datadir}/openstack-dashboard/manage.py collectstatic --noinput >/dev/null 2>&1 || :

%files -f horizon.lang
%dir %{python_sitelib}/horizon
%{python_sitelib}/horizon/*.py*
%{python_sitelib}/horizon/api
%{python_sitelib}/horizon/browsers
%{python_sitelib}/horizon/conf
%{python_sitelib}/horizon/dashboards
%{python_sitelib}/horizon/forms
%{python_sitelib}/horizon/management
%{python_sitelib}/horizon/openstack
%{python_sitelib}/horizon/static
%{python_sitelib}/horizon/tables
%{python_sitelib}/horizon/tabs
%{python_sitelib}/horizon/templates
%{python_sitelib}/horizon/templatetags
%{python_sitelib}/horizon/tests
%{python_sitelib}/horizon/usage
%{python_sitelib}/horizon/utils
%{python_sitelib}/horizon/views
%{python_sitelib}/horizon/workflows
%{python_sitelib}/*.egg-info
%exclude %{python_sitelib}/bin

%files -n openstack-dashboard -f dashboard.lang
%dir %{_datadir}/openstack-dashboard/
%{_datadir}/openstack-dashboard/*.py*
%{_datadir}/openstack-dashboard/static
%{_datadir}/openstack-dashboard/openstack_dashboard/*.py*
%{_datadir}/openstack-dashboard/openstack_dashboard/local
%{_datadir}/openstack-dashboard/openstack_dashboard/static
%{_datadir}/openstack-dashboard/openstack_dashboard/templates
%{_datadir}/openstack-dashboard/openstack_dashboard/test
%{_datadir}/openstack-dashboard/openstack_dashboard/wsgi

%{_sharedstatedir}/openstack-dashboard
%dir %{_sysconfdir}/openstack-dashboard
%config(noreplace) %{_sysconfdir}/httpd/conf.d/openstack-dashboard.conf
%config(noreplace) %{_sysconfdir}/openstack-dashboard/local_settings

%files doc
%doc html

%changelog
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
