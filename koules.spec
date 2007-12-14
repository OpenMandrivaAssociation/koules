%define name 		koules
%define version		1.4
%define release %mkrel 11

Summary:	Space action game for X11
Name:		%{name}
Version:	%{version}
Release:	%{release}
Group: 		Games/Arcade
URL:		http://www.paru.cas.cz/~hubicka/koules/English/koules.html
License:	GPLv2+
Source0:	%{name}-%{version}.tar.bz2
Source1:	%{name}-16.png
Source2:	%{name}-32.png
Source3:	%{name}-48.png
Patch0:		koules-debian.patch.bz2 
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}buildroot
BuildRequires:  X11-devel tk imake

%description
Koules is a fast action arcade-style game. This version is compiled for X11.
It has cool 256 color graphics, a multiplayer mode for up to 5 players, full
sound and, of course, network support. Koules is an original idea. The first
version of Koules was developed from scratch by Jan Hubicka in July 1995.

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
