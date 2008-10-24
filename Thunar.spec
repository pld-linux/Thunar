#
# Conditional build:
%bcond_without	static_libs	# don't build static library
#
%define		xfce_version	4.4.2
Summary:	Xfce file manager
Summary(pl.UTF-8):	Zarządca plików Xfce
Name:		Thunar
Version:	0.9.0
Release:	2
License:	GPL v2 / LGPL v2
Group:		X11/Applications
Source0:	http://www.xfce.org/archive/xfce-%{xfce_version}/src/%{name}-%{version}.tar.bz2
# Source0-md5:	0fc5008858661c0abd0399acbe30ef28
Patch0:		%{name}-desktop.patch
Patch1:		%{name}-locale-names.patch
Patch2:		%{name}-missing-audio-cds-for-volman.patch
URL:		http://thunar.xfce.org/
BuildRequires:	GConf2-devel >= 2.16.0
BuildRequires:	dbus-glib-devel >= 0.62
BuildRequires:	gamin-devel >= 0.1.0
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel >= 1:2.12.4
BuildRequires:	gtk+2-devel >= 2:2.10.6
BuildRequires:	gtk-doc >= 1.7
BuildRequires:	hal-devel >= 0.5.7
BuildRequires:	intltool
BuildRequires:	libexif-devel >= 0.6.13
BuildRequires:	libexo-devel >= 0.3.4
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel >= 1.2.12
BuildRequires:	libxfce4util-devel >= %{xfce_version}
BuildRequires:	pcre-devel >= 6.0
BuildRequires:	perl-base
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.311
BuildRequires:	startup-notification-devel >= 0.8
BuildRequires:	xfce4-panel-devel >= %{xfce_version}
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	gtk+2
Requires(post,postun):	hicolor-icon-theme
Requires:	%{name}-libs = %{version}-%{release}
Requires:	hal >= 0.5.7
Requires:	libexo >= 0.3.4
Requires:	shared-mime-info >= 0.15
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

%description apidocs
Thunar API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API Thunar.

%package libs
Summary:	Thunar libraries
Summary(pl.UTF-8):	Biblioteki Thunar
Group:		Libraries

%description libs
Thunar libraries.

%description libs -l pl.UTF-8
Biblioteki Thunar.

%package devel
Summary:	Header files for Thunar libraries
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotek Thunar
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	GConf2-devel >= 2.16.0
Requires:	dbus-glib-devel >= 0.62
Requires:	gamin-devel
Requires:	hal-devel >= 0.5.7
Requires:	libexo-devel >= 0.3.4
Requires:	libjpeg-devel

%description devel
This is the package containing the header files for Thunar libraries.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe biblioteki Thunar.

%package static
Summary:	Static Thunar libraries
Summary(pl.UTF-8):	Statyczne biblioteki Thunar
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static Thunar libraries.

%description static -l pl.UTF-8
Statyczne biblioteki Thunar.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p0

mv -f po/{pt_PT,pt}.po
mv -f po/{nb_NO,nb}.po

%build
%configure \
	--enable-dbus \
	--enable-exif \
	--enable-gnome-thumbnailers \
	--enable-gtk-doc \
	--enable-pcre \
	--enable-startup-notification \
	--with-html-dir=%{_gtkdocdir} \
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
%update_desktop_database_post
%update_icon_cache hicolor

%postun
%update_desktop_database_postun
%update_icon_cache hicolor

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
%attr(755,root,root) %{_libdir}/thunar-vfs-*
%attr(755,root,root) %{_libdir}/thunar-sendto-email
%dir %{_libdir}/thunarx-1
%attr(755,root,root) %{_libdir}/thunarx-1/*.so
%attr(755,root,root) %{_libdir}/xfce4/panel-plugins/thunar-tpa

%{_datadir}/Thunar
%{_datadir}/xfce4/panel-plugins/*.desktop
%{_datadir}/dbus-1/services/*.service
%{_desktopdir}/*.desktop
%{_iconsdir}/hicolor/*/*/*
%{_pixmapsdir}/Thunar
%{_mandir}/man1/Thunar*

# FIXME: maybe it's common dir?
%dir %{_datadir}/thumbnailers
%{_datadir}/thumbnailers/*.desktop

%dir %{_docdir}/Thunar
# move it to proper place
%{_docdir}/Thunar/README*

%dir %{_docdir}/Thunar/html
%{_docdir}/Thunar/*.txt
%{_docdir}/Thunar/html/C
%{_docdir}/Thunar/html/*.css
%lang(es) %{_docdir}/Thunar/html/es
%lang(eu) %{_docdir}/Thunar/html/eu
%lang(fr) %{_docdir}/Thunar/html/fr
%lang(ja) %{_docdir}/Thunar/html/ja
%lang(nl) %{_docdir}/Thunar/html/nl
%lang(pl) %{_docdir}/Thunar/html/pl
%lang(ru) %{_docdir}/Thunar/html/ru
%lang(zh_TW) %{_docdir}/Thunar/html/zh_TW

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/thunar*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*

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
