#
# Conditional build:
%bcond_without	static_libs	# don't build static library
#
%define		_pre		beta2
%define		xfce_version	4.3.90.2
Summary:	Xfce file manager
Summary(pl):	Zarz±dca plików Xfce
Name:		Thunar
Version:	0.3.2
Release:	0.%{_pre}.1
License:	GPL v2 / LGPL v2
Group:		Applications
Source0:	http://www.xfce.org/archive/xfce-%{xfce_version}/src/%{name}-%{version}%{_pre}.tar.bz2
# Source0-md5:	53087545a5bf6bdac0174a4628722c21
URL:		http://thunar.xfce.org/
BuildRequires:	GConf2-devel >= 2.14.0
BuildRequires:	dbus-glib-devel >= 0.62
# XXX: gamin (>= 0.1.0) is preferred over fam
BuildRequires:	fam-devel
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel >= 1:2.12.0
BuildRequires:	gtk+2-devel >= 2:2.10.0
BuildRequires:	hal-devel >= 0.5.7
BuildRequires:	intltool
BuildRequires:	libexif-devel >= 0.6.13
BuildRequires:	libexo-devel >= 0.3.1.8
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel >= 1.2.12
BuildRequires:	libxfce4util-devel >= %{xfce_version}
BuildRequires:	pcre-devel >= 6.0
BuildRequires:	perl-base
BuildRequires:	pkgconfig
BuildRequires:	startup-notification-devel >= 0.8
Requires(post,postun):	gtk+2 >= 2.10.0
Requires:	%{name}-libs = %{version}-%{release}
Requires:	hal >= 0.5.7
Requires:	hicolor-icon-theme
Requires:	libexo >= 0.3.1.8
Requires:	shared-mime-info >= 0.15
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Thunar is a modern file manager, aiming to be easy-to-use and fast.

%description -l pl
Thunar jest nowoczesnym zarz±dc± plików, nakierowanym na ³atwo¶æ i
szybko¶æ u¿ycia.

%package libs
Summary:	Thunar libraries
Summary(pl):	Biblioteki Thunar
Group:		Libraries

%description libs
Thunar libraries.

%description libs -l pl
Biblioteki Thunar.

%package devel
Summary:	Header files for Thunar libraries
Summary(pl):	Pliki nag³ówkowe bibliotek Thunar
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	GConf2-devel >= 2.14.0
Requires:	dbus-glib-devel >= 0.62
Requires:	fam-devel
Requires:	hal-devel >= 0.5.7
Requires:	libjpeg-devel

%description devel
This is the package containing the header files for Thunar libraries.

%description devel -l pl
Ten pakiet zawiera pliki nag³ówkowe biblioteki Thunar.

%package static
Summary:	Static Thunar library
Summary(pl):	Statyczna biblioteka libraries
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static Thunar libraries.

%description static -l pl
Statyczna biblioteki Thunar

%prep
%setup -qn %{name}-%{version}%{_pre}

%build
LDFLAGS="%{rpmldflags} -Wl,--as-needed"
%configure \
	%{?with_static_libs:--enable-static}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/thunarx-1/*.{a,la}

%find_lang %{name} --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post
gtk-update-icon-cache -qf %{_datadir}/icons/hicolor

%postun
gtk-update-icon-cache -qf %{_datadir}/icons/hicolor

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README THANKS TODO
%attr(755,root,root) %{_bindir}/*
%dir %{_sysconfdir}/xdg/Thunar
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/xdg/Thunar/*.xml
%attr(755,root,root) %{_libdir}/ThunarBulkRename
%attr(755,root,root) %{_libdir}/ThunarHelp
%attr(755,root,root) %{_libdir}/thunar-vfs-mime-cleaner-1
%attr(755,root,root) %{_libdir}/thunar-sendto-email
%dir %{_libdir}/thunarx-1
%attr(755,root,root) %{_libdir}/thunarx-1/*.so

%{_datadir}/Thunar
%{_datadir}/dbus-1/services/*.service
%{_desktopdir}/*.desktop
%{_iconsdir}/hicolor/*/*/*
%{_pixmapsdir}/Thunar

%dir %{_docdir}/Thunar
# move it to proper place
%{_docdir}/Thunar/README*

%dir %{_docdir}/Thunar/html
%{_docdir}/Thunar/html/C
%{_docdir}/Thunar/html/*.css
%lang(es) %{_docdir}/Thunar/html/es
%lang(fr) %{_docdir}/Thunar/html/fr
%lang(ja) %{_docdir}/Thunar/html/ja
%lang(ru) %{_docdir}/Thunar/html/ru
%lang(zh_TW) %{_docdir}/Thunar/html/zh_TW

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_includedir}/thunar*
%{_pkgconfigdir}/*.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/*.a
%endif
