%define name 		koules
%define version		1.4
%define release %mkrel 19

Summary:	Space action game for X11
Name:		%{name}
Version:	%{version}
Release:	%{release}
Group: 		Games/Arcade
URL:		http://www.ucw.cz/~hubicka/koules/English/distribution.html
License:	GPLv2+
Source0:	%{name}-%{version}.tar.bz2
Source1:	%{name}-16.png
Source2:	%{name}-32.png
Source3:	%{name}-48.png
Patch0:		debian-koules-1.4-17.patch
# this font is hardcoded in the code
Requires:	x11-font-schumacher-misc
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}buildroot
BuildRequires:  tk imake
BuildRequires:	pkgconfig(xext)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xau)
BuildRequires:	pkgconfig(xdmcp)
BuildRequires:  pkgconfig(xcb)	

%description
Koules is a simple fast-action arcade-style no-brainer balls game you have
never seen alike before! It has simple, classic, old-school fantastic 256
color graphics, a multiplayer mode for up to 5 players on the same keyboard,
or via network, full sound, and, of course, lots of wild fun!

%prep

%setup -q -n %{name}%{version}
%patch0 -p1 
sed -i 's/mkdirhier/mkdir -p/g' Imakefile

%build
xmkmf
make Makefile
make Makefiles
if [ ! -s xkoules.man ]; then ln -sf xkoules.6 xkoules.man; fi
%make KOULESDIR=%{_gamesbindir} SOUNDDIR=%{_libdir}/%{_gamesdir}/%{name} MANDIR=%{_mandir}/man6

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall KOULESDIR=%{buildroot}%{_gamesbindir} SOUNDDIR=%{buildroot}%{_libdir}/%{_gamesdir}/%{name} MANDIR=%{buildroot}/%{_mandir}/man6 
mv %{buildroot}%{_gamesbindir}/xkoules %{buildroot}%{_gamesbindir}/xkoules.bin
cat <<EOF >%{buildroot}%{_gamesbindir}/xkoules
#!/bin/sh
exec soundwrapper %{_gamesbindir}/xkoules.bin
EOF
chmod a+x %{buildroot}%{_gamesbindir}/xkoules

install startkoules %{buildroot}%{_gamesbindir}/
install koules.tcl %{buildroot}%{_libdir}/%{_gamesdir}/%{name}

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=XKoules
Comment=%{summary}
Exec=%{_gamesbindir}/xkoules
Icon=%{name}
Terminal=false
Type=Application
Categories=Game;ArcadeGame;
EOF

# mdk icon
install -m644 %{SOURCE1} -D $RPM_BUILD_ROOT%{_miconsdir}/%{name}.png
install -m644 %{SOURCE2} -D $RPM_BUILD_ROOT%{_iconsdir}/%{name}.png
install -m644 %{SOURCE3} -D $RPM_BUILD_ROOT%{_liconsdir}/%{name}.png

%if %mdkversion < 200900
%post
%{update_menus}
%endif

%if %mdkversion < 200900
%postun
%{clean_menus}
%endif

%clean
rm -fr %{buildroot};

%files
%defattr(-,root,root)
%doc ChangeLog ANNOUNCE BUGS Card Koules.FAQ Problems README TODO
%{_datadir}/applications/mandriva-%{name}.desktop
%{_gamesbindir}/*
%{_mandir}/*/*
%{_iconsdir}/*.png
%{_liconsdir}/*.png
%{_miconsdir}/*.png
%{_libdir}/%{_gamesdir}/%{name}


%changelog
* Sun Mar 29 2009 Michael Scherer <misc@mandriva.org> 1.4-19mdv2009.1
+ Revision: 362120
- fix BuildRequires on x86_64
- fix 49274, by using the proper path

* Fri Jul 25 2008 Thierry Vignaud <tvignaud@mandriva.com> 1.4-18mdv2009.0
+ Revision: 247859
- rebuild

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas

* Tue Feb 19 2008 Gustavo De Nardin <gustavodn@mandriva.com> 1.4-16mdv2008.1
+ Revision: 173143
- super improved description for the new millennium

* Tue Feb 19 2008 Thierry Vignaud <tvignaud@mandriva.com> 1.4-15mdv2008.1
+ Revision: 173064
- description is not changelog nor about X11

* Tue Feb 19 2008 Gustavo De Nardin <gustavodn@mandriva.com> 1.4-14mdv2008.1
+ Revision: 172935
- new URL

* Tue Feb 19 2008 Gustavo De Nardin <gustavodn@mandriva.com> 1.4-13mdv2008.1
+ Revision: 172934
- require hardcoded font, so the game runs
- use soundwrapper to run

* Tue Feb 19 2008 Gustavo De Nardin <gustavodn@mandriva.com> 1.4-12mdv2008.1
+ Revision: 172927
- finer X11 buildrequires
- apply new debian patch
- updated patch of debian patches to koules-1.4-17, with the following ones,
  in order (well, all but the kfreebsd one):
  000_build_rules.diff, 050_defines.diff, 100_spelling.diff,
  101_buffer_overflow.diff, 102_includes.diff, 103_asm.diff, 104_types.diff,
  105_save_file.diff, 106_shm_check.diff, 107_fix_xsynchronize.diff,
  108_use_right_visual.diff, 200_tcl.diff, 109_fpe_fix.diff

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tvignaud@mandriva.com>
    - kill re-definition of %%buildroot on Pixel's request

* Fri Dec 14 2007 Funda Wang <fundawang@mandriva.org> 1.4-11mdv2008.1
+ Revision: 119635
- drop old menu

* Fri Apr 20 2007 Pascal Terjan <pterjan@mandriva.org> 1.4-10mdv2008.0
+ Revision: 15231
- Buildrequires imake
- Import koules



* Thu Jul 13 2006 Nicolas Lécureuil <neoclust@mandriva.org> 1.4-9mdv2007.0
- XDG
- use mkrel

* Thu Jul 15 2005 Pascal Terjan <pterjan@mandriva.org> 1.4-8mdk
- Don't own %%{_miconsdir} and %%{_liconsdir}

* Wed Jan 26 2005 Pascal Terjan <pterjan@mandrake.org> 1.4-7mdk
- BuildRequires tk, in order to avoid an automated require on /usr/bin/wish 

* Sun Jan 16 2005 Pascal Terjan <pterjan@mandrake.org> 1.4-6mdk
- BuildRequires X11 for rman

* Tue Jul 20 2004 Pascal Terjan <pterjan@mandrake.org> 1.4-5mdk
- update menu section

* Wed Dec 24 2003 Pascal Terjan <CMoi@tuxfamily.org> 1.4-4mdk
- s/gamedir/gamesdir/

* Mon Dec 22 2003 Pascal Terjan <CMoi@tuxfamily.org> 1.4-3mdk
- Fix Makefile to remove build dependency upon XFree86

* Mon Dec 22 2003 Pascal Terjan <CMoi@tuxfamily.org> 1.4-2mdk 
- add BuildRequires XFree86 for mkdirhier

* Mon Dec 22 2003 Pascal Terjan <CMoi@tuxfamily.org> 1.4-1mdk
- New rpm based on debian package
- 
