#
# Conditional build:
%bcond_without	static	# don't build static version
#
Summary:	Text editor compatible with Vi
Summary(pl.UTF-8):	Edytor tekstu kompatybilny z Vi
Name:		vile
Version:	9.6
Release:	1
License:	GPL v2
Group:		Applications/Editors
Source0:	ftp://invisible-island.net/vile/%{name}-%{version}.tgz
# Source0-md5:	3695e234f4e7e9038450876f44832613
Source1:	x%{name}.desktop
Patch0:		%{name}-ac_fix.patch
URL:		http://invisible-island.net/vile/
BuildRequires:	automake
BuildRequires:	ncurses-devel
BuildRequires:	xorg-lib-libXt-devel
%if %{with static}
BuildRequires:	glibc-static
BuildRequires:	ncurses-static
%endif
Requires:	%{name}-common = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
vile is a text editor which is extremely compatible with vi in terms
of "finger feel". in addition, it has extended capabilities in many
areas, notably multi-file editing and viewing, key rebinding, and real
X window system support.

%description -l pl.UTF-8
vile to edytor tekstu ściśle kompatybilny z Vi jeśli chodzi o
klawiszologię. Posiada wiele przydatnych dodatków jak możliwość edycji
wielu plików równocześnie, przemapowywanie klawiszy czy interfejs dla
X Window.

%package common
Summary:	Common files for vile and xvile
Summary(pl.UTF-8):	Wspólne pliki vile i xvile
Group:		Applications/Editors

%description common
This package contains common files for vile and xvile.

%description common -l pl.UTF-8
Ten pakiet zawiera pliki wspólne dla vile i xvile.

%package static
Summary:	vile static
Summary(pl.UTF-8):	vile skompilowany statycznie
Group:		Applications/Editors
Provides:	vi
Obsoletes:	vi

%description static
The classic Unix /bin/vi - small, static comiled editor which is
useful as a rescue tool.

%description static -l pl.UTF-8
Klasyczny uniksowy /bin/vi - mały, skompilowany statycznie edytor,
który przydaje się przy awarii systemu.

%package X11
Summary:	xvile (vile with X11 support)
Summary(pl.UTF-8):	xvile (vile dla X Window System)
Group:		X11/Applications/Editors
Requires:	%{name}-common = %{version}-%{release}

%description X11
xvile - vile with X11 support.

%description X11 -l pl.UTF-8
xvile - vile dla X Window.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
cp -f /usr/share/automake/config.sub .
%if %{with static}
LDFLAGS="%{rpmldflags} -static"
%configure \
	--with-screen=ncurses \
	--without-x \
	--with-cflags="%{rpmcflags}"

%{__make} \
	LIBS="-lcrypt -lncurses -ltinfo"
mv -f vile vile.static
%{__make} distclean
%endif

LDFLAGS="%{rpmldflags}"; export LDFLAGS
%configure \
	--with-screen=x11 \
	--with-locale \
	--with-cflags="%{rpmcflags}"

%{__make} xvile
mv -f xvile vile.x11
%{__make} distclean

%configure \
	--with-screen=ncurses \
	--with-locale \
	--with-cflags="%{rpmcflags}"

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
%{_desktopdir}/*.desktop
