#
# Conditional build:
%bcond_without	static_libs	# don't build static library

%define		xfce_version	4.16.0
Summary:	Xfce file manager
Summary(pl.UTF-8):	Zarządca plików Xfce
Name:		Thunar
Version:	4.16.9
Release:	2
License:	GPL v2 / LGPL v2
Group:		X11/Applications
Source0:	http://archive.xfce.org/src/xfce/thunar/4.16/thunar-%{version}.tar.bz2
# Source0-md5:	83a5e6504dd6678b07e733ad162a59eb
Patch0:		%{name}-desktop.patch
URL:		http://thunar.xfce.org/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake >= 1:1.8
BuildRequires:	dbus-glib-devel >= 0.62
BuildRequires:	docbook-dtd412-xml
BuildRequires:	exo-devel >= 4.15.3
BuildRequires:	gdk-pixbuf2-devel
BuildRequires:	gettext-tools
BuildRequires:	glib2-devel >= 1:2.50.0
BuildRequires:	gobject-introspection-devel >= 1.30.0
BuildRequires:	gtk+3-devel >= 3.22.0
BuildRequires:	gtk-doc >= 1.7
BuildRequires:	intltool
BuildRequires:	libexif-devel >= 0.6.0
BuildRequires:	libgudev-devel
BuildRequires:	libnotify-devel >= 0.4.0
BuildRequires:	libtool
BuildRequires:	libxfce4ui-devel >= 4.16.0
BuildRequires:	libxfce4util-devel >= %{xfce_version}
BuildRequires:	pcre-devel >= 6.0
BuildRequires:	perl-base
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 2.011
BuildRequires:	startup-notification-devel >= 0.8
BuildRequires:	xfce4-dev-tools >= %{xfce_version}
BuildRequires:	xfce4-panel-devel >= %{xfce_version}
BuildRequires:	xfconf-devel >= %{xfce_version}
Requires(post,postun):	desktop-file-utils
Requires(post,preun):	systemd-units >= 250.1
Requires:	%{name}-libs = %{version}-%{release}
Requires:	exo >= 4.15.3
Requires:	gtk-update-icon-cache
Requires:	hicolor-icon-theme
Requires:	shared-mime-info >= 0.15
Requires:	systemd-units >= 250.1
Requires:	xfconf >= %{xfce_version}
Suggests:	tumbler
Obsoletes:	Thunar-thumbnailers < 0.5
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Thunar is a modern file manager, aiming to be easy-to-use and fast.

%description -l pl.UTF-8
Thunar jest nowoczesnym zarządcą plików, nakierowanym na łatwość i
szybkość użycia.

%package apidocs
Summary:	Thunar API documentation
Summary(pl.UTF-8):	Dokumentacja API Thunar
Group:		Documentation
Requires:	gtk-doc-common
Obsoletes:	thunar-vfs-apidocs < 1.3
BuildArch:	noarch

%description apidocs
Thunar API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API Thunar.

%package libs
Summary:	Thunar libraries
Summary(pl.UTF-8):	Biblioteki Thunar
Group:		X11/Libraries
Obsoletes:	thunar-vfs < 1.3

%description libs
Thunar libraries.

%description libs -l pl.UTF-8
Biblioteki Thunar.

%package devel
Summary:	Header files for Thunar libraries
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotek Thunar
Group:		X11/Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	exo-devel >= 4.15.3
Requires:	gtk+3-devel >= 3.22.0
Obsoletes:	thunar-vfs-devel < 1.3

%description devel
This is the package containing the header files for Thunar libraries.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe biblioteki Thunar.

%package static
Summary:	Static Thunar libraries
Summary(pl.UTF-8):	Statyczne biblioteki Thunar
Group:		X11/Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Obsoletes:	thunar-vfs-static < 1.3

%description static
Static Thunar libraries.

%description static -l pl.UTF-8
Statyczne biblioteki Thunar.

%prep
%setup -q -n thunar-%{version}
%patch0 -p1

mkdir -p m4

%{__sed} -i -e 's/AM_CONFIG_HEADER/AC_CONFIG_HEADERS/' configure.ac

%build
%{__gtkdocize}
%{__intltoolize}
%{__libtoolize}
%{__aclocal}
%{__automake}
%{__autoheader}
%{__autoconf}
%configure \
	--enable-exif \
	--enable-gtk-doc \
	--enable-pcre \
	--with-html-dir=%{_gtkdocdir} \
	%{?with_static_libs:--enable-static} \
	--disable-silent-rules

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/thunarx-3/*.{a,la}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/xfce4/panel/plugins/*.{a,la}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la

# duplicate of ur
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/ur_PK

# unknown / unsupported
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/{fa_IR,hye,hy_AM,ie}

%find_lang %{name} --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_desktop_database_post
%update_icon_cache hicolor
%systemd_user_post thunar.service

%preun
%systemd_user_preun thunar.service

%postun
%update_desktop_database_postun
%update_icon_cache hicolor

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS THANKS
%attr(755,root,root) %{_bindir}/*
%dir %{_sysconfdir}/xdg/Thunar
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/xdg/Thunar/*.xml
%dir %{_libdir}/Thunar
%attr(755,root,root) %{_libdir}/Thunar/thunar-sendto-email
%dir %{_libdir}/thunarx-3
%attr(755,root,root) %{_libdir}/thunarx-3/*.so
%attr(755,root,root) %{_libdir}/xfce4/panel/plugins/libthunar-tpa.so

%{systemduserunitdir}/thunar.service
%{_libdir}/girepository-1.0/Thunarx-3.0.typelib
%{_datadir}/metainfo/org.xfce.thunar.appdata.xml
%{_datadir}/polkit-1/actions/org.xfce.thunar.policy
%{_datadir}/Thunar/sendto/*.desktop
%{_datadir}/xfce4/panel/plugins/*.desktop
%{_datadir}/dbus-1/services/*.service
%{_desktopdir}/*.desktop
%{_iconsdir}/hicolor/*/*/*
%{_mandir}/man1/Thunar*

%dir %{_docdir}/thunar
# move it to proper place
%{_docdir}/thunar/README*

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/thunarx

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libthunarx-3.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libthunarx-3.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libthunarx-3.so
%{_includedir}/thunarx-3
%{_pkgconfigdir}/thunarx-3.pc
%{_datadir}/gir-1.0/Thunarx-3.0.gir

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libthunarx-3.a
%endif
