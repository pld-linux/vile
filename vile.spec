Summary:	Text editor compatible with Vi
Summary(pl):	Edytor tekstu kompatybilny z Vi
Name:		vile
Version:	9.2
Release:	1
License:	GPL
Group:		Applications/Editors
Group(de):	Applikationen/Editors
Group(pl):	Aplikacje/Edytory
Group(pt):	Aplicações/Editores
# Source0:	ftp://ftp.clark.net/pub/dickey/vile/%{name}-%{version}.tgz
Source0:	ftp://invisible-island.net/vile/%{name}-%{version}.tgz
Source1:	x%{name}.desktop
Icon:		vile.xpm
URL:		http://www.clark.net/pub/dickey/vile/vile.html
BuildRequires:	ncurses-devel
BuildRequires:	XFree86-libs
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)


%description
vile is a text editor which is extremely compatible with vi in terms
of "finger feel". in addition, it has extended capabilities in many
areas, notably multi-file editing and viewing, key rebinding, and real
X window system support.

%description -l pl
vile to edytor tekstu ¶ci¶le komatybilny z Vi je¶li chodzi o
klawiszologiê. Posiada wiele przydatnych dodatków jak mo¿liwo¶æ edycji
wielu plików równocze¶nie, przemapowywanie klawiszy czy interfejs dla
X Window.

%package common
Summary:	Common files for vile and xvile
Summary(pl):	Wspólne pliki vile i xvile
Group:		Applications/Editors
Group(de):	Applikationen/Editors
Group(pl):	Aplikacje/Edytory
Group(pt):	Aplicações/Editores

%description common
This package contains common files for vile and xvile.

%description -l pl
Ten pakiet zawiera wspólne pliki vile i xvile.

%package static
Summary:	vile static
Summary(pl):	vile skompilowany statycznie
Group:		Applications/Editors
Group(de):	Applikationen/Editors
Group(pl):	Aplikacje/Edytory
Group(pt):	Aplicações/Editores
Provides:	vi
Obsoletes:	vi

%description static
The classic unix /bin/vi - small, static comiled editor which is
useful as a rescue tool.

%description static -l pl
Klasyczny unixowy /bin/vi - ma³y, skompilowany statycznie edytor,
który przydaje siê przy awarii systemu.

%package X11
Summary:	xvile (vile with X11 support)
Summary(pl):	xvile (vile dla X Window)
Group:		Applications/Editors
Group(de):	Applikationen/Editors
Group(pl):	Aplikacje/Edytory
Group(pt):	Aplicações/Editores

%description X11
xvile - vile with X11 supprt.

%description X11 -l pl
xvile - vile dla X Window.

%prep
%setup -q

%build
IMAKE_LOADFLAGS="%{rpmldflags} -static"; export IMAKE_LOADFLAGS
%configure \
	--with-screen=ncurses \
	--with-CFLAGS="%{rpmcflags}"

%{__make}
mv -f vile vile.static

%{__make} distclean
IMAKE_LOADFLAGS="%{rpmldflags}"; export IMAKE_LOADFLAGS
%configure \
	--with-screen=x11 \
	--with-locale \
	--with-CFLAGS="%{rpmcflags}"

%{__make} xvile
mv -f xvile vile.x11

%{__make} distclean
%configure \
	--with-screen=ncurses \
	--with-locale \
	--with-CFLAGS="%{rpmcflags}"

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_mandir}/man1,%{_datadir}/vile} \
	$RPM_BUILD_ROOT{%{_prefix}/X11R6/bin,/bin} \
	$RPM_BUILD_ROOT%{_applnkdir}/Office/Editors

install vile $RPM_BUILD_ROOT%{_bindir}/vile
install vile.static $RPM_BUILD_ROOT/bin/vi
install vile.x11 $RPM_BUILD_ROOT%{_prefix}/X11R6/bin/xvile
install vile.1 $RPM_BUILD_ROOT%{_mandir}/man1

install vile.hlp $RPM_BUILD_ROOT%{_datadir}/vile

%{__make} -C filters install \
	datadir=$RPM_BUILD_ROOT%{_datadir}/vile \
	bindir=$RPM_BUILD_ROOT%{_bindir}

install %{SOURCE1} $RPM_BUILD_ROOT%{_applnkdir}/Office/Editors

gzip -9nf README* CHANGES* doc/*

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/vile

%files common
%defattr(644,root,root,755)
%doc {*,doc/*}.gz
%{_mandir}/man1/vile.1*
%attr(755,root,root) %{_bindir}/vile-*
%{_datadir}/vile

%files static
%defattr(644,root,root,755)
%attr(755,root,root) /bin/vi

%files X11
%defattr(644,root,root,755)
%attr(755,root,root) %{_prefix}/X11R6/bin/xvile
%{_applnkdir}/Office/Editors/xvile.desktop
