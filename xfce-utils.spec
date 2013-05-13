%define url_ver %(echo %{version} | cut -c 1-3)

Summary:	Utilities for the Xfce Desktop Environment
Name:		xfce-utils
Version:	4.8.3
Release:	ZED'S DEAD BABY
License:	GPLv2+
URL:		http://www.xfce.org
Group:		Graphical desktop/Xfce
Source0:	http://archive.xfce.org/src/xfce/%{name}/%{url_ver}/%{name}-%{version}.tar.bz2
# An english native speaker should feel free to update this file :)
Source1:	Mandriva
Source2:	06Xfce
Source3:	xfce4.sh
Source4:	xfce4.pam
Patch5:		%{name}-4.8.2-xinitrc.patch
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


%changelog
* Fri Sep 23 2011 Tomasz Pawel Gajc <tpg@mandriva.org> 4.8.3-1
+ Revision: 701028
- update to new version 4.8.3

* Sat Jul 30 2011 Tomasz Pawel Gajc <tpg@mandriva.org> 4.8.2-3
+ Revision: 692482
- rediff patch 5

* Sat Jul 30 2011 Tomasz Pawel Gajc <tpg@mandriva.org> 4.8.2-2
+ Revision: 692471
- drop patch 5, not needed anymore

* Sat Jun 18 2011 Tomasz Pawel Gajc <tpg@mandriva.org> 4.8.2-1
+ Revision: 685912
- update to new version 4.8.2

* Sat Mar 12 2011 Funda Wang <fwang@mandriva.org> 4.8.1-2
+ Revision: 643886
- rebuild to obsolete old packages

* Wed Feb 02 2011 Tomasz Pawel Gajc <tpg@mandriva.org> 4.8.1-1
+ Revision: 635006
- update to new version 4.8.1

* Sun Jan 23 2011 Tomasz Pawel Gajc <tpg@mandriva.org> 4.8.0-1
+ Revision: 632412
- update to new version 4.8.0

* Thu Jan 06 2011 Tomasz Pawel Gajc <tpg@mandriva.org> 4.7.4-1mdv2011.0
+ Revision: 629134
- update to new version 4.7.4

* Wed Dec 08 2010 Tomasz Pawel Gajc <tpg@mandriva.org> 4.7.3-1mdv2011.0
+ Revision: 616356
- update to new version 4.7.3

* Sat Dec 04 2010 Tomasz Pawel Gajc <tpg@mandriva.org> 4.7.2-1mdv2011.0
+ Revision: 609458
- update to new version 4.7.2

