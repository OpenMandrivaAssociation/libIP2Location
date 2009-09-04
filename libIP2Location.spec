%define lib_major       0
%define lib_name_orig   %mklibname IP2Location
%define lib_name        %{lib_name_orig}%{lib_major}

Name:           libIP2Location
Version:        1.1.0
Release:        %mkrel 5
Epoch:          0
Summary:        Find the country, region, etc. that any IP address or hostname originates from
Group:          System/Libraries
License:        GPL
URL:            http://www.ip2location.com/c.htm
Source0:        http://www.ip2location.com/developers/c/C-IP2Location-%{version}.tar.bz2
BuildRequires:  chrpath
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

%description
IP2Location is a C library that enables the user to find the
country, region, city, coordinates, zip code, ISP and domain name
that any IP address or hostname originates from. It has been
optimized for speed and memory utilization. Developers can use the
API to query all IP2Location binary databases for applications
written in C or supporting static/dynamic library.

%package -n %{lib_name}
Summary:        Main library for %{name}
Group:          System/Libraries

%description -n %{lib_name}
IP2Location is a C library that enables the user to find the
country, region, city, coordinates, zip code, ISP and domain name
that any IP address or hostname originates from. It has been
optimized for speed and memory utilization. Developers can use the
API to query all IP2Location binary databases or applications
written in C or supporting static/dynamic library.

%package -n %{lib_name}-devel
Summary:        Development files for %{name}
Group:          System/Libraries
Requires:       %{lib_name} = %{epoch}:%{version}-%{release}
Provides:       %{name}-devel = %{epoch}:%{version}-%{release}

%description -n %{lib_name}-devel
This package contains the development files for %{name}.

%package -n %{lib_name}-static-devel
Summary:        Static development files for %{name}
Group:          System/Libraries
Requires:       %{lib_name}-devel = %{epoch}:%{version}-%{release}
Provides:       %{name}-static-devel = %{epoch}:%{version}-%{release}

%description -n %{lib_name}-static-devel
This package contains the static development files for %{name}.

%prep
%setup -q -n C-IP2Location-%{version}
%{_bindir}/autoreconf -i --force

%build
%configure2_5x
%make

%install
%{__rm} -rf %{buildroot}
%makeinstall

%{__mv} %{buildroot}%{_libdir}/libIP2Location/* %{buildroot}%{_libdir}
%{__rm} -rf %{buildroot}%{_libdir}/libIP2Location

%{__mkdir_p} %{buildroot}%{_includedir}/libIP2Location
%{__install} -m 644 libIP2Location/IP2Location.h %{buildroot}%{_includedir}/libIP2Location

%{_bindir}/chrpath -d %{buildroot}%{_libdir}/libIP2Location.so

%{__perl} -pi -e 's| -R/usr/local/lib -L/usr/local/lib||;' \
              -e 's|%{_libdir}/libIP2Location|%{_libdir}|;' \
  %{buildroot}%{_libdir}/*.la 

%{__perl} -pi -e 's/\r$//g' AUTHORS ChangeLog COPYING README

%clean
%{__rm} -rf %{buildroot}

%if %mdkversion < 200900
%post -n %{lib_name} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{lib_name} -p /sbin/ldconfig
%endif

%files -n %{lib_name}
%defattr(0644,root,root,0755)
%doc AUTHORS ChangeLog COPYING INSTALL NEWS README
%defattr(-,root,root,-)
%{_libdir}/*.so

%files -n %{lib_name}-devel
%defattr(0644,root,root,0755)
%dir %{_includedir}/libIP2Location
%{_includedir}/libIP2Location/*.h
%defattr(-,root,root,-)
%{_libdir}/*.la

%files -n %{lib_name}-static-devel
%{_libdir}/*.a


