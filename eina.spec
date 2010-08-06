# Conditional build:
%bcond_without	mmx		# without MMX and MMX2
%bcond_without	sse		# without SSE
%bcond_without	altivec		# without altivec
%bcond_without	static_libs	# don't build static library
#
%ifnarch i586 i686 pentium3 pentium4 athlon %{x8664}
%undefine	with_mmx
%endif
%ifnarch i686 pentium3 pentium4 athlon %{x8664}
%undefine	with_sse
%endif
%ifnarch ppc
%undefine	with_altivec
%endif

Summary:	Data types library (List, hash, etc)
Summary(pl.UTF-8):	Bilblioteka typów danych (Lista, hasz, itd.)
Name:		eina
Version:	0.9.9.49898
Release:	1
License:	LGPL v2.1
Group:		Libraries
Source0:	http://download.enlightenment.org/snapshots/LATEST/%{name}-%{version}.tar.bz2
# Source0-md5:	d14bacce7d588524c12ddad1db9c7240
URL:		http://enlightenment.org/p.php?p=about/libs/eina
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Data types library (List, hash, etc)

%description -l pl.UTF-8
Bilblioteka typów danych(Lista, hasz, itd.)

%package devel
Summary:	Eina header files
Summary(pl.UTF-8):	Pliki nagłówkowe Einy
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for Eina.

%description devel -l pl.UTF-8
Pliki nagłówkowe Eina.

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
rm -rf autom4te.cache
rm -f aclocal.m4 ltmain.sh
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{?with_static_libs:--enable-static} \
%if %{with mmx}
	--enable-cpu-mmx	\
%else
	--disable-cpu-mmx	\
%endif
%if %{with sse}
	--enable-cpu-sse	\
%else
	--disable-cpu-sse	\
%endif
%if %{with altivec}
	--enable-cpu-altivec	\
%else
	--disable-cpu-altivec	\
%endif

%{__make} V=1

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
%doc AUTHORS
%attr(755,root,root) %{_libdir}/libeina-ver-svn-06.so.0.9.9
%attr(755,root,root) %ghost %{_libdir}/libeina-ver-svn-06.so.0

%files devel
%defattr(644,root,root,755)
%{_includedir}/eina-0
%{_libdir}/libeina.la
%{_libdir}/libeina.so
%{_pkgconfigdir}/eina-0.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libeina.a
%endif
