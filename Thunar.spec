#
# Conditional build:
%bcond_without	static_libs	# static library

%define		xfce_version	4.18.0
Summary:	Xfce file manager
Summary(pl.UTF-8):	Zarządca plików Xfce
Name:		Thunar
Version:	4.18.11
Release:	1
License:	GPL v2 / LGPL v2
Group:		X11/Applications
Source0:	https://archive.xfce.org/src/xfce/thunar/4.18/thunar-%{version}.tar.bz2
# Source0-md5:	506e80f3fa94aca251b18c185b1303e8
Patch0:		%{name}-desktop.patch
URL:		https://docs.xfce.org/xfce/thunar/start
BuildRequires:	autoconf >= 2.60
BuildRequires:	automake >= 1:1.11
BuildRequires:	docbook-dtd412-xml
BuildRequires:	exo-devel >= 4.17.0
BuildRequires:	gdk-pixbuf2-devel >= 2.40.0
BuildRequires:	gettext-tools
BuildRequires:	glib2-devel >= 1:2.66.0
BuildRequires:	gobject-introspection-devel >= 1.66.0
BuildRequires:	gtk+3-devel >= 3.24.0
BuildRequires:	gtk-doc >= 1.9
BuildRequires:	intltool
BuildRequires:	libexif-devel >= 0.6.0
BuildRequires:	libgudev-devel >= 145
BuildRequires:	libnotify-devel >= 0.4.0
BuildRequires:	libtool >= 2:2.4
BuildRequires:	libxfce4ui-devel >= %{xfce_version}
BuildRequires:	libxfce4util-devel >= %{xfce_version}
BuildRequires:	pcre-devel >= 6.0
BuildRequires:	pango-devel >= 1:1.38.0
BuildRequires:	perl-base
BuildRequires:	pkgconfig
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 2.011
BuildRequires:	startup-notification-devel >= 0.8
BuildRequires:	xfce4-dev-tools >= %{xfce_version}
BuildRequires:	xfce4-panel-devel >= %{xfce_version}
BuildRequires:	xfconf-devel >= %{xfce_version}
BuildRequires:	xorg-lib-libSM-devel
BuildRequires:	xorg-lib-libX11-devel
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	gtk-update-icon-cache
Requires(post,preun):	systemd-units >= 1:250.1
Requires:	%{name}-libs = %{version}-%{release}
Requires:	exo >= 4.17.0
Requires:	gdk-pixbuf2 >= 2.40.0
Requires:	hicolor-icon-theme
Requires:	libnotify >= 0.4.0
Requires:	libxfce4ui >= %{xfce_version}
Requires:	libxfce4util >= %{xfce_version}
Requires:	pango >= 1:1.38.0
Requires:	shared-mime-info >= 0.15
Requires:	systemd-units >= 1:250.1
Requires:	xfconf >= %{xfce_version}
Suggests:	tumbler
Obsoletes:	Thunar-thumbnailers < 0.5
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Thunar is a modern file manager, aiming to be easy-to-use and fast.

%description -l pl.UTF-8
Thunar jest nowoczesnym zarządcą plików, nakierowanym na łatwość i
szybkość użycia.

%package libs
Summary:	Thunar libraries
Summary(pl.UTF-8):	Biblioteki Thunar
Group:		X11/Libraries
Requires:	glib2 >= 1:2.66.0
Requires:	gtk+3 >= 3.24.0
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
Requires:	glib2-devel >= 1:2.66.0
Requires:	gtk+3-devel >= 3.24.0
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

%prep
%setup -q -n thunar-%{version}
%patch0 -p1

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
	--disable-silent-rules \
	%{?with_static_libs:--enable-static} \
	--with-html-dir=%{_gtkdocdir}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/thunarx-3/*.{a,la}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/xfce4/panel/plugins/*.{a,la}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la

# unify
%{__mv} $RPM_BUILD_ROOT%{_localedir}/{fa_IR,fa}
# duplicate of hy,ur
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/{hy_AM,ur_PK}
# not supported by glibc (as of 2.37)
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/{hye,ie}

%find_lang thunar

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

%files -f thunar.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS THANKS
%attr(755,root,root) %{_bindir}/Thunar
%attr(755,root,root) %{_bindir}/thunar
%attr(755,root,root) %{_bindir}/thunar-settings
%dir %{_sysconfdir}/xdg/Thunar
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/xdg/Thunar/*.xml
%dir %{_libdir}/Thunar
%attr(755,root,root) %{_libdir}/Thunar/thunar-sendto-email
%dir %{_libdir}/thunarx-3
%attr(755,root,root) %{_libdir}/thunarx-3/thunar-*.so
%attr(755,root,root) %{_libdir}/xfce4/panel/plugins/libthunar-tpa.so

%{systemduserunitdir}/thunar.service
%{_datadir}/dbus-1/services/org.xfce.FileManager.service
%{_datadir}/dbus-1/services/org.xfce.Thunar.service
%{_datadir}/dbus-1/services/org.xfce.Thunar.FileManager1.service
%{_datadir}/metainfo/org.xfce.thunar.appdata.xml
%{_datadir}/polkit-1/actions/org.xfce.thunar.policy
%{_datadir}/Thunar/sendto/thunar-sendto-email.desktop
%{_datadir}/xfce4/panel/plugins/thunar-tpa.desktop
%{_desktopdir}/thunar.desktop
%{_desktopdir}/thunar-bulk-rename.desktop
%{_desktopdir}/thunar-settings.desktop
%{_iconsdir}/hicolor/*x*/apps/org.xfce.thunar.png
%{_iconsdir}/hicolor/*x*/stock/navigation/stock_folder-*.png
%{_iconsdir}/hicolor/scalable/apps/org.xfce.thunar.svg
%{_mandir}/man1/Thunar.1*

%dir %{_docdir}/thunar
# move it to proper place
%{_docdir}/thunar/README*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libthunarx-3.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libthunarx-3.so.0
%{_libdir}/girepository-1.0/Thunarx-3.0.typelib

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

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/thunar
%{_gtkdocdir}/thunarx
