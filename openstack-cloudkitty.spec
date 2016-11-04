%global service cloudkitty
Name:           openstack-cloudkitty
Version:        0.6.1
Release:        1%{?dist}
Summary:        OpenStack Billing and Usage Reporter

License:        ASL 2.0
URL:            https://wiki.openstack.org/wiki/CloudKitty
Source0:        https://tarballs.openstack.org/%{service}/%{service}-%{version}.tar.gz
Source1:        openstack-cloudkitty-api.service
Source2:        openstack-cloudkitty-processor.service


BuildArch:      noarch
BuildRequires:  python2-setuptools
BuildRequires:  python2-devel

BuildRequires:  python-oslo-config

Requires:       python-pbr
Requires:       python-alembic
Requires:       python-eventlet
Requires:       python-keystonemiddleware
Requires:       python-ceilometerclient
Requires:       python-gnocchiclient
Requires:       python-keystoneauth1
Requires:       python-iso8601
Requires:       python-PasteDeploy
Requires:       python-pecan
Requires:       python-WSME
Requires:       python-oslo-config
Requires:       python-oslo-context
Requires:       python-oslo-concurrency
Requires:       python-oslo-db
Requires:       python-oslo-i18n
Requires:       python-oslo-messaging
Requires:       python-oslo-middleware
Requires:       python-oslo-policy
Requires:       python-oslo-utils
Requires:       python-sqlalchemy
Requires:       python-six
Requires:       python-stevedore
Requires:       python-tooz

%description
Rating as a Service component

CloudKitty aims at filling the gap between metrics collection systems like
ceilometer and a billing system.

Every metrics are collected, aggregated and processed through different
rating modules. You can then query CloudKitty's storage to retrieve
processed data and easily generate reports.

Most parts of CloudKitty are modular so you can easily extend the base code
to address your particular use case.

%package api
Summary: cloudkitty api service

Requires: %{name} == %{version}-%{release}

%description api
%{summary}

%package processor
Summary: cloudkitty processor service
Requires: %{name} == %{version}-%{release}

%description processor
%{summary}


%prep
%autosetup -n %{service}-%{version}


%build
%py2_build


%install
%py2_install

# setup directories and config
install -d -m 755 %{buildroot}%{_sysconfdir}/cloudkitty
install -d -m 755 %{buildroot}%{_localstatedir}/log/cloudkitty

# install systemd units

install -p -D -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}-api.service
install -p -D -m 644 %{SOURCE2} %{buildroot}%{_unitdir}/%{name}-processor.service

%post api
%systemd_post %{name}-api.service

%preun api
%systemd_preun %{name}-api.service

%post processor
%systemd_post %{name}-processor.service

%preun processor
%systemd_preun %{name}-processor.service

%files
%license LICENSE
%doc README.rst
%{python2_sitelib}
%{_bindir}/%{service}-dbsync
%{_bindir}/%{service}-storage-init
%{_bindir}/%{service}-writer

%files api
%license LICENSE
%doc README.rst
%{_bindir}/%{service}-api

%files processor
%license LICENSE
%doc README.rst
%{_bindir}/%{service}-processor

%changelog
* Tue Nov  1 2016 Matthias Runge <mrunge@redhat.com>
- initial packaging
