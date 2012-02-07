#
# This is 2012.1 essex-3 milestone
#
%global release_name essex
%global release_letter e
%global milestone 3

Name:       python-django-horizon
Version:    2012.1
Release:    0.1.%{release_letter}%{milestone}%{?dist}
Summary:    Django application for talking to Openstack

Group:      Development/Libraries
# Code in horizon/horizon/utils taken from django which is BSD
License:    ASL 2.0 and BSD
URL:        http://horizon.openstack.org
BuildArch:  noarch

Source0:    http://launchpad.net/horizon/%{release_name}/%{release_name}-%{milestone}/+download/horizon-%{version}~%{release_letter}%{milestone}.tar.gz
Source1:    openstack-dashboard.conf

# This was supposed to be in essex-3 but came 2 patches too late
Patch1:     %{name}-drop-openstackx.patch
# Dep is for testing only, so not required for a first run
Patch2:     %{name}-remove-test-dep.patch
# Place sqlite DB in /var/lib/openstack-dashboard
Patch3:     %{name}-db-var-path.patch

Requires:   Django >= 1.3.0
Requires:   openstack-glance >= 2012.1
Requires:   python-cloudfiles >= 1.7.9.3
Requires:   python-dateutil
Requires:   python-keystoneclient >= 2012.1
Requires:   python-novaclient >= 2012.1
Requires:   python-quantumclient >= 2012.1

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

BuildRequires: python-sphinx

# Doc building basically means we have to mirror Requires:
BuildRequires: openstack-glance
BuildRequires: python-cloudfiles >= 1.7.9.3
BuildRequires: python-dateutil
BuildRequires: python-keystoneclient
BuildRequires: python-novaclient >= 2012.1
BuildRequires: python-quantumclient


%description doc
Documentation for the Django Horizon application for talking with Openstack


%prep
%setup -q -n horizon-%{version}
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
pushd horizon
%{__python} setup.py build
popd

%install
pushd horizon
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
popd

install -m 0644 -D -p %{SOURCE1} %{buildroot}%{_sysconfdir}/httpd/conf.d/openstack-dashboard.conf

# This is needed for docs building
cp openstack-dashboard/local/local_settings.py.example \
   openstack-dashboard/local/local_settings.py

export PYTHONPATH="$( pwd ):$PYTHONPATH"
sphinx-build -b html docs/source html

# Fix hidden-file-or-dir warnings
rm -fr html/.doctrees html/.buildinfo

install -d -m 755 %{buildroot}%{_localstatedir}/openstack-dashboard
install -d -m 755 %{buildroot}%{_sysconfdir}/openstack-dashboard
rm openstack-dashboard/local/local_settings.py
cp openstack-dashboard/local/local_settings.py.example \
   %{buildroot}%{_sysconfdir}/openstack-dashboard/local_settings
ln -s %{_sysconfdir}/openstack-dashboard/local_settings \
      openstack-dashboard/local/local_settings.py

install -d -m 755 %{buildroot}%{_datadir}/openstack-dashboard
cp -r openstack-dashboard/dashboard %{buildroot}%{_datadir}/openstack-dashboard
cp -r openstack-dashboard/local %{buildroot}%{_datadir}/openstack-dashboard


%files
%{python_sitelib}/horizon
%{python_sitelib}/*.egg-info


%files -n openstack-dashboard
%{_datadir}/openstack-dashboard/
%{_localstatedir}/openstack-dashboard/
%config(noreplace) %{_sysconfdir}/httpd/conf.d/openstack-dashboard.conf
%config(noreplace) %{_sysconfdir}/openstack-dashboard/local_settings

%files doc
%doc html

%changelog
* Mon Jan 30 2012 Cole Robinson <crobinso@redhat.com> - 2012.1-0.1.e3
- Initial package
