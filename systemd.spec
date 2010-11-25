#

%bcond_with	gtk	# build gtk tools

Summary:	systemd - a system and service manager for Linux
Summary(pl.UTF-8):	systemd - zarządca systemu i usług dla Linuksa
Name:		systemd
Version:	15
Release:	0.1
License:	GPL v2+
Group:		Base
Source0:	http://www.freedesktop.org/software/systemd/%{name}-%{version}.tar.bz2
# Source0-md5:	36011aa8593862ca78e3e909f6143570
URL:		http://www.freedesktop.org/wiki/Software/systemd
#BuildRequires:	-
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	dbus-devel
BuildRequires:	gettext-devel
%if %{with gtk}
BuildRequires:	libnotify-devel >= 0.7.0
%endif
BuildRequires:	libtool
BuildRequires:	udev-devel >= 160
BuildRequires:	vala >= 0.11
#Requires(postun):	-
#Requires(pre,post):	-
#Requires(preun):	-
#Requires:	-
#Provides:	-
#Provides:	group(foo)
#Provides:	user(foo)
#Obsoletes:	-
#Conflicts:	-
#BuildArch:	noarch
#ExclusiveArch:	%{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
systemd is a system and service manager for Linux, compatible with 
SysV and LSB init scripts. systemd provides aggressive parallelization
capabilities, uses socket and D-Bus activation for starting services,
offers on-demand starting of daemons, keeps track of processes using
Linux cgroups, supports snapshotting and restoring of the system
state, maintains mount and automount points and implements an
elaborate transactional dependency-based service control logic. It can
work as a drop-in replacement for sysvinit. 

%description -l pl.UTF-8
systemd jest zarządcą systemu i usług dla Linuksa, kompatybilny ze
skryptami SysV i LSB. systemd udostępnia rozbudowane zdolności
paralelizacji, do uruchamiania usług używa socketów oraz D-Busa,
oferuje uruchamianie usług na życzenie, monitoruje procesy używając
linuksowych cgroups, wspomaga zapisywanie (snapshot) i odczytywanie
(restore) stanu systemu, zarządza (auto)mount pointami oraz
implementuje starannie opracowaną transakcjonalną, bazującą na
zależnościach logikę kontroli usług. Może pracować jako zastepca dla
sysvinit.

%prep
%setup -q

%build
%{__gettextize}
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__automake}
%configure \
	--with-distro="PLD Linux" \
	--%{?with_gtk:en}%{!?with_gtk:dis}able-gtk
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS CREDITS ChangeLog NEWS README THANKS TODO
