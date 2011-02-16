#
# Conditional build:
%bcond_without	static_libs	# don't build static library
#
%define		xfce_version	4.8.0
Summary:	Xfce file manager
Summary(pl.UTF-8):	Zarządca plików Xfce
Name:		Thunar
Version:	1.2.1
Release:	1
License:	GPL v2 / LGPL v2
Group:		X11/Applications
Source0:	http://archive.xfce.org/src/xfce/thunar/1.2/%{name}-%{version}.tar.bz2
# Source0-md5:	d8dce796890619d67aed0cd7ef84c7b1
Patch0:		%{name}-desktop.patch
URL:		http://thunar.xfce.org/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake >= 1:1.8
BuildRequires:	dbus-glib-devel >= 0.62
BuildRequires:	docbook-dtd412-xml
BuildRequires:	exo-devel >= 0.6.0
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel >= 1:2.18.0
BuildRequires:	gtk+2-devel >= 2:2.14.0
BuildRequires:	gtk-doc >= 1.7
BuildRequires:	intltool
BuildRequires:	libexif-devel >= 0.6.0
BuildRequires:	libnotify-devel >= 0.4.0
BuildRequires:	libtool
BuildRequires:	libxfce4ui-devel >= %{xfce_version}
BuildRequires:	libxfce4util-devel >= %{xfce_version}
BuildRequires:	pcre-devel >= 6.0
BuildRequires:	perl-base
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.601
BuildRequires:	startup-notification-devel >= 0.8
BuildRequires:	udev-glib-devel >= 145
BuildRequires:	xfce4-dev-tools >= %{xfce_version}
BuildRequires:	xfce4-panel-devel >= %{xfce_version}
Requires(post,postun):	desktop-file-utils
Requires:	%{name}-libs = %{version}-%{release}
Requires:	exo >= 0.6.0
Requires:	gtk-update-icon-cache
Requires:	hicolor-icon-theme
Requires:	shared-mime-info >= 0.15
Requires:	xfconf >= %{xfce_version}
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
Group:		X11/Libraries

%description libs
Thunar libraries.

%description libs -l pl.UTF-8
Biblioteki Thunar.

%package devel
Summary:	Header files for Thunar libraries
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotek Thunar
Group:		X11/Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	exo-devel >= 0.6.0
Requires:	gtk+2-devel >= 2:2.14.0

%description devel
This is the package containing the header files for Thunar libraries.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe biblioteki Thunar.

%package static
Summary:	Static Thunar libraries
Summary(pl.UTF-8):	Statyczne biblioteki Thunar
Group:		X11/Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static Thunar libraries.

%description static -l pl.UTF-8
Statyczne biblioteki Thunar.

%prep
%setup -q
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
	--enable-dbus \
	--enable-exif \
	--enable-gtk-doc \
	--enable-pcre \
	--enable-startup-notification \
	--with-html-dir=%{_gtkdocdir} \
	%{?with_static_libs:--enable-static} \
	--disable-silent-rules

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/thunarx-2/*.{a,la}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/xfce4/panel/plugins/*.{a,la}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la

%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/locale/ur_PK

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
%dir %{_libdir}/Thunar
%attr(755,root,root) %{_libdir}/Thunar/ThunarBulkRename
%attr(755,root,root) %{_libdir}/Thunar/ThunarHelp
%attr(755,root,root) %{_libdir}/Thunar/thunar-sendto-email
%dir %{_libdir}/thunarx-2
%attr(755,root,root) %{_libdir}/thunarx-2/*.so
%attr(755,root,root) %{_libdir}/xfce4/panel/plugins/libthunar-tpa.so

%{_datadir}/Thunar
%{_datadir}/xfce4/panel-plugins/*.desktop
%{_datadir}/dbus-1/services/*.service
%{_desktopdir}/*.desktop
%{_iconsdir}/hicolor/*/*/*
%{_pixmapsdir}/Thunar
%{_mandir}/man1/Thunar*

%dir %{_docdir}/Thunar
# move it to proper place
%{_docdir}/Thunar/README*

%dir %{_docdir}/Thunar/html
%{_docdir}/Thunar/html/C
%{_docdir}/Thunar/html/*.css
%lang(bn) %{_docdir}/Thunar/html/bn
%lang(ca) %{_docdir}/Thunar/html/ca
%lang(da) %{_docdir}/Thunar/html/da
%lang(el) %{_docdir}/Thunar/html/el
%lang(es) %{_docdir}/Thunar/html/es
%lang(eu) %{_docdir}/Thunar/html/eu
%lang(fr) %{_docdir}/Thunar/html/fr
%lang(gl) %{_docdir}/Thunar/html/gl
%lang(id) %{_docdir}/Thunar/html/id
%lang(it) %{_docdir}/Thunar/html/it
%lang(ja) %{_docdir}/Thunar/html/ja
%lang(nl) %{_docdir}/Thunar/html/nl
%lang(pl) %{_docdir}/Thunar/html/pl
%lang(ru) %{_docdir}/Thunar/html/ru
%lang(sv) %{_docdir}/Thunar/html/sv
%lang(tr) %{_docdir}/Thunar/html/tr
%lang(ug) %{_docdir}/Thunar/html/ug
%lang(zh_CN) %{_docdir}/Thunar/html/zh_CN
%lang(zh_TW) %{_docdir}/Thunar/html/zh_TW

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/thunarx

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libthunarx-2.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libthunarx-2.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libthunarx-2.so
%{_includedir}/thunarx-2
%{_pkgconfigdir}/thunarx-2.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libthunarx-2.a
%endif
