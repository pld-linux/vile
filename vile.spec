Summary:	Text editor compatible with Vi
Summary(pl):	Edytor tekstu kompatybilny z Vi
Name:		vile
Version:	8.3
Release:	2
Group:		Applications/Editors
Group(pl):	Aplikacje/Edytory
Copyright:	GPL
Source:		ftp://ftp.clark.net/pub/dickey/vile/%{name}-%{version}.tgz
URL:		http://www.clark.net/pub/dickey/vile/
BuildPrereq:	ncurses-devel
BuildPrereq:	XFree86-libs
BuildRoot:   	/tmp/%{name}-%{version}-root

%description
vile is a text editor which is extremely compatible with vi in terms
of "finger feel".  in addition, it has extended capabilities in many areas,
notably multi-file editing and viewing, key rebinding, and real X window
system support.

%description -l pl
vile to edytor tekstu ¶ci¶le komatybilny z Vi je¶li chodzi o klawiszologiê.
Posiada wiele przydatnych dodatków jak mo¿liwo¶æ edycji wielu plików
równocze¶nie, przemapowywanie klawiszy czy interfejs dla X Window.

%package common
Summary:	Common files for vile and xvile
Summary(pl):	Wspólne pliki vile i xvile
Group:		Applications/Editors
Group(pl):	Aplikacje/Edytory

%description common
This package contains common files for vile and xvile.

%description -l pl
Ten pakiet zawiera wspólne pliki vile i xvile.

%package static
Summary:	vile static
Summary(pl):	vile skompilowany statycznie
Group:		Applications/Editors
Group(pl):	Aplikacje/Edytory
Provides:	vi
Obsoletes:	vi

%description static
The classic unix /bin/vi - small, static comiled editor which is useful
as a rescue tool.

%description static -l pl
Klasyczny unixowy /bin/vi - ma³y, skompilowany statycznie edytor, który
przydaje siê przy awarii systemu.

%package X11
Summary:	xvile (vile with X11 support)
Summary(pl):	xvile (vile dla X Window)
Group:		Applications/Editors
Group(pl):	Aplikacje/Edytory

%description X11
xvile - vile with X11 supprt.

%description X11 -l pl
xvile - vile dla X Window.

%prep
%setup -q

%build
CFLAGS="$RPM_OPT_FLAGS" LDFLAGS="-static -s" \
./configure %{_target_platform} \
	--prefix=%{_prefix} \
	--with-screen=ncurses
make
mv vile vile.static
make distclean

CFLAGS="$RPM_OPT_FLAGS" LDFLAGS="-s" \
./configure %{_target_platform} \
	--prefix=%{_prefix} \
	--with-screen=x11
make xvile
mv xvile vile.x11
make distclean

CFLAGS="$RPM_OPT_FLAGS" LDFLAGS="-s" \
./configure \
	--prefix=%{_prefix} \
	--with-screen=ncurses
make

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_mandir}/man1,/usr/X11R6/bin,/bin}

install -s vile		$RPM_BUILD_ROOT%{_bindir}/vile
install -s vile.static	$RPM_BUILD_ROOT/bin/vi
install -s vile.x11	$RPM_BUILD_ROOT/usr/X11R6/bin/xvile
install -s vile-*	$RPM_BUILD_ROOT%{_bindir}
install    vile.1	$RPM_BUILD_ROOT%{_mandir}/man1

gzip -9nf $RPM_BUILD_ROOT%{_mandir}/man*/* README* CHANGES* doc/*

%clean
rm -rf $RPM_BUILD_ROOT

%files
%attr(755,root,root) %{_bindir}/vile

%files common
%defattr(644,root,root,755)
%doc {*,doc/*}.gz
%{_mandir}/man1/vile.1.gz
%attr(755,root,root) %{_bindir}/vile-*

%files static
%attr(755,root,root) /bin/vi

%files X11
%attr(755,root,root) /usr/X11R6/bin/xvile
