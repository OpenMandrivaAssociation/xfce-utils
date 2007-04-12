%define version	4.4.0
%define release	1
%define __libtoolize /bin/true

Summary: 	Utilities for the Xfce Desktop Environment
Name: 		xfce-utils
Version: 	%{version}
Release: 	%mkrel %{release}
License:	GPL
URL: 		http://www.xfce.org/
Source0: 	%{name}-%{version}.tar.bz2
# (mpol) don't set font options
# (fc) 4.0.6-2mdk don't touch background
Patch0:		xfce-utils-4.1.99.3-fonts_background.patch
Patch1:		xfce-utils-4.1.99.3-no_compositor.patch
Group: 		Graphical desktop/Xfce
BuildRoot: 	%{_tmppath}/%{name}-root
Requires:	xfce-mcs-manager
# for /usr/sbin/fndSession:
Requires:	desktop-common-data
Requires:	exo
BuildRequires:	xfce-mcs-manager-devel
BuildRequires:	libgdk_pixbuf2.0-devel
BuildRequires:	chrpath

%description
Xfce-utils contains utilities for the Xfce Desktop Environment.

%prep
%setup -q
%patch0 -p1 -b .fonts_background
%patch1 -p1 -b .no_compositor

%build
%configure2_5x --enable-gdm --sysconfdir=%_sysconfdir/X11
%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std

# use 06 as session numbering
mv $RPM_BUILD_ROOT/%{_sysconfdir}/X11/wmsession.d/10XFce4 \
    $RPM_BUILD_ROOT/%{_sysconfdir}/X11/wmsession.d/06XFce4

# remove gdm session file, use fndSession
rm $RPM_BUILD_ROOT/%{_sysconfdir}/X11/gdm/Sessions/XFce4
rm $RPM_BUILD_ROOT/%{_sysconfdir}/X11/dm/Sessions/xfce.desktop

# remove switchdesk file, not in mdk
rm $RPM_BUILD_ROOT/%{_datadir}/apps/switchdesk/Xclients.xfce4

# remove desktop file
rm $RPM_BUILD_ROOT/%{_datadir}/xsessions/xfce.desktop

# remove unneeded devel files
rm -f %{buildroot}/%{_libdir}/xfce4/mcs-plugins/*.*a

chrpath -d $RPM_BUILD_ROOT/%{_bindir}/xfrun4

%find_lang %{name}


%post
%make_session
touch --no-create %{_datadir}/icons/hicolor || :
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
   %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi

%postun
%make_session
touch --no-create %{_datadir}/icons/hicolor || :
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
   %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi

%clean
rm -rf $RPM_BUILD_ROOT


%files -f %{name}.lang
%defattr(-,root,root)
%doc README TODO COPYING AUTHORS
%{_bindir}/*
%{_datadir}/xfce4/*
%{_datadir}/icons/*
#%{_datadir}/dbus-1/services/org.xfce.RunDialog.service
%config(noreplace) %{_sysconfdir}/X11/*