* Mon Nov 08 2010 Götz Waschk <waschk@mandriva.org> 4.7.1-2mdv2011.0
+ Revision: 595069
- fix installation of credits file (bug #61562)

* Sun Nov 07 2010 Tomasz Pawel Gajc <tpg@mandriva.org> 4.7.1-1mdv2011.0
+ Revision: 594784
- update to new version 4.7.1
- rediff patch 5
- drop patch 6, fixed by upstream
- fix file list
- drop old conditions in spec file for mdv release older than 200900

* Sat Sep 18 2010 Tomasz Pawel Gajc <tpg@mandriva.org> 4.7.0-1mdv2011.0
+ Revision: 579569
- update to new version 4.7.0
- drop patches 0, 4, 8 and 11
- rediff patch 5
- adjust buildrequires
- fix file list

* Sat Sep 11 2010 Tomasz Pawel Gajc <tpg@mandriva.org> 4.6.2-6mdv2011.0
+ Revision: 577404
- do not spawn yet another one session

* Sat Sep 11 2010 Tomasz Pawel Gajc <tpg@mandriva.org> 4.6.2-5mdv2011.0
+ Revision: 577141
- launch xfce4-session with dbus-launch

* Wed Sep 08 2010 Michael Scherer <misc@mandriva.org> 4.6.2-4mdv2011.0
+ Revision: 576710
- reuse dash, as tpg found the real issue ( missing () for function definition )

* Sun Sep 05 2010 Michael Scherer <misc@mandriva.org> 4.6.2-3mdv2011.0
+ Revision: 576130
- fix xfce start breakage ( ie, xfce started as root when gdm start )

* Sat Sep 04 2010 Tomasz Pawel Gajc <tpg@mandriva.org> 4.6.2-2mdv2011.0
+ Revision: 576003
- rework patch 5, make it dash compliant, also use dash by default

* Fri Jul 16 2010 Tomasz Pawel Gajc <tpg@mandriva.org> 4.6.2-1mdv2011.0
+ Revision: 553897
- update to new version 4.6.2

* Fri Jun 04 2010 Tomasz Pawel Gajc <tpg@mandriva.org> 4.6.1-6mdv2010.1
+ Revision: 547078
- remove ck-launch-session form 06Xfce file (mdv #58842)

* Mon Apr 19 2010 Ahmad Samir <ahmadsamir@mandriva.org> 4.6.1-5mdv2010.1
+ Revision: 536814
- revert previous patch, ck-launch-session is already used via
  /etc/X11/wmsession.d/06Xfce

* Sat Apr 10 2010 Tomasz Pawel Gajc <tpg@mandriva.org> 4.6.1-4mdv2010.1
+ Revision: 533557
- Patch11: register ConsoleKit session (mdvbz #56150)

* Tue Jul 07 2009 Tomasz Pawel Gajc <tpg@mandriva.org> 4.6.1-3mdv2010.0
+ Revision: 393344
- bump release tag, because BS is hungry
- add requires on iceauth (mdvbz #52099)

* Wed Apr 22 2009 Tomasz Pawel Gajc <tpg@mandriva.org> 4.6.1-1mdv2010.0
+ Revision: 368746
- update to new version 4.6.1

* Thu Mar 05 2009 Tomasz Pawel Gajc <tpg@mandriva.org> 4.6.0-4mdv2009.1
+ Revision: 349303
- rebuild
- rebuild whole xfce

* Sat Feb 28 2009 Tomasz Pawel Gajc <tpg@mandriva.org> 4.6.0-2mdv2009.1
+ Revision: 346152
- Patch8: rediff and reenable it

* Sat Feb 28 2009 Jérôme Soyer <saispo@mandriva.org> 4.6.0-1mdv2009.1
+ Revision: 346001
- Disable Patch8

* Mon Feb 23 2009 Tomasz Pawel Gajc <tpg@mandriva.org> 4.5.99.1-2mdv2009.1
+ Revision: 344116
- Patch5: this is not the place to source scripts from /etc/X11/xinit.d

* Tue Jan 27 2009 Tomasz Pawel Gajc <tpg@mandriva.org> 4.5.99.1-1mdv2009.1
+ Revision: 333945
- update to new version 4.5.99.1
- Patch5: rediff

* Mon Jan 19 2009 Tomasz Pawel Gajc <tpg@mandriva.org> 4.5.93-2mdv2009.1
+ Revision: 331252
- fix the path for xfce configs for xinitrc file

* Thu Jan 15 2009 Jérôme Soyer <saispo@mandriva.org> 4.5.93-1mdv2009.1
+ Revision: 329673
- Remove patch3 fixed upstream

  + Tomasz Pawel Gajc <tpg@mandriva.org>
    - Patch5: source scripts from /etc/X11/xinit.d directory
    - update url in vendor file info for Mandriva's Xfce wiki
    - update to new version 4.5.93

* Wed Jan 07 2009 Götz Waschk <waschk@mandriva.org> 4.5.92-7mdv2009.1
+ Revision: 326748
- fix desktop entry

* Thu Dec 11 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 4.5.92-6mdv2009.1
+ Revision: 313398
- run %%make_dm_session for post scriplet

* Sat Nov 29 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 4.5.92-5mdv2009.1
+ Revision: 307569
- fix path for env script

* Mon Nov 24 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 4.5.92-4mdv2009.1
+ Revision: 306483
- Patch5: backport from 4.4.2

* Sun Nov 23 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 4.5.92-3mdv2009.1
+ Revision: 306040
- remove xsession desktop file
- add env script
- add pam rules
- set DESKTOP var

* Sat Nov 22 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 4.5.92-2mdv2009.1
+ Revision: 305947
- add session file
- add full path for the Source0

* Sat Nov 15 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 4.5.92-1mdv2009.1
+ Revision: 303455
- update to new version 4.5.92 (Xfce 4.6 Beta 2 Hopper)

* Sat Oct 18 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 4.5.91-2mdv2009.1
+ Revision: 294973
- Patch10: use thunar instread of depreciated xftree4
- drop patch 1 and 9
- rediff patch 5
- spef file clean

* Thu Oct 16 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 4.5.91-1mdv2009.1
+ Revision: 294413
- Xfce4.6 beta1 is landing on cooker
- drop patche7 and temporaily disable patches 1 and 9
- fix file list

* Mon Sep 22 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 4.4.2-26mdv2009.0
+ Revision: 286672
- Patch5: remove some code, as it is now handled dirrefently by mandriva-xfce-config package

* Tue Sep 09 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 4.4.2-25mdv2009.0
+ Revision: 283231
- Patch7: enable for mdv newer than 2008.1, as it needs never glib than 2.13 (#40462)

* Sun Sep 07 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 4.4.2-23mdv2009.0
+ Revision: 282242
- move Xft.xrdb file to mandriva-xfce-config package

* Wed Jul 02 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 4.4.2-22mdv2009.0
+ Revision: 230855
- Patch9: convert xfrun labels to utf-8 (upstream bug #3543)

* Wed Jun 25 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 4.4.2-21mdv2009.0
+ Revision: 228807
- Patch5: do not run ssh-agent and do not execute dbus-launch, because it is handled differently already, also do not ovveride xsetroot settings

* Mon May 12 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 4.4.2-20mdv2009.0
+ Revision: 206288
- fix sysconfdir path for mdv release 2009 and newer
- change sysconfdir from /etc/X11/xdg to /etc/xdg only for Mandriva releases newer than 2008.1

* Sun May 04 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 4.4.2-19mdv2009.0
+ Revision: 201087
- Patch8: pass /etc/xdg and /etc/X11/xdg in the startxfce script

* Wed Apr 30 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 4.4.2-18mdv2009.0
+ Revision: 199346
- switch xlockmore with xscreensaver

* Sun Apr 20 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 4.4.2-17mdv2009.0
+ Revision: 196013
- Patch5: fix regression introduced in last commit

* Sun Apr 20 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 4.4.2-16mdv2009.0
+ Revision: 195974
- Patch5: be more carefull when creating mdv's specific icons on desktop
- add one more person to the hall of fame

* Wed Apr 16 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 4.4.2-15mdv2009.0
+ Revision: 194767
- Patch5: export gtkrc file specific to mandriva and xfce theme (thanks to GTK2_RC_FILES)
- Patch7: use a real GtkComboBoxEntry (Xfce upstream bug #3820)

* Wed Mar 19 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 4.4.2-14mdv2008.1
+ Revision: 188840
- merge patch 2 into patch 5
- Patch5: rediff, do not start pulseaudio daemon(this is not the place and time for this)
- Patch6: prevent about dialog box resize on startup

* Thu Mar 13 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 4.4.2-13mdv2008.1
+ Revision: 187456
- Patch5: rediff, fix directory name for notification-daemon-xfce settings

* Wed Mar 12 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 4.4.2-12mdv2008.1
+ Revision: 187090
- Patch5: rediff, copy register.desktop and upgrade.desktop on user's desktop only for given mdv flavour

* Mon Mar 03 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 4.4.2-11mdv2008.1
+ Revision: 178196
- add Dr_ST to the hall of fame ;-)

* Fri Feb 29 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 4.4.2-10mdv2008.1
+ Revision: 176620
- Patch5: rediff, add option to add xfce preferneces if doesn't exist

* Sun Feb 24 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 4.4.2-9mdv2008.1
+ Revision: 174371
- fix typo in requires

* Sat Feb 23 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 4.4.2-8mdv2008.1
+ Revision: 174097
- Patch5: start pulseaudio as a deamon at Xfce lauch (only for mdv 2008.1 and higher)
- requires xflockmore

* Mon Feb 18 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 4.4.2-7mdv2008.1
+ Revision: 170067
- require xdg-user-dirs-gtk

* Sun Jan 27 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 4.4.2-6mdv2008.1
+ Revision: 158492
- add requires on xinit
- check wheter screensaver is running, patch 4

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

* Tue Dec 18 2007 Tomasz Pawel Gajc <tpg@mandriva.org> 4.4.2-5mdv2008.1
+ Revision: 132005
- add patch 3, which shows xfce version by using --xfce-version option

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sat Nov 24 2007 Tomasz Pawel Gajc <tpg@mandriva.org> 4.4.2-4mdv2008.1
+ Revision: 111774
- update tarball

* Fri Nov 23 2007 Jérôme Soyer <saispo@mandriva.org> 4.4.2-3mdv2008.1
+ Revision: 111614
- Add one contributors

* Tue Nov 20 2007 Tomasz Pawel Gajc <tpg@mandriva.org> 4.4.2-2mdv2008.1
+ Revision: 110665
- add missing buildrequires on dbus-glib-devel
- fix file list

* Sun Nov 18 2007 Tomasz Pawel Gajc <tpg@mandriva.org> 4.4.2-1mdv2008.1
+ Revision: 110001
- drop patch 0 (fixed upstream)
- set Thunar as a default browser
- set Terminal as a default terminal application
- fix file list
- hardcode buildrequires to a specific xfce version
- new version
- new license policy
- add some explicit options to configure

* Mon Sep 24 2007 Tomasz Pawel Gajc <tpg@mandriva.org> 4.4.1-7mdv2008.0
+ Revision: 92543
- add Scara
- add Dotan Kamberd
- fix "about" info, make it utf-8

* Tue Sep 18 2007 Tomasz Pawel Gajc <tpg@mandriva.org> 4.4.1-6mdv2008.0
+ Revision: 89662
- requires dbus-x11

* Sat Aug 25 2007 Tomasz Pawel Gajc <tpg@mandriva.org> 4.4.1-5mdv2008.0
+ Revision: 71412
- provide patch 2 (xinitrc with cpp)
- remove unneeded configure scripts
- update mandriva file

* Mon Jul 23 2007 Tomasz Pawel Gajc <tpg@mandriva.org> 4.4.1-4mdv2008.0
+ Revision: 54512
- add missing icon to the startup script (closes bug #29095)

* Tue Jun 26 2007 Tomasz Pawel Gajc <tpg@mandriva.org> 4.4.1-3mdv2008.0
+ Revision: 44285
- disable builing of static files rather than deleting them
- fix file list
- own proper configuration files
- set default browser and terminal
- add P0
- update description

* Fri May 25 2007 Tomasz Pawel Gajc <tpg@mandriva.org> 4.4.1-2mdv2008.0
+ Revision: 31215
- use macros in %%post and %%postun
- add Mandriva file - information about vendor
- spec file clean

* Wed Apr 18 2007 Jérôme Soyer <saispo@mandriva.org> 4.4.1-1mdv2008.0
+ Revision: 14663
- New release 4.4.1


* Fri Jan 26 2007 Jérôme Soyer <saispo@mandriva.org> 4.4.0-1mdv2007.0
+ Revision: 113679
- Fix dbus

  + plouf <plouf>
    - New release 4.4.0

* Fri Dec 29 2006 Jérôme Soyer <saispo@mandriva.org> 4.3.99.2-1mdv2007.1
+ Revision: 102553
- Remove dbus file
- New release 4.3.99.2

  + Nicolas Lécureuil <neoclust@mandriva.org>
    - import xfce-utils-4.3.90.2-1mdv2007.0

* Tue Jul 11 2006 Charles A Edwards <eslrahc@mandriva.org> 4.3.90.2-1mdv2007.0
- 4.3.90.2 (Xfce-4.4 beta2)

* Wed Apr 19 2006 trem <trem@mandriva.org> 4.3.90.1-1mdk
- 4.3.90.1

* Sat Mar 11 2006 Marcel Pol <mpol@mandriva.org> 4.3.0-0.svn_r20246.1mdk
- svn r20246
- drop P2, 3, using exo-open now
- don't require libxfcegui4-plugins anymore

* Sun Feb 05 2006 Marcel Pol <mpol@mandriva.org> 4.3.0-0.svn_r19739.1mdk
- 4.3.0 svn r19739
- don't run libtoolize
- update filelist
- rediff P2
- P3, use www-browser as preferred browser

* Fri Jan 13 2006 Marcel Pol <mpol@mandriva.org> 4.2.3-1mdk
- 4.2.3
- remove more unneeded devel files

* Wed May 25 2005 Marcel Pol <mpol@mandriva.org> 4.2.2-1mdk
- 4.2.2
- %%{1}mdv2007.1
- requires desktop-common-data

* Sat Apr 30 2005 Marcel Pol <mpol@mandriva.org> 4.2.1-2mdk
- use xvt as default terminal
  use -e and -T for execute and title

* Wed Mar 16 2005 Charles A Edwards <eslrahc@mandrake.org> 4.2.1-1mdk
- 4.2.1

* Sat Jan 22 2005 Marcel Pol <mpol@mandrake.org> 4.2.0-3mdk
- P0, run taskbar by default

* Sat Jan 22 2005 Marcel Pol <mpol@mandrake.org> 4.2.0-2mdk
- group: Graphical desktop/Xfce
- fix P1
- remove unneeded devel files

* Tue Jan 18 2005 Charles A Edwards <eslrahc@mandrake.org> 4.2.0-1mdk
- 4.2.0 Final

* Mon Dec 27 2004 Marcel Pol <mpol@mandrake.org> 4.1.99.3-2mdk
- disable P1 for now, it breaks

* Sun Dec 26 2004 Marcel Pol <mpol@mandrake.org> 4.1.99.3-1mdk
- 4.1.99.3 (4.2.0 RC 3)
- rediff P0
- P1, disable compositor by default

* Sun Dec 12 2004 Charles A Edwards <eslrahc@mandrake.org> 4.1.99.2-1mdk
- 4.1.99.2 (4.2.0 RC 2)
- drop P1

* Tue Nov 16 2004 Marcel Pol <mpol@mandrake.org> 4.1.99.1-2mdk
- require libxfcegui4-plugins

* Tue Nov 16 2004 Marcel Pol <mpol@mandrake.org> 4.1.99.1-1mdk
- 4.1.99.1
- s/XFce/Xfce
- rediff and integrate p0 and p1 for xinitrc script
- update filelist
- remove rpath from xfrun4

* Sat Oct 02 2004 Frederic Crozat <fcroza@mandrakesoft.com> 4.0.6-2mdk
- Patch1: don't touch background at startup

* Tue Jul 13 2004 Charles A Edwards <eslrahc@mandrake.org> 4.0.6-1mdk
- 4.0.6
- reenable libtoolize

* Sun Apr 18 2004 Charles A Edwards <eslrahc@mandrake.org> 4.0.5-1mdk
- 4.0.5
- rm desktop files

* Sat Apr 10 2004 Charles A Edwards <eslrahc@mandrake.org> 4.0.4-1mdk
- 4.0.4

 * Sat Jan 10 2004 Charles A Edwards <eslrahc@mandrake.org> 4.0.3-1mdk
- 4.0.3

