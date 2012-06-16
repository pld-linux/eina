#
# Conditional build:
%bcond_without	mmx		# without MMX and MMX2
%bcond_without	sse		# without SSE
%bcond_without	sse2		# without SSE2
%bcond_without	altivec		# without altivec
%bcond_without	static_libs	# don't build static library
#
%ifnarch i586 i686 pentium3 pentium4 athlon %{x8664}
%undefine	with_mmx
%endif
%ifnarch i686 pentium3 pentium4 athlon %{x8664}
%undefine	with_sse
%endif
%ifnarch pentium4 %{x8664}
%undefine	with_sse2
%endif
%ifnarch ppc
%undefine	with_altivec
%endif

Summary:	Data types library (list, hash, etc.)
Summary(pl.UTF-8):	Biblioteka struktur danych (lista, hasz, itp.)
Name:		eina
Version:	1.2.1
Release:	1
License:	LGPL v2.1+
Group:		Libraries
Source0:	http://download.enlightenment.org/releases/%{name}-%{version}.tar.bz2
# Source0-md5:	588ec74a3d6eb77b9bd1a70f88cbd285
URL:		http://trac.enlightenment.org/e/wiki/Eina
BuildRequires:	pkgconfig >= 1:0.22
# ememoa-devel >= 0.0.26
# escape (for ps3 platform)
# evil (for win32 platform)
# exotic (for ??? platforms)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Data types library (list, hash, etc.)

%description -l pl.UTF-8
Bilblioteka struktur danych (lista, hasz, itp.).

%package devel
Summary:	Eina header files
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki Eina
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for Eina.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Eina.

%package static
Summary:	Static Eina library
Summary(pl.UTF-8):	Statyczna biblioteka Eina
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static Eina library.

%description static -l pl.UTF-8
Statyczna biblioteka Eina.

%prep
%setup -q

%build
%configure \
	--disable-silent-rules \
	%{?with_static_libs:--enable-static} \
	--enable-cpu-mmx%{!?with_mmx:=no} \
	--enable-cpu-sse%{!?with_sse:=no} \
	--enable-cpu-sse2%{!?with_sse2:=no} \
	--enable-cpu-altivec%{!?with_altivec:=no}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_libdir}/libeina.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libeina.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libeina.so
%{_libdir}/libeina.la
%{_includedir}/eina-1
%{_pkgconfigdir}/eina.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libeina.a
%endif
