%define url_ver %(echo %{version} | cut -c 1-3)

Summary:	Utilities for the Xfce Desktop Environment
Name:		xfce-utils
Version:	4.7.1
Release:	%mkrel 2
License:	GPLv2+
URL:		http://www.xfce.org
Group:		Graphical desktop/Xfce
Source0:	http://archive.xfce.org/src/xfce/%{name}/%{url_ver}/%{name}-%{version}.tar.bz2
# An english native speaker should feel free to update this file :)
Source1:	Mandriva
Source2:	06Xfce
Source3:	xfce4.sh
Source4:	xfce4.pam
Patch5:		%{name}-4.7.1-xinitrc.patch
Patch10:	%{name}-4.5.91-xfmountdev4-use-thunar.patch
BuildRequires:	chrpath
BuildRequires:	dbus-glib-devel
BuildRequires:	libxfce4util-devel >= 4.7.0
BuildRequires:	libxfce4ui-devel >= 4.7.0
# for /usr/sbin/fndSession:
Requires:	desktop-common-data
Requires:	exo
Requires:	dbus-x11
Requires:	xinit
Requires:	xdg-user-dirs-gtk
Requires:	xscreensaver
Requires:	iceauth
Requires:	consolekit
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

%description
The utilities and scripts provides an about dialog for
Xfce 4, an application launcher, and several useful
scripts that are also used by other Xfce components such
as the panel and the desktop menu.

%prep
%setup -q
%patch5 -p1 -b .xinitrc
%patch10 -p1

%build

%if %mdkversion > 200900
sed -i -e 's#/etc/X11/xdg#/etc/xdg#g' scripts/xinitrc.in.in
%endif

%configure2_5x \
	--enable-dbus \
	--with-vendor-info=Mandriva \
	--disable-static \
	--with-browser=firefox \
	--with-terminal=Terminal

%make

%install
rm -rf %{buildroot}
%makeinstall_std

chrpath -d %{buildroot}%{_bindir}/xfrun4
install -m 644 -D %{SOURCE1} %{buildroot}%{_datadir}/xfce4/Mandriva

# session
mkdir -p %{buildroot}%{_sysconfdir}/X11/wmsession.d
install -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/X11/wmsession.d

# env
mkdir -p %{buildroot}%{_sysconfdir}/profile.d
install -m 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/profile.d

# pam
mkdir -p %{buildroot}%{_sysconfdir}/pam.d
install -m 644 %{SOURCE4} %{buildroot}%{_sysconfdir}/pam.d/xfce4

# not needed at all in mdv case
rm -rf %{buildroot}%{_datadir}/xsessions/xfce.desktop

# (tpg) this file is in mandriva-xfce-config package
rm -rf %{buildroot}%{_sysconfdir}/xdg/xfce4/Xft.xrdb

%find_lang %{name}

%post
%make_dm_session
if [ "$1" = "2" -a -r /etc/sysconfig/desktop ]; then
  sed -i -e "s|^DESKTOP=Xfce4$|DESKTOP=xfce4|g" /etc/sysconfig/desktop
fi

%postun
%make_session

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
%doc README TODO ChangeLog AUTHORS
%dir %{_sysconfdir}/xdg/xfce4
%attr(755,root,root) %{_sysconfdir}/xdg/xfce4/xinitrc
%{_sysconfdir}/xdg/autostart/xfconf-migration-4.6.desktop
%config(noreplace) %{_sysconfdir}/X11/wmsession.d/06Xfce
%attr(755,root,root) %config(noreplace) %{_sysconfdir}/profile.d/xfce4.sh
%config(noreplace) %{_sysconfdir}/pam.d/xfce4
%dir %{_datadir}/xfce4
%{_datadir}/xfce4/Mandriva
%{_bindir}/*
%{_libdir}/xfce4/xfconf-migration/xfconf-migration-4.6.pl
%{_datadir}/icons/*
%{_datadir}/applications/*.desktop
%{_datadir}/dbus-1/services/org.xfce.RunDialog.service
