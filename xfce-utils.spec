Summary:	Utilities for the Xfce Desktop Environment
Name:		xfce-utils
Version:	4.6.2
Release:	%mkrel 3
License:	GPLv2+
URL:		http://www.xfce.org
Group:		Graphical desktop/Xfce
Source0:	http://www.xfce.org/archive/xfce-%{version}/src/%{name}-%{version}.tar.bz2
# An english native speaker should feel free to update this file :)
Source1:	Mandriva
Source2:	06Xfce
Source3:	xfce4.sh
Source4:	xfce4.pam
Patch0:		xfce-utils-4.5.92-fix-desktop-entry.patch
Patch4:		01_xflock4-test-running-screensaver.patch
Patch5:		%{name}-4.6.2-xinitrc.patch
Patch6:		%{name}-4.4.2-prevent-about-dialog-resize.patch
Patch8:		%{name}-4.6.0-startxfce-data-dirs.patch
Patch10:	%{name}-4.5.91-xfmountdev4-use-thunar.patch
Patch11:	%{name}-4.6.1-register-consolekit-session.patch
BuildRequires:	chrpath
BuildRequires:	dbus-glib-devel
BuildRequires:	libxfcegui4-devel >= 4.6.0
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
%patch0 -p1
%patch4 -p1
%patch5 -p1 -b .xinitrc
%patch6 -p1
%patch8 -p1
%patch10 -p1
#%patch11 -p1

%build

%if %mdkversion > 200900
sed -i -e 's#/etc/X11/xdg#/etc/xdg#g' scripts/xinitrc.in.in
%endif

%configure2_5x \
	--enable-dbus \
%if %mdkversion < 200900
	--sysconfdir=%{_sysconfdir}/X11 \
%endif
	--with-vendor-info=Mandriva \
	--disable-static \
	--with-browser=firefox \
	--with-terminal=Terminal

%make

%install
rm -rf %{buildroot}
%makeinstall_std

chrpath -d %{buildroot}%{_bindir}/xfrun4
install -m 644 %{SOURCE1} %{buildroot}%{_datadir}/xfce4

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

%find_lang %{name}

%post
%make_dm_session
if [ "$1" = "2" -a -r /etc/sysconfig/desktop ]; then
  sed -i -e "s|^DESKTOP=Xfce4$|DESKTOP=xfce4|g" /etc/sysconfig/desktop
fi

%if %mdkversion < 200900
%update_icon_cache hicolor
%endif


%postun
%make_session
%if %mdkversion < 200900
%clean_icon_cache hicolor
%endif

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
%doc README TODO ChangeLog AUTHORS
%if %mdkversion < 200900
%dir %{_sysconfdir}/X11/xdg/xfce4
%attr(755,root,root) %{_sysconfdir}/X11/xdg/xfce4/xinitrc
%{_sysconfdir}/X11/xdg/xfce4/Xft.xrdb
%{_sysconfdir}/X11/xdg/autostart/xfconf-migration-4.6.desktop
%else
%dir %{_sysconfdir}/xdg/xfce4
%attr(755,root,root) %{_sysconfdir}/xdg/xfce4/xinitrc
%exclude %{_sysconfdir}/xdg/xfce4/Xft.xrdb
%{_sysconfdir}/xdg/autostart/xfconf-migration-4.6.desktop
%config(noreplace) %{_sysconfdir}/X11/wmsession.d/06Xfce
%attr(755,root,root) %config(noreplace) %{_sysconfdir}/profile.d/xfce4.sh
%config(noreplace) %{_sysconfdir}/pam.d/xfce4
%endif
%dir %{_datadir}/xfce4
%{_bindir}/*
%{_libdir}/xfce4/xfconf-migration/xfconf-migration-4.6.pl
%{_datadir}/xfce4/*
%{_datadir}/icons/*
%{_datadir}/dbus-1/services/org.xfce.RunDialog.service
