#
# Conditional build:
%bcond_without	static	# don't build static version
#
Summary:	Text editor compatible with Vi
Summary(pl):	Edytor tekstu kompatybilny z Vi
Name:		vile
Version:	9.4
Release:	2
License:	GPL
Group:		Applications/Editors
# Source0:	ftp://ftp.clark.net/pub/dickey/vile/%{name}-%{version}.tgz
Source0:	ftp://invisible-island.net/vile/%{name}-%{version}.tgz
# Source0-md5:	1c69045467b7c48be99fa7ac2052a95f
Source1:	x%{name}.desktop
Patch0:		%{name}-ac_fix.patch
Patch1:		%{name}-nolibs.patch
Icon:		vile.xpm
URL:		http://www.clark.net/pub/dickey/vile/vile.html
BuildRequires:	XFree86-devel
BuildRequires:	autoconf
BuildRequires:	automake
%{?with_static:BuildRequires:	glibc-static}
BuildRequires:	ncurses-devel
%{?with_static:BuildRequires:	ncurses-static}
Requires:	%{name}-common = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
vile is a text editor which is extremely compatible with vi in terms
of "finger feel". in addition, it has extended capabilities in many
areas, notably multi-file editing and viewing, key rebinding, and real
X window system support.

%description -l pl
vile to edytor tekstu �ci�le kompatybilny z Vi je�li chodzi o
klawiszologi�. Posiada wiele przydatnych dodatk�w jak mo�liwo�� edycji
wielu plik�w r�wnocze�nie, przemapowywanie klawiszy czy interfejs dla
X Window.

%package common
Summary:	Common files for vile and xvile
Summary(pl):	Wsp�lne pliki vile i xvile
Group:		Applications/Editors

%description common
This package contains common files for vile and xvile.

%description common -l pl
Ten pakiet zawiera pliki wsp�lne dla vile i xvile.

%package static
Summary:	vile static
Summary(pl):	vile skompilowany statycznie
Group:		Applications/Editors
Provides:	vi
Obsoletes:	vi

%description static
The classic unix /bin/vi - small, static comiled editor which is
useful as a rescue tool.

%description static -l pl
Klasyczny uniksowy /bin/vi - ma�y, skompilowany statycznie edytor,
kt�ry przydaje si� przy awarii systemu.

%package X11
Summary:	xvile (vile with X11 support)
Summary(pl):	xvile (vile dla X Window)
Group:		Applications/Editors
Requires:	%{name}-common = %{version}-%{release}

%description X11
xvile - vile with X11 support.

%description X11 -l pl
xvile - vile dla X Window.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
cp -f /usr/share/automake/config.sub .
rm -f configure
%{__autoheader}
%{__autoconf}
%if %{with static}
IMAKE_LOADFLAGS="%{rpmldflags} -static"; export IMAKE_LOADFLAGS
%configure \
	--with-screen=ncurses \
	--with-CFLAGS="%{rpmcflags}"

%{__make} \
	LIBS="-lcrypt -lncurses -ltinfo"
mv -f vile vile.static
%{__make} distclean
%endif

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
install -d $RPM_BUILD_ROOT{%{_bindir},/bin,%{_mandir}/man1,%{_datadir}/vile} \
	$RPM_BUILD_ROOT%{_desktopdir}

install vile $RPM_BUILD_ROOT%{_bindir}/vile
%{?with_static:install vile.static $RPM_BUILD_ROOT/bin/vi}
install vile.x11 $RPM_BUILD_ROOT%{_bindir}/xvile
install vile.1 $RPM_BUILD_ROOT%{_mandir}/man1

install vile.hlp $RPM_BUILD_ROOT%{_datadir}/vile

%{__make} -C filters install \
	datadir=$RPM_BUILD_ROOT%{_datadir}/vile \
	bindir=$RPM_BUILD_ROOT%{_bindir}

install %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/vile

%files common
%defattr(644,root,root,755)
%doc README* CHANGES* doc/*
%{_mandir}/man1/vile.1*
%attr(755,root,root) %{_bindir}/atr2*
%attr(755,root,root) %{_bindir}/vile-*
%{_datadir}/vile

%if %{with static}
%files static
%defattr(644,root,root,755)
%attr(755,root,root) /bin/vi
%endif

%files X11
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/xvile
%{_desktopdir}/*
