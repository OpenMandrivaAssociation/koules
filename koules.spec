%define name 		koules
%define version		1.4
%define release %mkrel 15

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
BuildRequires:	libxext-devel
BuildRequires:	libx11-devel
BuildRequires:	libxau-devel
BuildRequires:	libxdmcp-devel
BuildRequires:	libxcb-devel

%description
Koules is a fast action arcade-style game.  It has cool 256 color graphics, a
multiplayer mode for up to 5 players, full sound and, of course, network
support.

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
Exec=%{_bindir}/%{name}
Icon=%{name}
Terminal=false
Type=Application
Categories=Game;ArcadeGame;
EOF

# mdk icon
install -m644 %{SOURCE1} -D $RPM_BUILD_ROOT%{_miconsdir}/%{name}.png
install -m644 %{SOURCE2} -D $RPM_BUILD_ROOT%{_iconsdir}/%{name}.png
install -m644 %{SOURCE3} -D $RPM_BUILD_ROOT%{_liconsdir}/%{name}.png

%post
%{update_menus}

%postun
%{clean_menus}

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
