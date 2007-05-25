Summary:	Utilities for the Xfce Desktop Environment
Name:		xfce-utils
Version:	4.4.1
Release:	%mkrel 2
License:	GPL
URL:		http://www.xfce.org
Group:		Graphical desktop/Xfce
Source0:	%{name}-%{version}.tar.bz2
# An english native speaker should feel free to update this file :)
Source1:	Mandriva
Requires:	xfce-mcs-manager
# for /usr/sbin/fndSession:
Requires:	desktop-common-data
Requires:	exo
BuildRequires:	xfce-mcs-manager-devel
BuildRequires:	libgdk_pixbuf2.0-devel
BuildRequires:	chrpath
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

%description
Xfce-utils contains utilities for the Xfce Desktop Environment.

%prep
%setup -q

%build
%configure2_5x \
	--enable-gdm \
	--sysconfdir=%{_sysconfdir}/X11 \
	--with-vendor-info=Mandriva
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

# remove unneeded devel files
rm -f %{buildroot}%{_libdir}/xfce4/mcs-plugins/*.*a

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
%doc README TODO COPYING AUTHORS
%{_bindir}/*
%{_datadir}/xfce4/*
%{_datadir}/icons/*
%config(noreplace) %{_sysconfdir}/X11/*
