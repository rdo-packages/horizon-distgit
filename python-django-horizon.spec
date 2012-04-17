#
# This is 2012.1 essex-3 milestone
#
%global release_name essex
%global release_letter rc
%global milestone 1
%global snapdate 20120304
%global git_revno 1447
%global snaptag ~%{release_letter}%{milestone}~%{snapdate}.%{git_revno}

Name:       python-django-horizon
Version:    2012.1
Release:    2%{?dist}
#Release:    0.1.%{?release_letter}%{milestone}%{?dist}
Summary:    Django application for talking to Openstack

Group:      Development/Libraries
# Code in horizon/horizon/utils taken from django which is BSD
License:    ASL 2.0 and BSD
URL:        http://horizon.openstack.org
BuildArch:  noarch

Source0:    http://launchpad.net/horizon/%{release_name}/+download/horizon-%{version}.tar.gz
#Source0:    http://launchpad.net/horizon/%{release_name}/%{release_name}-%{milestone}/+download/horizon-%{version}~%{?release_letter}%{milestone}.tar.gz
#Source0:    http://horizon.openstack.org/tarballs/horizon-%{version}%{snaptag}.tar.gz
Source1:    openstack-dashboard.conf

Patch1:     %{name}-disable-debug.patch
Patch2:     %{name}-default-db.patch
Patch3:     xss-in-log-viewer.patch

Requires:   Django >= 1.3.0
Requires:   openstack-glance >= 2012.1
Requires:   python-cloudfiles >= 1.7.9.3
Requires:   python-dateutil
Requires:   python-keystoneclient >= 2012.1
Requires:   python-novaclient >= 2012.1
Requires:   python-quantumclient >= 2012.1
Requires:   python-django-nose

BuildRequires: python2-devel
BuildRequires: python-setuptools


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
BuildRequires: openstack-glance
BuildRequires: python-cloudfiles >= 1.7.9.3
BuildRequires: python-dateutil
BuildRequires: python-keystoneclient
BuildRequires: python-novaclient >= 2012.1
BuildRequires: python-quantumclient
BuildRequires: python-django-nose

%description doc
Documentation for the Django Horizon application for talking with Openstack


%prep
%setup -q -n horizon-%{version}
%patch1 -p1
%patch3 -p1

%build
%{__python} setup.py build

%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

install -m 0644 -D -p %{SOURCE1} %{buildroot}%{_sysconfdir}/httpd/conf.d/openstack-dashboard.conf

export PYTHONPATH="$( pwd ):$PYTHONPATH"
sphinx-build -b html docs/source html

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


%post -n openstack-dashboard
python %{_datadir}/openstack-dashboard/manage.py syncdb >/dev/null 2>&1 || :
python %{_datadir}/openstack-dashboard/manage.py collectstatic --noinput >/dev/null 2>&1 || :

%files
%{python_sitelib}/horizon
%{python_sitelib}/*.egg-info

%files -n openstack-dashboard
%{_datadir}/openstack-dashboard/
%{_sharedstatedir}/openstack-dashboard
%{_sysconfdir}/openstack-dashboard
%config(noreplace) %{_sysconfdir}/httpd/conf.d/openstack-dashboard.conf
%config(noreplace) %{_sysconfdir}/openstack-dashboard/local_settings

%files doc
%doc html

%changelog
* Tue Apr 17 2012 Pádraig Brady <P@draigBrady.com> - 2012.1-2
- CVE-2012-2094 XSS vulnerability in Horizon log viewer

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
