Summary:	Utilities for the Xfce Desktop Environment
Name:		xfce-utils
Version:	4.4.2
Release:	%mkrel 3
License:	GPLv2+
URL:		http://www.xfce.org
Group:		Graphical desktop/Xfce
Source0:	%{name}-%{version}.tar.bz2
# An english native speaker should feel free to update this file :)
Source1:	Mandriva
#(tpg) please see bug 29095
Patch1:		%{name}-4.4.1-missing-icon-in-startup-script.patch
Patch2:		%{name}-4.4.1-xinitrc-cpp.patch
BuildRequires:	xfce-mcs-manager-devel >= %{version}
BuildRequires:	libgdk_pixbuf2.0-devel
BuildRequires:	chrpath
BuildRequires:	dbus-glib-devel
Requires:	xfce-mcs-manager
# for /usr/sbin/fndSession:
Requires:	desktop-common-data
Requires:	exo
Requires:	dbus-x11
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

%description
The utilities and scripts provides an about dialog for
Xfce 4, an application launcher, and several useful
scripts that are also used by other Xfce components such
as the panel and the desktop menu.

%prep
%setup -q
%patch1 -p1
%patch2 -p1

%build
%configure2_5x \
	--enable-gdm \
	--enable-dbus \
	--with-gdm-prefix=%{_sysconfdir}/X11 \
	--sysconfdir=%{_sysconfdir}/X11 \
	--with-vendor-info=Mandriva \
	--disable-static \
	--with-browser=Thunar \
	--with-terminal=Terminal
%make

%install
rm -rf %{buildroot}
%makeinstall_std

# use 06 as session numbering
mv %{buildroot}%{_sysconfdir}/X11/wmsession.d/10XFce4 \
    %{buildroot}%{_sysconfdir}/X11/wmsession.d/06XFce4

# remove gdm session file, use fndSession
rm %{buildroot}%{_sysconfdir}/X11/gdm/Sessions/XFce4
rm %{buildroot}%{_sysconfdir}/X11/dm/Sessions/xfce.desktop

# remove switchdesk file, not in mdk
rm %{buildroot}%{_datadir}/apps/switchdesk/Xclients.xfce4

# remove desktop file
rm %{buildroot}%{_datadir}/xsessions/xfce.desktop

chrpath -d %{buildroot}%{_bindir}/xfrun4
install -m 644 %{SOURCE1} %{buildroot}%{_datadir}/xfce4

%find_lang %{name}

%post
%make_session
%update_icon_cache hicolor

%postun
%make_session
%clean_icon_cache hicolor

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
%doc README TODO ChangeLog AUTHORS
%dir %{_sysconfdir}/X11/xdg/xfce4
%dir %{_datadir}/xfce4
%config(noreplace) %{_sysconfdir}/X11/xdg/xfce4/xinitrc
%{_bindir}/*
%{_datadir}/xfce4/*
%{_datadir}/icons/*
%{_sysconfdir}/X11/wmsession.d/06XFce4
%{_sysconfdir}/X11/xdg/xfce4/Xft.xrdb
%{_datadir}/dbus-1/services/org.xfce.RunDialog.service
