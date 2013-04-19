# TODO:
# - merge rpm macros provided by systemd with ours
#
# Conditional build:
%bcond_without	audit		# without audit support
%bcond_without	cryptsetup	# without cryptsetup support
%bcond_without	microhttpd	# microhttpd support
%bcond_without	pam		# PAM authentication support
%bcond_without	qrencode	# QRencode support
%bcond_without	selinux		# without SELinux support
%bcond_without	tcpd		# libwrap (tcp_wrappers) support
%bcond_with	tests		# "make check" (requires systemd already installed)

Summary:	A System and Service Manager
Summary(pl.UTF-8):	systemd - zarządca systemu i usług dla Linuksa
Name:		systemd
# Verify ChangeLog and NEWS when updating (since there are incompatible/breaking changes very often)
Version:	202
Release:	1
Epoch:		1
License:	GPL v2+ (udev), LGPL v2.1+ (the rest)
Group:		Base
Source0:	http://www.freedesktop.org/software/systemd/%{name}-%{version}.tar.xz
# Source0-md5:	3136c6912d3ee1f6d4deb16234783731
Source1:	%{name}-sysv-convert
Source2:	%{name}_booted.c
Source3:	network.service
Source4:	var-lock.mount
Source5:	var-run.mount
Source10:	pld-storage-init-late.service
Source11:	pld-storage-init.service
Source12:	pld-wait-storage.service
Source13:	pld-storage-init.sh
Source14:	pld-clean-tmp.service
Source15:	pld-clean-tmp.sh
Source16:	pld-rc-inetd-generator.sh
Source17:	rc-inetd.service
Source18:	default.preset
Source19:	prefdm.service
# rules
Source101:	udev-alsa.rules
Source102:	udev.rules
Source103:	udev-links.conf
# scripts / helpers
Source110:	udev-net.helper
Source111:	start_udev
# misc
Source120:	udev.blacklist
Source121:	fbdev.blacklist
Patch0:		target-pld.patch
Patch1:		config-pld.patch
Patch2:		shut-sysv-up.patch
Patch3:		pld-sysv-network.patch
Patch4:		tmpfiles-not-fatal.patch
Patch6:		udev-so.patch
Patch8:		udev-ploop-rules.patch
Patch9:		udevadm-in-sbin.patch
Patch10:	net-rename-revert.patch
Patch11:	nss-in-rootlib.patch
Patch12:	proc-hidepid.patch
Patch13:	nss-myhostname-link.patch
URL:		http://www.freedesktop.org/wiki/Software/systemd
BuildRequires:	acl-devel
BuildRequires:	attr-devel
%{?with_audit:BuildRequires:	audit-libs-devel}
BuildRequires:	autoconf >= 2.64
BuildRequires:	automake >= 1:1.11
BuildRequires:	binutils >= 3:2.22.52.0.1-2
%{?with_cryptsetup:BuildRequires:	cryptsetup-devel >= 1.4.3}
BuildRequires:	dbus-devel >= 1.3.2
BuildRequires:	docbook-style-xsl
BuildRequires:	glib2-devel >= 1:2.22.0
BuildRequires:	glibc-misc
BuildRequires:	gobject-introspection-devel >= 1.31.1
BuildRequires:	gperf
BuildRequires:	gtk-doc >= 1.18
BuildRequires:	intltool >= 0.40.0
BuildRequires:	kmod-devel >= 5
BuildRequires:	libblkid-devel >= 2.20
BuildRequires:	libcap-devel
BuildRequires:	libgcrypt-devel >= 1.4.5
%{?with_microhttpd:BuildRequires:	libmicrohttpd-devel >= 0.9.5}
%{?with_selinux:BuildRequires:	libselinux-devel >= 2.1.9}
BuildRequires:	libtool >= 2:2.2
%{?with_tcpd:BuildRequires:	libwrap-devel}
BuildRequires:	libxslt-progs
BuildRequires:	m4
%{?with_pam:BuildRequires:	pam-devel}
BuildRequires:	pkgconfig >= 0.9.0
BuildRequires:	python-devel
BuildRequires:	python-modules
%{?with_qrencode:BuildRequires:	qrencode-devel}
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.628
BuildRequires:	sed >= 4.0
%{?with_tests:BuildRequires:	systemd}
BuildRequires:	usbutils >= 0.82
BuildRequires:	xz-devel
BuildRequires:	zlib-devel
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}
Requires:	%{name}-units = %{epoch}:%{version}-%{release}
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires:	/etc/os-release
Requires:	SysVinit-tools
Requires:	agetty
%{?with_cryptsetup:Requires:	cryptsetup >= 1.4.3}
Requires:	dbus >= 1.4.16-6
Requires:	filesystem >= 4.0-3
Requires:	libutempter
Requires:	rc-scripts >= 0.4.5.3-7
Requires:	setup >= 2.8.0-2
Requires:	udev-core = %{epoch}:%{version}-%{release}
Requires:	udev-libs = %{epoch}:%{version}-%{release}
Requires:	virtual(module-tools)
Suggests:	ConsoleKit
Suggests:	fsck >= 2.20
Suggests:	kmod >= 5
Suggests:	service(klogd)
Suggests:	service(syslog)
Provides:	group(systemd-journal)
Provides:	group(systemd-journal-gateway)
Provides:	udev-acl = %{epoch}:%{version}-%{release}
Provides:	user(systemd-journal-gateway)
Obsoletes:	systemd-no-compat-tmpfiles
Obsoletes:	udev-systemd
# systemd takes care of that and causes problems
Conflicts:	binfmt-detector
# sytemd wants pam with pam_systemd.so in system-auth...
Conflicts:	pam < 1:1.1.5-5
# ...and sudo hates it
Conflicts:	sudo < 1:1.7.8p2-4
# for prefdm script
Conflicts:	xinitrc-ng < 1.0
# systemd scripts use options not present in older versions
Conflicts:	kpartx < 0.4.9-7
Conflicts:	multipath-tools < 0.4.9-7
# no tmpfs on /media, use /run/media/$USER for mounting
Conflicts:	udisks2 < 1.92.0
# packages that have dirs under /var/run and/or /var/lock must provide tmpfiles configs
Conflicts:	ConsoleKit-dirs < 0.4.5-7
Conflicts:	NetworkManager < 2:0.9.2.0-3
Conflicts:	Zope < 2.11.8-2
Conflicts:	amavisd-new < 1:2.7.0-1
Conflicts:	apache-base < 2.2.21-4
Conflicts:	apache-mod_bw < 0.92-3
Conflicts:	apache-mod_fastcgi < 2.4.6-6
Conflicts:	apache1-base < 1.3.42-5
Conflicts:	apache1-mod_fastcgi < 2.4.6-2
Conflicts:	asterisk < 10.0.1-2
Conflicts:	autossh-init < 1.4b-3
Conflicts:	balance < 3.54-2
Conflicts:	bind < 7:9.8.1.P1-4
Conflicts:	bopm < 3.1.3-4
Conflicts:	callweaver < 1.2.1-9
Conflicts:	cassandra-bin < 0.8.9-2
Conflicts:	clamav < 0.97.3-3
Conflicts:	cups < 1:1.5.0-10
Conflicts:	dovecot < 1:2.0.16-3
Conflicts:	dspam < 3.9.0-6
Conflicts:	fail2ban < 0.8.4-4
Conflicts:	gammu-smsd < 1:1.31.0-3
# Break gdm2.20 installs
#Conflicts:	gdm < 2:3.2.1.1-9
Conflicts:	greylistd < 0.8.8-2
Conflicts:	inn < 2.4.6-7
Conflicts:	ipsec-tools < 0.8.0-3
Conflicts:	jabber-common < 0-9
Conflicts:	laptop-mode-tools < 1.58-2
Conflicts:	libgpod < 0.8.0-6
Conflicts:	libvirt-utils < 0.9.9-4
Conflicts:	lighttpd < 1.4.30-5
Conflicts:	lirc < 0.9.0-20
Conflicts:	mailman < 5:2.1.14-4
Conflicts:	memcached < 1.4.11-2
Conflicts:	mpd < 0.16.5-4
Conflicts:	mrtg < 2.17.0-3
Conflicts:	munin-common < 1.4.5-5
Conflicts:	nagios-nrpe < 2.13-2
Conflicts:	ndisc6-rdnssd < 1.0.1-3
Conflicts:	nscd < 6:2.14.1-5
Conflicts:	nss_ldapd-nslcd < 0.8.4-2
Conflicts:	openct < 0.6.20-3
Conflicts:	openl2tp < 1.8-3
Conflicts:	openldap-overlay-nssov < 2.4.28-4
Conflicts:	openldap-servers < 2.4.28-4
Conflicts:	openvpn < 2.2.2-2
Conflicts:	pam-pam_mount < 2.12-3
Conflicts:	pam-pam_ssh < 1.97-2
Conflicts:	pcsc-lite < 1.8.1-2
Conflicts:	php-dirs < 1.2-3
Conflicts:	policyd < 2.0.10-3
Conflicts:	pound < 2.6-2
Conflicts:	pptp < 1.7.2-3
Conflicts:	proftpd-common < 2:1.3.4a-2
Conflicts:	pulseaudio-server < 1.1-2
Conflicts:	quagga < 0.99.20-3
Conflicts:	radvd < 1.8.5-2
Conflicts:	red5 < 0.9.0-2
Conflicts:	redis-server < 2.4.2-4
Conflicts:	smokeping < 2.4.2-10
Conflicts:	smtp-gated < 1.4.17-2
Conflicts:	socat < 1.7.2.0-2
Conflicts:	speech-dispatcher < 0.7.1-2
Conflicts:	sphinx < 2.0.3-4
Conflicts:	splashutils < 1.5.4.3-3
Conflicts:	stunnel < 4.50-2
Conflicts:	tenshi < 0.12-2
Conflicts:	tor < 0.2.2.35-2
Conflicts:	ucarp < 1.5.2-3
Conflicts:	udisks < 1.0.4-3
Conflicts:	util-vserver < 0.30.216-1.pre3002.3
Conflicts:	vpnc < 0.5.3-2
Conflicts:	web2ldap < 1.1.0rc1-2
Conflicts:	wesnoth-server < 1:1.10-2
Conflicts:	wpa_supplicant < 0.7.3-10
Conflicts:	xl2tpd < 1.3.0-2
# end of tmpfiles conflicts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sbindir	/sbin
%define		_libexecdir	%{_prefix}/lib

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
zależnościach logikę kontroli usług. Może pracować jako zastępca dla
sysvinit.

%package init
Summary:	systemd /sbin/init and LSB/SysV compatibility symlinks
Summary(pl.UTF-8):	/sbin/init z systemd i dowiązania dla kompatybilności z LSB/SysV
Group:		Base
Requires:	systemd
Provides:	readahead = 1:1.5.7-3
Provides:	virtual(init-daemon)
Obsoletes:	SysVinit
Obsoletes:	readahead < 1:1.5.7-3
Obsoletes:	virtual(init-daemon)
Conflicts:	upstart

%description init
Install this package when you are ready to final switch to systemd.

%description init -l pl.UTF-8
Ten pakiet należy zainstalować po przygotowaniu się do ostatecznego
przejścia na systemd.

%package units
Summary:	Configuration files, directories and installation tool for systemd
Summary(pl.UTF-8):	Pliki konfiguracyjne, katalogi i narzędzie instalacyjne dla systemd
Group:		Base
Requires(post):	coreutils
Requires(post):	/bin/awk

%description units
Basic configuration files, directories and installation tool for the
systemd system and service manager.

This is common config, use %{_sysconfdir}/systemd/system to override.

%description units -l pl.UTF-8
Podstawowe pliki konfiguracyjne, katalogi i narzędzie instalacyjne dla
zarządcy systemu i usług systemd.

Ten pakiet zawiera ogólną konfigurację, ustawienia można nadpisać
poprzez katalog %{_sysconfdir}/systemd/system.

%package inetd
Summary:	Native inet service support for systemd via socket activation
Summary(pl.UTF-8):	Natywna obsługa usług inet dla systemd
Group:		Base
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	rc-inetd
Provides:	inetdaemon
Obsoletes:	inetd
Obsoletes:	inetdaemon
Obsoletes:	rlinetd
Obsoletes:	xinetd

%description inetd
Native inet service support for systemd via socket activation.

This package contains inet service generator that provides the
functionality of rc-inetd service and replaces a separate inet daemon
with systemd socket activation feature.

%description inetd -l pl.UTF-8
Natywna obsługa usług inet dla systemd.

Ten pakiet zawiera generator usług inet udostępniający funkcjonalność
serwisu rc-inetd i zastępujący osobny demon inet przez systemd i
aktywację usług przez gniazda.

%package analyze
Summary:	Tool for processing systemd profiling information
Summary(pl.UTF-8):	Narzędzie do przetwarzania informacji profilujących systemd
Group:		Base
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	python-dbus
Requires:	python-modules
Suggests:	python-pycairo
Conflicts:	systemd < 44-3

%description analyze
'systemd-analyze blame' lists which systemd unit needed how much time
to finish initialization at boot. 'systemd-analyze plot' renders an
SVG visualizing the parallel start of units at boot.

%description analyze -l pl.UTF-8
'systemd-analyze blame' wypisuje, ile czasu wymagały poszczególne
jednostki systemd na zakończenie podczas rozruchu systemu.
'systemd-analyze plot' tworzy wykres SVG wizualizujący równoległy
start jednostek podczas rozruchu.

%package libs
Summary:	Shared systemd libraries
Summary(pl.UTF-8):	Biblioteki współdzielone systemd
Group:		Libraries
Requires:	libgcrypt >= 1.4.5
%{?with_selinux:Requires:	libselinux >= 2.1.9}
Obsoletes:	nss_myhostname

%description libs
Shared systemd libraries.

%description libs -l pl.UTF-8
Biblioteki współdzielone systemd.

%package devel
Summary:	Header files for systemd libraries
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotek systemd
Group:		Development/Libraries
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}

%description devel
Header files for systemd libraries.

%description devel -l pl.UTF-8
Pliki nagłówkowe bibliotek systemd.

%package static
Summary:	Static systemd libraries
Summary(pl.UTF-8):	Statyczne biblioteki systemd
Group:		Development/Libraries
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}

%description static
Static systemd libraries.

%description static -l pl.UTF-8
Statyczne biblioteki systemd.

%package -n bash-completion-systemd
Summary:	bash-completion for systemd
Summary(pl.UTF-8):	Bashowe dopełnianie składni dla systemd
Group:		Applications/Shells
Requires:	%{name} = %{epoch}:%{version}
Requires:	bash-completion >= 2.0

%description -n bash-completion-systemd
bash-completion for systemd.

%description -n bash-completion-systemd -l pl.UTF-8
Bashowe dopełnianie składni dla systemd.

%package -n udev
Summary:	Device manager for the Linux 2.6 kernel series
Summary(pl.UTF-8):	Zarządca urządzeń dla Linuksa 2.6
Group:		Base
Requires:	udev-core = %{epoch}:%{version}-%{release}
Provides:	dev = 3.5.0
Obsoletes:	dev
Obsoletes:	hotplug
Obsoletes:	hotplug-input
Obsoletes:	hotplug-net
Obsoletes:	hotplug-pci
Obsoletes:	udev-dev
Obsoletes:	udev-extras < 20090628
Obsoletes:	udev-tools

%description -n udev
udev is the device manager for the Linux 2.6 kernel series. Its
primary function is managing device nodes in /dev. It is the successor
of devfs and hotplug.

%description -n udev -l pl.UTF-8
udev jest zarządcą urządzeń dla Linuksa 2.6. Jego główną funkcją jest
zarządzanie węzłami urządzeń w katalogu /dev. Jest następcą devfs i
hotpluga.

%package -n udev-core
Summary:	A userspace implementation of devfs - core part of udev
Summary(pl.UTF-8):	Implementacja devfs w przestrzeni użytkownika - główna część udev
Group:		Base
Requires:	coreutils
Requires:	filesystem >= 3.0-45
Requires:	kmod-libs >= 5
Requires:	libblkid >= 2.20
%{?with_selinux:Requires:	libselinux >= 2.1.9}
Requires:	setup >= 2.6.1-1
Requires:	udev-libs = %{epoch}:%{version}-%{release}
Requires:	uname(release) >= 2.6.32
Obsoletes:	udev-compat
Obsoletes:	udev-initrd < %{epoch}:%{version}-%{release}}
Conflicts:	rc-scripts < 0.4.5.3-1
Conflicts:	systemd-units < 1:183
Conflicts:	udev < 1:118-1
Conflicts:	geninitrd < 12639

%description -n udev-core
A userspace implementation of devfs - core part of udev.

%description -n udev-core -l pl.UTF-8
Implementacja devfs w przestrzeni użytkownika - główna część udev.

%package -n udev-libs
Summary:	Shared library to access udev device information
Summary(pl.UTF-8):	Biblioteka współdzielona do dostępu do informacji o urządzeniach udev
Group:		Libraries

%description -n udev-libs
Shared libudev library to access udev device information.

%description -n udev-libs -l pl.UTF-8
Biblioteka współdzielona libudev służąca do dostępu do informacji o
urządzeniach udev.

%package -n udev-devel
Summary:	Header file for libudev library
Summary(pl.UTF-8):	Plik nagłówkowy biblioteki libudev
Group:		Development/Libraries
Requires:	udev-libs = %{epoch}:%{version}-%{release}

%description -n udev-devel
Header file for libudev library.

%description -n udev-devel -l pl.UTF-8
Plik nagłówkowy biblioteki libudev.

%package -n udev-static
Summary:	Static libudev library
Summary(pl.UTF-8):	Biblioteka statyczna libudev
Group:		Development/Libraries
Requires:	udev-devel = %{epoch}:%{version}-%{release}

%description -n udev-static
Static libudev library.

%description -n udev-static -l pl.UTF-8
Biblioteka statyczna libudev.

%package -n udev-apidocs
Summary:	libudev API documentation
Summary(pl.UTF-8):	Dokumentacja API libudev
Group:		Documentation
Requires:	gtk-doc-common

%description -n udev-apidocs
libudev API documentation.

%description -n udev-apidocs -l pl.UTF-8
Dokumentacja API libudev.

%package -n udev-glib
Summary:	Shared libgudev library - GObject bindings for libudev
Summary(pl.UTF-8):	Biblioteka współdzielona libgudev - wiązania GObject do libudev
Group:		Libraries
Requires:	glib2 >= 1:2.22.0
Requires:	udev-libs = %{epoch}:%{version}-%{release}

%description -n udev-glib
Shared libgudev library - GObject bindings for libudev.

%description -n udev-glib -l pl.UTF-8
Biblioteka współdzielona libgudev - wiązania GObject do libudev.

%package -n udev-glib-devel
Summary:	Header file for libgudev library
Summary(pl.UTF-8):	Plik nagłówkowy biblioteki libgudev
Group:		Development/Libraries
Requires:	glib2-devel >= 1:2.22.0
Requires:	udev-devel = %{epoch}:%{version}-%{release}
Requires:	udev-glib = %{epoch}:%{version}-%{release}

%description -n udev-glib-devel
Header file for libgudev library.

%description -n udev-glib-devel -l pl.UTF-8
Plik nagłówkowy biblioteki libgudev.

%package -n udev-glib-static
Summary:	Static libgudev library
Summary(pl.UTF-8):	Biblioteka statyczna libgudev
Group:		Development/Libraries
Requires:	udev-glib-devel = %{epoch}:%{version}-%{release}

%description -n udev-glib-static
Static libgudev library.

%description -n udev-glib-static -l pl.UTF-8
Biblioteka statyczna libgudev.

%package -n udev-glib-apidocs
Summary:	libgudev API documentation
Summary(pl.UTF-8):	Dokumentacja API libgudev
Group:		Documentation
Requires:	gtk-doc-common

%description -n udev-glib-apidocs
libgudev API documentation.

%description -n udev-glib-apidocs -l pl.UTF-8
Dokumentacja API libgudev.

%package -n bash-completion-udev
Summary:	bash-completion for udev
Summary(pl.UTF-8):	Bashowe dopełnianie składni dla udev
Group:		Applications/Shells
Requires:	bash-completion >= 2.0
Requires:	udev = %{epoch}:%{version}

%description -n bash-completion-udev
bash-completion for udev.

%description -n bash-completion-udev -l pl.UTF-8
Bashowe dopełnianie składni dla udev.


%package -n python-systemd
Summary:	Systemd Python bindings
Summary(pl.UTF-8):	Wiązania do Systemd dla Pythona
Group:		Development/Languages/Python
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}
Requires:	python

%description -n python-systemd
Systemd Python bindings.

%description -n python-systemd -l pl.UTF-8
Wiązania do Systemd dla Pythona.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
#patch2 -p1
%patch3 -p1
%patch4 -p1
%patch6 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
cp -p %{SOURCE2} src/systemd_booted.c

%build
%{__gtkdocize}
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	QUOTAON=/sbin/quotaon \
	QUOTACHECK=/sbin/quotacheck \
	SETCAP=/sbin/setcap \
	KILL=/bin/kill \
	%{?debug:--enable-debug} \
	%{__enable_disable audit} \
	%{__enable_disable cryptsetup libcryptsetup} \
	%{__enable_disable pam} \
	%{__enable_disable selinux} \
	%{__enable_disable tcpd tcpwrap} \
	%{__enable_disable microhttpd} \
	%{__enable_disable qrencode} \
	--disable-silent-rules \
	--enable-chkconfig \
	--enable-gtk-doc \
	--enable-introspection \
	--enable-split-usr \
	--enable-static \
	--with-html-dir=%{_gtkdocdir} \
	--with-kbd-loadkeys=/usr/bin/loadkeys \
	--with-kbd-setfont=/bin/setfont \
	--with-sysvinit-path=/etc/rc.d/init.d \
	--with-sysvrcnd-path=/etc/rc.d \
	--with-rc-local-script-path-start=/etc/rc.d/rc.local \
	--with-rc-local-script-path-stop=/sbin/halt.local \
	--with-rootprefix="" \
	--with-rootlibdir=/%{_lib}

%{__make} -j1
./libtool --mode=link --tag=CC %{__cc} %{rpmcppflags} %{rpmcflags} -o systemd_booted %{rpmldflags} src/systemd_booted.c -L. -lsystemd-daemon

%{?with_tests:%{__make} check}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/var/lib/%{name}/coredump \
	$RPM_BUILD_ROOT{%{_sysconfdir}/{modprobe.d,systemd/system-preset},%{_sbindir}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

./libtool --mode=install install -p -m755 systemd_booted $RPM_BUILD_ROOT/bin/systemd_booted

# compatibility symlinks to udevd binary
mv $RPM_BUILD_ROOT/lib/{systemd/systemd-,udev/}udevd
ln -s /lib/udev/udevd $RPM_BUILD_ROOT/lib/systemd/systemd-udevd
ln -s /lib/udev/udevd $RPM_BUILD_ROOT%{_sbindir}/udevd

# compat symlinks for "/ merged into /usr" programs
mv $RPM_BUILD_ROOT/{,s}bin/udevadm
ln -s %{_sbindir}/udevadm $RPM_BUILD_ROOT/bin
ln -s /lib/udev $RPM_BUILD_ROOT/usr/lib/

# install custom udev rules from pld package
cp -a %{SOURCE101} $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d/40-alsa-restore.rules
cp -a %{SOURCE102} $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d/70-udev-pld.rules

# disable this abomination
# http://www.freedesktop.org/wiki/Software/systemd/PredictableNetworkInterfaceNames
ln -s /dev/null $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d/80-net-name-slot.rules

# install udev configs
cp -a %{SOURCE103} $RPM_BUILD_ROOT%{_sysconfdir}/udev/links.conf

# install udev executables (scripts, helpers, etc.)
install -p %{SOURCE110} $RPM_BUILD_ROOT/lib/udev/net_helper
install -p %{SOURCE111} $RPM_BUILD_ROOT%{_sbindir}/start_udev

# install misc udev stuff
cp -a %{SOURCE120} $RPM_BUILD_ROOT%{_sysconfdir}/modprobe.d/udev_blacklist.conf
cp -a %{SOURCE121} $RPM_BUILD_ROOT%{_sysconfdir}/modprobe.d/fbdev-blacklist.conf

mv $RPM_BUILD_ROOT%{_mandir}/man8/{systemd-,}udevd.8
echo ".so man8/udevd.8" >$RPM_BUILD_ROOT%{_mandir}/man8/systemd-udevd.8

# Main binary has been moved, but we don't want to break existing installs
ln -s ../lib/systemd/systemd $RPM_BUILD_ROOT/bin/systemd

# Create SysV compatibility symlinks. systemctl/systemd are smart
# enough to detect the way they were called
install -d $RPM_BUILD_ROOT/sbin
ln -s ../lib/systemd/systemd $RPM_BUILD_ROOT/sbin/init
ln -s ../bin/systemctl $RPM_BUILD_ROOT/sbin/halt
ln -s ../bin/systemctl $RPM_BUILD_ROOT/sbin/poweroff
ln -s ../bin/systemctl $RPM_BUILD_ROOT/sbin/reboot
ln -s ../bin/systemctl $RPM_BUILD_ROOT/sbin/runlevel
ln -s ../bin/systemctl $RPM_BUILD_ROOT/sbin/shutdown
ln -s ../bin/systemctl $RPM_BUILD_ROOT/sbin/telinit

ln -s ../modules $RPM_BUILD_ROOT%{_sysconfdir}/modules-load.d/modules.conf

# disable redundant SYSV services
ln -s /dev/null $RPM_BUILD_ROOT%{systemdunitdir}/allowlogin.service
ln -s /dev/null $RPM_BUILD_ROOT%{systemdunitdir}/console.service
ln -s /dev/null $RPM_BUILD_ROOT%{systemdunitdir}/cpusets.service
ln -s /dev/null $RPM_BUILD_ROOT%{systemdunitdir}/killall.service
ln -s /dev/null $RPM_BUILD_ROOT%{systemdunitdir}/netfs.service
ln -s /dev/null $RPM_BUILD_ROOT%{systemdunitdir}/random.service

# add static (non-NetworkManager) networking
cp -p %{SOURCE3} $RPM_BUILD_ROOT%{systemdunitdir}/network.service

# restore bind-mounts /var/run -> run and /var/lock -> /run/lock
# we don't have those directories symlinked
cp -p %{SOURCE4} $RPM_BUILD_ROOT%{systemdunitdir}/var-lock.mount
cp -p %{SOURCE5} $RPM_BUILD_ROOT%{systemdunitdir}/var-run.mount
ln -s ../var-lock.mount $RPM_BUILD_ROOT%{systemdunitdir}/local-fs.target.wants
ln -s ../var-run.mount $RPM_BUILD_ROOT%{systemdunitdir}/local-fs.target.wants

# and remove tmp on tmpfs mount
%{__rm} $RPM_BUILD_ROOT%{systemdunitdir}/tmp.mount
%{__rm} $RPM_BUILD_ROOT%{systemdunitdir}/local-fs.target.wants/tmp.mount

# Install and enable storage subsystems support services (RAID, LVM, etc.)
cp -p %{SOURCE10} $RPM_BUILD_ROOT%{systemdunitdir}/pld-storage-init-late.service
cp -p %{SOURCE11} $RPM_BUILD_ROOT%{systemdunitdir}/pld-storage-init.service
cp -p %{SOURCE12} $RPM_BUILD_ROOT%{systemdunitdir}/pld-wait-storage.service
cp -p %{SOURCE14} $RPM_BUILD_ROOT%{systemdunitdir}/pld-clean-tmp.service
install -p %{SOURCE13} $RPM_BUILD_ROOT/lib/systemd/pld-storage-init
install -p %{SOURCE15} $RPM_BUILD_ROOT/lib/systemd/pld-clean-tmp

ln -s ../pld-storage-init-late.service $RPM_BUILD_ROOT%{systemdunitdir}/local-fs.target.wants
ln -s ../pld-storage-init.service $RPM_BUILD_ROOT%{systemdunitdir}/local-fs.target.wants
ln -s ../pld-clean-tmp.service $RPM_BUILD_ROOT%{systemdunitdir}/local-fs.target.wants

# Install rc-inetd replacement
cp -p %{SOURCE16} $RPM_BUILD_ROOT/lib/systemd/system-generators/pld-rc-inetd-generator
cp -p %{SOURCE17} $RPM_BUILD_ROOT%{systemdunitdir}/rc-inetd.service

cp -p %{SOURCE18} $RPM_BUILD_ROOT%{_sysconfdir}/systemd/system-preset/default.preset

cp -p %{SOURCE19} $RPM_BUILD_ROOT%{systemdunitdir}/prefdm.service

# handled by rc-local sysv service, no need for generator
%{__rm} $RPM_BUILD_ROOT/lib/systemd/system-generators/systemd-rc-local-generator

# provided by rc-scripts
%{__rm} $RPM_BUILD_ROOT/lib/systemd/system/rc-local.service

# Make sure these directories are properly owned:
#	- halt,kexec,poweroff,reboot: generic ones used by ConsoleKit-systemd,
#	- syslog _might_ be used by some syslog implementation (none for now),
#	- isn't dbus populated by dbus-systemd only (so to be moved there)?
install -d $RPM_BUILD_ROOT%{systemdunitdir}/{basic,dbus,halt,initrd,kexec,poweroff,reboot,syslog}.target.wants

# Create new-style configuration files so that we can ghost-own them
touch $RPM_BUILD_ROOT%{_sysconfdir}/{hostname,locale.conf,machine-id,machine-info,timezone,vconsole.conf}

# Install SysV conversion tool for systemd
install -p %{SOURCE1} $RPM_BUILD_ROOT%{_bindir}

install -d $RPM_BUILD_ROOT/var/log
:> $RPM_BUILD_ROOT/var/log/btmp
:> $RPM_BUILD_ROOT/var/log/wtmp

%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}
%{__rm} $RPM_BUILD_ROOT/%{_lib}/security/pam_systemd.la
%{__rm} $RPM_BUILD_ROOT/%{_lib}/libnss_myhostname.la
%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la
%{__rm} $RPM_BUILD_ROOT%{py_sitedir}/systemd/*.la
%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 288 systemd-journal
%groupadd -g 287 systemd-journal-gateway
%useradd -u 287 -g 287 -d /var/log/journal -s /bin/false -c "Systemd Journal Gateway" systemd-journal-gateway

%post
# should we?
#setfacl -nm g:logs:rx,d:g:logs:rx /var/log/journal
/bin/systemd-machine-id-setup > /dev/null 2>&1 || :
/bin/systemctl daemon-reexec > /dev/null 2>&1 || :

%postun
if [ $1 -ge 1 ]; then
	/bin/systemctl try-restart systemd-logind.service >/dev/null 2>&1 || :
fi
if [ "$1" = "0" ]; then
	%userremove systemd-journal-gateway
	%groupremove systemd-journal-gateway
	%groupremove systemd-journal
fi

%post   libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%post units
if [ $1 -eq 1 ]; then
	# Try to read default runlevel from the old inittab if it exists
	runlevel=$(/bin/awk -F ':' '$3 == "initdefault" && $1 !~ "^#" { print $2 }' /etc/inittab 2> /dev/null)
	if [ -z "$runlevel" ] ; then
		target="%{systemdunitdir}/graphical.target"
	else
		target="%{systemdunitdir}/runlevel$runlevel.target"
	fi

	# And symlink what we found to the new-style default.target
	ln -s "$target" %{_sysconfdir}/systemd/system/default.target >/dev/null 2>&1 || :

	# Setup hostname
	[ -f /etc/sysconfig/network ] && . /etc/sysconfig/network
	if [ -n "$HOSTNAME" -a "$HOSTNAME" != "pldmachine" ]; then
		[ -f /etc/hostname ] && mv -f /etc/hostname /etc/hostname.rpmsave
		echo $HOSTNAME > /etc/hostname
		chmod 644 /etc/hostname
	fi

	# Enable the services we install by default.
	/bin/systemctl enable \
		getty@.service \
		network.service \
		remote-fs.target \
		systemd-readahead-replay.service \
		systemd-readahead-collect.service \
		systemd-udev-settle.service >/dev/null 2>&1 || :
fi

%preun units
if [ $1 -eq 0 ] ; then
	/bin/systemctl disable \
		getty@.service \
		network.service \
		remote-fs.target \
		systemd-readahead-replay.service \
		systemd-readahead-collect.service \
		systemd-udev-settle.service >/dev/null 2>&1 || :

	%{__rm} -f %{_sysconfdir}/systemd/system/default.target >/dev/null 2>&1 || :
fi

%postun units
if [ $1 -ge 1 ]; then
	/bin/systemctl daemon-reload > /dev/null 2>&1 || :
fi

%triggerpostun units -- systemd-units < 43-7
# Remove design fialures
%{__rm} -f %{_sysconfdir}/systemd/system/network.target.wants/ifcfg@*.service >/dev/null 2>&1 || :
%{__rm} -f %{_sysconfdir}/systemd/system/network.target.wants/network-post.service >/dev/null 2>&1 || :
%{__rm} -f %{_sysconfdir}/systemd/system/multi-user.target.wants/network-post.service >/dev/null 2>&1 || :
/bin/systemctl reenable network.service >/dev/null 2>&1 || :

%triggerpostun units -- systemd-units < 1:183
/bin/systemctl --quiet enable systemd-udev-settle.service >/dev/null 2>&1 || :
%{__rm} -f /etc/systemd/system/basic.target.wants/udev-settle.service >/dev/null 2>&1 || :
# preserve renamed configs
if [ -f /etc/systemd/systemd-journald.conf.rpmsave ]; then
	%{__mv} /etc/systemd/journald.conf{,.rpmnew}
	%{__mv} -f /etc/systemd/systemd-journald.conf.rpmsave /etc/systemd/journald.conf
fi
if [ -f /etc/systemd/systemd-logind.conf.rpmsave ]; then
	%{__mv} /etc/systemd/logind.conf{,.rpmnew}
	%{__mv} -f /etc/systemd/systemd-logind.conf.rpmsave /etc/systemd/logind.conf
fi

%triggerpostun units -- systemd-units < 1:187-3
if [ -f /etc/sysconfig/rpm ]; then
	. /etc/sysconfig/rpm
	if [ ${RPM_ENABLE_SYSTEMD_SERVICE:-yes} = no ]; then
		echo "disable *" >>%{_sysconfdir}/systemd/system-preset/default.preset
	fi
fi

%post inetd
%systemd_reload
# Do not change it to restart, we only want to start new services here
%systemd_service_start sockets.target

%postun inetd
%systemd_reload

%triggerpostun -n udev-core -- dev
if [ "$2" = 0 ]; then
	# need to kill and restart udevd as after obsoleting dev package the
	# /dev tree will remain empty. umask is needed as otherwise udev will
	# create devices with strange permissions (udev bug probably)
	umask 000
	/sbin/start_udev || exit 0
fi

%triggerpostun -n udev-core -- udev < 108
%{__sed} -i -e 's#IMPORT{program}="/sbin/#IMPORT{program}="#g' /etc/udev/rules.d/*.rules
%if "%{_lib}" != "lib"
%{__sed} -i -e 's#/%{_lib}/udev/#/lib/udev/#g' /etc/udev/rules.d/*.rules
%endif

%triggerpostun -n udev-core -- udev < 165
/sbin/udevadm info --convert-db

%post -n udev-core
if [ $1 -gt 1 ]; then
	if [ ! -x /bin/systemd_booted ] || ! /bin/systemd_booted; then
		if grep -qs devtmpfs /proc/mounts && [ -n "$(pidof udevd)" ]; then
			/sbin/udevadm control --exit
			/lib/udev/udevd --daemon
		fi
	else
		SYSTEMD_LOG_LEVEL=warning SYSTEMD_LOG_TARGET=syslog \
		/bin/systemctl --quiet try-restart systemd-udevd.service || :
	fi
fi

%postun -n udev-core
if [ -x /bin/systemd_booted ] && /bin/systemd_booted; then
	SYSTEMD_LOG_LEVEL=warning SYSTEMD_LOG_TARGET=syslog \
	/bin/systemctl --quiet daemon-reload || :
fi

%post	-n udev-libs -p /sbin/ldconfig
%postun	-n udev-libs -p /sbin/ldconfig

%post	-n udev-glib -p /sbin/ldconfig
%postun	-n udev-glib -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc DISTRO_PORTING README TODO
/etc/dbus-1/system.d/org.freedesktop.hostname1.conf
/etc/dbus-1/system.d/org.freedesktop.locale1.conf
/etc/dbus-1/system.d/org.freedesktop.login1.conf
/etc/dbus-1/system.d/org.freedesktop.systemd1.conf
/etc/dbus-1/system.d/org.freedesktop.timedate1.conf
%ghost %config(noreplace) %{_sysconfdir}/machine-id
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/hostname
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/locale.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/machine-info
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/timezone
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/vconsole.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/systemd/bootchart.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/systemd/journald.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/systemd/logind.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/systemd/system.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/systemd/user.conf
%dir %{_sysconfdir}/systemd/user
%dir %{_sysconfdir}/systemd/system/*.target.wants
%config(noreplace,missingok) %verify(not md5 mtime size) %{_sysconfdir}/systemd/system/*.target.wants/*.service
%config(noreplace,missingok) %verify(not md5 mtime size) %{_sysconfdir}/systemd/system/*.target.wants/*.target
/etc/xdg/systemd
%attr(755,root,root) /bin/journalctl
%attr(755,root,root) /bin/loginctl
%attr(755,root,root) /bin/systemd
%attr(755,root,root) /bin/systemd-ask-password
%attr(755,root,root) /bin/systemd-inhibit
%attr(755,root,root) /bin/systemd-machine-id-setup
%attr(755,root,root) /bin/systemd-notify
%attr(755,root,root) /bin/systemd-tty-ask-password-agent
%attr(755,root,root) %{_bindir}/bootctl
%attr(755,root,root) %{_bindir}/hostnamectl
%attr(755,root,root) %{_bindir}/kernel-install
%attr(755,root,root) %{_bindir}/localectl
%attr(755,root,root) %{_bindir}/systemd-cat
%attr(755,root,root) %{_bindir}/systemd-cgls
%attr(755,root,root) %{_bindir}/systemd-cgtop
%attr(755,root,root) %{_bindir}/systemd-coredumpctl
%attr(755,root,root) %{_bindir}/systemd-delta
%attr(755,root,root) %{_bindir}/systemd-detect-virt
%attr(755,root,root) %{_bindir}/systemd-nspawn
%attr(755,root,root) %{_bindir}/systemd-stdio-bridge
%attr(755,root,root) %{_bindir}/systemd-sysv-convert
%attr(755,root,root) %{_bindir}/timedatectl
%attr(755,root,root) /lib/systemd/pld-clean-tmp
%attr(755,root,root) /lib/systemd/pld-storage-init
%attr(755,root,root) /lib/systemd/systemd-ac-power
%attr(755,root,root) /lib/systemd/systemd-activate
%attr(755,root,root) /lib/systemd/systemd-binfmt
%attr(755,root,root) /lib/systemd/systemd-bootchart
%attr(755,root,root) /lib/systemd/systemd-cgroups-agent
%attr(755,root,root) /lib/systemd/systemd-coredump
%{?with_cryptsetup:%attr(755,root,root) /lib/systemd/systemd-cryptsetup}
%attr(755,root,root) /lib/systemd/systemd-fsck
%attr(755,root,root) /lib/systemd/systemd-hostnamed
%attr(755,root,root) /lib/systemd/systemd-initctl
%{?with_microhttpd:%attr(755,root,root) /lib/systemd/systemd-journal-gatewayd}
%attr(755,root,root) /lib/systemd/systemd-journald
%attr(755,root,root) /lib/systemd/systemd-localed
%attr(755,root,root) /lib/systemd/systemd-logind
%attr(755,root,root) /lib/systemd/systemd-modules-load
%attr(755,root,root) /lib/systemd/systemd-multi-seat-x
%attr(755,root,root) /lib/systemd/systemd-quotacheck
%attr(755,root,root) /lib/systemd/systemd-random-seed
%attr(755,root,root) /lib/systemd/systemd-readahead
%attr(755,root,root) /lib/systemd/systemd-remount-fs
%attr(755,root,root) /lib/systemd/systemd-reply-password
%attr(755,root,root) /lib/systemd/systemd-shutdown
%attr(755,root,root) /lib/systemd/systemd-shutdownd
%attr(755,root,root) /lib/systemd/systemd-sleep
%attr(755,root,root) /lib/systemd/systemd-sysctl
%attr(755,root,root) /lib/systemd/systemd-timedated
%attr(755,root,root) /lib/systemd/systemd-timestamp
%attr(755,root,root) /lib/systemd/systemd-udevd
%attr(755,root,root) /lib/systemd/systemd-update-utmp
%attr(755,root,root) /lib/systemd/systemd-user-sessions
%attr(755,root,root) /lib/systemd/systemd-vconsole-setup
%dir /lib/systemd/system-generators
%attr(755,root,root) /lib/systemd/systemd
%attr(755,root,root) /lib/systemd/system-generators/systemd-*-generator
/lib/udev/rules.d/70-uaccess.rules
/lib/udev/rules.d/71-seat.rules
/lib/udev/rules.d/73-seat-late.rules
/lib/udev/rules.d/99-systemd.rules
%dir %{_libexecdir}/systemd
%dir %{_libexecdir}/systemd/catalog
%{_libexecdir}/systemd/catalog/systemd.catalog
%{_libexecdir}/systemd/user
%dir %{_libexecdir}/systemd/user-generators
%{_libexecdir}/tmpfiles.d/legacy.conf
%{_libexecdir}/tmpfiles.d/systemd.conf
%{_libexecdir}/tmpfiles.d/tmp.conf
%{_libexecdir}/tmpfiles.d/x11.conf
%{_datadir}/dbus-1/interfaces/org.freedesktop.hostname1.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.locale1.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.systemd1.*.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.timedate1.xml
%{_datadir}/dbus-1/services/org.freedesktop.systemd1.service
%{_datadir}/dbus-1/system-services/org.freedesktop.hostname1.service
%{_datadir}/dbus-1/system-services/org.freedesktop.locale1.service
%{_datadir}/dbus-1/system-services/org.freedesktop.login1.service
%{_datadir}/dbus-1/system-services/org.freedesktop.systemd1.service
%{_datadir}/dbus-1/system-services/org.freedesktop.timedate1.service
%{_datadir}/polkit-1/actions/org.freedesktop.hostname1.policy
%{_datadir}/polkit-1/actions/org.freedesktop.locale1.policy
%{_datadir}/polkit-1/actions/org.freedesktop.login1.policy
%{_datadir}/polkit-1/actions/org.freedesktop.systemd1.policy
%{_datadir}/polkit-1/actions/org.freedesktop.timedate1.policy
%dir %{_datadir}/systemd
%{?with_microhttpd:%{_datadir}/systemd/gatewayd}
%{_datadir}/systemd/kbd-model-map
%{_mandir}/man1/hostnamectl.1*
%{_mandir}/man1/journalctl.1*
%{_mandir}/man1/localectl.1*
%{_mandir}/man1/loginctl.1*
%{_mandir}/man1/systemd.1*
%{_mandir}/man1/systemd-ask-password.1*
%{_mandir}/man1/systemd-bootchart.1*
%{_mandir}/man1/systemd-cat.1*
%{_mandir}/man1/systemd-cgls.1*
%{_mandir}/man1/systemd-cgtop.1*
%{_mandir}/man1/systemd-coredumpctl.1*
%{_mandir}/man1/systemd-delta.1*
%{_mandir}/man1/systemd-detect-virt.1*
%{_mandir}/man1/systemd-inhibit.1*
%{_mandir}/man1/systemd-machine-id-setup.1*
%{_mandir}/man1/systemd-notify.1*
%{_mandir}/man1/systemd-nspawn.1*
%{_mandir}/man1/systemd-tty-ask-password-agent.1*
%{_mandir}/man1/timedatectl.1*
%{_mandir}/man5/binfmt.d.5*
%{_mandir}/man5/bootchart.conf.5*
# cfl with rc-scripts
#%{_mandir}/man5/crypttab.5*
%{_mandir}/man5/hostname.5*
%{_mandir}/man5/journald.conf.5*
%{_mandir}/man5/locale.conf.5*
%{_mandir}/man5/localtime.5*
%{_mandir}/man5/logind.conf.5*
%{_mandir}/man5/machine-id.5*
%{_mandir}/man5/machine-info.5*
%{_mandir}/man5/modules-load.d.5*
%{_mandir}/man5/os-release.5*
%{_mandir}/man5/sysctl.d.5*
%{_mandir}/man5/systemd.*.5*
%{_mandir}/man5/systemd-system.conf.5*
%{_mandir}/man5/systemd-user.conf.5*
%{_mandir}/man5/vconsole.conf.5*
%{_mandir}/man7/bootup.7*
%{_mandir}/man7/daemon.7*
%{_mandir}/man7/kernel-command-line.7*
%{_mandir}/man7/systemd.directives.7*
%{_mandir}/man7/systemd.index.7*
%{_mandir}/man7/systemd.journal-fields.7*
%{_mandir}/man7/systemd.special.7*
%{_mandir}/man7/systemd.time.7*
%{_mandir}/man8/kernel-install.8*
%{_mandir}/man8/nss-myhostname.8*
%{_mandir}/man8/systemd-activate.8*
%{_mandir}/man8/systemd-binfmt.8*
%{?with_cryptsetup:%{_mandir}/man8/systemd-cryptsetup-generator.8*}
%{_mandir}/man8/systemd-fsck.8*
%{_mandir}/man8/systemd-fstab-generator.8*
%{_mandir}/man8/systemd-getty-generator.8*
%{_mandir}/man8/systemd-hostnamed.8*
%{_mandir}/man8/systemd-initctl.8*
%{?with_microhttpd:%{_mandir}/man8/systemd-journal-gatewayd.8*}
%{_mandir}/man8/systemd-journald.8*
%{_mandir}/man8/systemd-localed.8*
%{_mandir}/man8/systemd-logind.8*
%{_mandir}/man8/systemd-modules-load.8*
%{_mandir}/man8/systemd-quotacheck.8*
%{_mandir}/man8/systemd-random-seed.8*
%{_mandir}/man8/systemd-readahead.8*
%{_mandir}/man8/systemd-remount-fs.8*
%{_mandir}/man8/systemd-shutdown.8*
%{_mandir}/man8/systemd-shutdownd.8*
%{_mandir}/man8/systemd-sleep.8*
%{_mandir}/man8/systemd-sysctl.8*
%{_mandir}/man8/systemd-system-update-generator.8*
%{_mandir}/man8/systemd-timedated.8*
%{_mandir}/man8/systemd-udevd.8*
%{_mandir}/man8/systemd-update-utmp.8*
%{_mandir}/man8/systemd-user-sessions.8*
%{_mandir}/man8/systemd-vconsole-setup.8*
%dir /var/lib/%{name}
%dir /var/lib/%{name}/coredump
%attr(640,root,root) %ghost /var/log/btmp
%attr(664,root,utmp) %ghost /var/log/wtmp
%dir /var/log/journal

%if %{with pam}
%attr(755,root,root) /%{_lib}/security/pam_systemd.so
%{_mandir}/man8/pam_systemd.8*
%endif

%files init
%defattr(644,root,root,755)
%attr(755,root,root) /sbin/halt
%attr(755,root,root) /sbin/init
%attr(755,root,root) /sbin/poweroff
%attr(755,root,root) /sbin/reboot
%attr(755,root,root) /sbin/runlevel
%attr(755,root,root) /sbin/shutdown
%attr(755,root,root) /sbin/telinit
%{_mandir}/man1/init.1
%{_mandir}/man8/halt.8*
%{_mandir}/man8/poweroff.8
%{_mandir}/man8/reboot.8
%{_mandir}/man8/runlevel.8*
%{_mandir}/man8/shutdown.8*
%{_mandir}/man8/telinit.8*

%files units
%defattr(644,root,root,755)
%dir %{_sysconfdir}/binfmt.d
%dir %{_sysconfdir}/modules-load.d
%config(noreplace,missingok) %verify(not md5 mtime size) %{_sysconfdir}/modules-load.d/modules.conf
%dir %{_sysconfdir}/sysctl.d
%dir %{_sysconfdir}/systemd
%dir %{_sysconfdir}/systemd/system
%dir %{_sysconfdir}/systemd/system-preset
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/systemd/system-preset/default.preset
%dir %{_sysconfdir}/tmpfiles.d
%dir %{_libexecdir}/binfmt.d
%dir %{_libexecdir}/modules-load.d
%dir %{_libexecdir}/sysctl.d
%dir /lib/systemd/system-sleep
%dir /lib/systemd/system-shutdown
%{_libexecdir}/sysctl.d/50-coredump.conf
%{_libexecdir}/sysctl.d/50-default.conf
%attr(755,root,root) /bin/systemctl
%attr(755,root,root) /bin/systemd-tmpfiles
%attr(755,root,root) /bin/systemd_booted
%{_mandir}/man1/systemctl.1*
%{_mandir}/man5/tmpfiles.d.5*
%{_mandir}/man8/systemd-tmpfiles.8*
%{_npkgconfigdir}/systemd.pc

%{systemdunitdir}/*.automount
%{systemdunitdir}/*.mount
%{systemdunitdir}/*.path
%{systemdunitdir}/*.service
%exclude %{systemdunitdir}/rc-inetd.service
%{systemdunitdir}/*.socket
%{systemdunitdir}/*.target
%{systemdunitdir}/*.timer
%dir %{systemdunitdir}/basic.target.wants
%dir %{systemdunitdir}/dbus.target.wants
%dir %{systemdunitdir}/final.target.wants
%dir %{systemdunitdir}/graphical.target.wants
%dir %{systemdunitdir}/halt.target.wants
%dir %{systemdunitdir}/initrd.target.wants
%dir %{systemdunitdir}/kexec.target.wants
%dir %{systemdunitdir}/local-fs.target.wants
%dir %{systemdunitdir}/multi-user.target.wants
%dir %{systemdunitdir}/poweroff.target.wants
%dir %{systemdunitdir}/reboot.target.wants
%dir %{systemdunitdir}/runlevel[12345].target.wants
%dir %{systemdunitdir}/shutdown.target.wants
%dir %{systemdunitdir}/sockets.target.wants
%dir %{systemdunitdir}/sysinit.target.wants
%dir %{systemdunitdir}/syslog.target.wants
%dir %{systemdunitdir}/timers.target.wants
%{systemdunitdir}/final.target.wants/*
%{systemdunitdir}/graphical.target.wants/*
%{systemdunitdir}/local-fs.target.wants/*
%{systemdunitdir}/multi-user.target.wants/getty.target
%{systemdunitdir}/multi-user.target.wants/rc-local.service
%{systemdunitdir}/multi-user.target.wants/systemd-ask-password-wall.path
%{systemdunitdir}/multi-user.target.wants/systemd-logind.service
%{systemdunitdir}/multi-user.target.wants/systemd-user-sessions.service
%{systemdunitdir}/runlevel[12345].target.wants/*
%{systemdunitdir}/shutdown.target.wants/*
%{systemdunitdir}/sockets.target.wants/*
%{?with_cryptsetup:%{systemdunitdir}/sysinit.target.wants/cryptsetup.target}
%{systemdunitdir}/sysinit.target.wants/dev-hugepages.mount
%{systemdunitdir}/sysinit.target.wants/dev-mqueue.mount
%{systemdunitdir}/sysinit.target.wants/proc-sys-fs-binfmt_misc.automount
%{systemdunitdir}/sysinit.target.wants/sys-*.mount
%{systemdunitdir}/sysinit.target.wants/systemd-*
%{systemdunitdir}/timers.target.wants/*.timer
%{_mandir}/man8/systemd-ask-password-console.path.8*
%{_mandir}/man8/systemd-ask-password-console.service.8*
%{_mandir}/man8/systemd-ask-password-wall.path.8*
%{_mandir}/man8/systemd-ask-password-wall.service.8*
%{_mandir}/man8/systemd-binfmt.service.8*
%{?with_cryptsetup:%{_mandir}/man8/systemd-cryptsetup.8*}
%{?with_cryptsetup:%{_mandir}/man8/systemd-cryptsetup@.service.8*}
%{_mandir}/man8/systemd-fsck-root.service.8*
%{_mandir}/man8/systemd-fsck@.service.8*
%{_mandir}/man8/systemd-halt.service.8*
%{_mandir}/man8/systemd-hibernate.service.8*
%{_mandir}/man8/systemd-hostnamed.service.8*
%{_mandir}/man8/systemd-hybrid-sleep.service.8*
%{_mandir}/man8/systemd-initctl.service.8*
%{_mandir}/man8/systemd-initctl.socket.8*
%{?with_microhttpd:%{_mandir}/man8/systemd-journal-gatewayd.service.8*}
%{?with_microhttpd:%{_mandir}/man8/systemd-journal-gatewayd.socket.8*}
%{_mandir}/man8/systemd-journald.service.8*
%{_mandir}/man8/systemd-journald.socket.8*
%{_mandir}/man8/systemd-kexec.service.8*
%{_mandir}/man8/systemd-localed.service.8*
%{_mandir}/man8/systemd-logind.service.8*
%{_mandir}/man8/systemd-modules-load.service.8*
%{_mandir}/man8/systemd-poweroff.service.8*
%{_mandir}/man8/systemd-quotacheck.service.8*
%{_mandir}/man8/systemd-random-seed-load.service.8*
%{_mandir}/man8/systemd-random-seed-save.service.8*
%{_mandir}/man8/systemd-readahead-collect.service.8*
%{_mandir}/man8/systemd-readahead-done.service.8*
%{_mandir}/man8/systemd-readahead-done.timer.8*
%{_mandir}/man8/systemd-readahead-replay.service.8*
%{_mandir}/man8/systemd-reboot.service.8*
%{_mandir}/man8/systemd-remount-fs.service.8*
%{_mandir}/man8/systemd-shutdownd.service.8*
%{_mandir}/man8/systemd-shutdownd.socket.8*
%{_mandir}/man8/systemd-suspend.service.8*
%{_mandir}/man8/systemd-sysctl.service.8*
%{_mandir}/man8/systemd-timedated.service.8*
%{_mandir}/man8/systemd-tmpfiles-clean.service.8*
%{_mandir}/man8/systemd-tmpfiles-clean.timer.8*
%{_mandir}/man8/systemd-tmpfiles-setup.service.8*
%{_mandir}/man8/systemd-udevd.service.8*
%{_mandir}/man8/systemd-udevd-control.socket.8*
%{_mandir}/man8/systemd-udevd-kernel.socket.8*
%{_mandir}/man8/systemd-update-utmp-runlevel.service.8*
%{_mandir}/man8/systemd-update-utmp-shutdown.service.8*
%{_mandir}/man8/systemd-user-sessions.service.8*
%{_mandir}/man8/systemd-vconsole-setup.service.8*

%files inetd
%defattr(644,root,root,755)
%attr(755,root,root) /lib/systemd/system-generators/pld-rc-inetd-generator
%{systemdunitdir}/rc-inetd.service

%files analyze
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/systemd-analyze
%{_mandir}/man1/systemd-analyze.1*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) /%{_lib}/libnss_myhostname.so.2
%attr(755,root,root) /%{_lib}/libsystemd-daemon.so.*.*.*
%attr(755,root,root) %ghost /%{_lib}/libsystemd-daemon.so.0
%attr(755,root,root) /%{_lib}/libsystemd-id128.so.*.*.*
%attr(755,root,root) %ghost /%{_lib}/libsystemd-id128.so.0
%attr(755,root,root) /%{_lib}/libsystemd-journal.so.*.*.*
%attr(755,root,root) %ghost /%{_lib}/libsystemd-journal.so.0
%attr(755,root,root) /%{_lib}/libsystemd-login.so.*.*.*
%attr(755,root,root) %ghost /%{_lib}/libsystemd-login.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libsystemd-daemon.so
%attr(755,root,root) %{_libdir}/libsystemd-id128.so
%attr(755,root,root) %{_libdir}/libsystemd-journal.so
%attr(755,root,root) %{_libdir}/libsystemd-login.so
%{_includedir}/%{name}
%{_pkgconfigdir}/libsystemd-daemon.pc
%{_pkgconfigdir}/libsystemd-id128.pc
%{_pkgconfigdir}/libsystemd-journal.pc
%{_pkgconfigdir}/libsystemd-login.pc
%{_mandir}/man3/SD_*.3*
%{_mandir}/man3/sd*.3*

%files static
%defattr(644,root,root,755)
%{_libdir}/libsystemd-daemon.a
%{_libdir}/libsystemd-id128.a
%{_libdir}/libsystemd-journal.a
%{_libdir}/libsystemd-login.a

%files -n bash-completion-systemd
%defattr(644,root,root,755)
%{_datadir}/bash-completion/completions/hostnamectl
%{_datadir}/bash-completion/completions/journalctl
%{_datadir}/bash-completion/completions/localectl
%{_datadir}/bash-completion/completions/loginctl
%{_datadir}/bash-completion/completions/systemctl
%{_datadir}/bash-completion/completions/systemd-coredumpctl
%{_datadir}/bash-completion/completions/timedatectl

%files -n udev
%defattr(644,root,root,755)
%dev(c,1,3) %attr(666,root,root) /dev/null
%dev(c,5,1) %attr(660,root,console) /dev/console
%dev(c,1,5) %attr(666,root,root) /dev/zero

%files -n udev-core
%defattr(644,root,root,755)

/usr/lib/udev

%attr(755,root,root) /lib/udev/collect

%attr(755,root,root) /lib/udev/keyboard-force-release.sh

%attr(755,root,root) /lib/udev/net_helper

%attr(755,root,root) /lib/udev/ata_id
%attr(755,root,root) /lib/udev/cdrom_id
%attr(755,root,root) /lib/udev/mtd_probe
%attr(755,root,root) /lib/udev/scsi_id
%attr(755,root,root) /lib/udev/v4l_id

%attr(755,root,root) /lib/udev/udevd

%attr(755,root,root) /lib/udev/keymap
%dir /lib/udev/keymaps
/lib/udev/keymaps/*

%attr(755,root,root) /lib/udev/accelerometer
%attr(755,root,root) /lib/udev/findkeyboards

%dir /lib/udev/hwdb.d
/lib/udev/hwdb.d/20-OUI.hwdb
/lib/udev/hwdb.d/20-acpi-vendor.hwdb
/lib/udev/hwdb.d/20-bluetooth-vendor-product.hwdb
/lib/udev/hwdb.d/20-pci-classes.hwdb
/lib/udev/hwdb.d/20-pci-vendor-model.hwdb
/lib/udev/hwdb.d/20-usb-classes.hwdb
/lib/udev/hwdb.d/20-usb-vendor-model.hwdb

%attr(755,root,root) %{_sbindir}/start_udev
%attr(755,root,root) %{_sbindir}/udevd
%attr(755,root,root) %{_sbindir}/udevadm
%attr(755,root,root) /bin/udevadm

%dir %{_sysconfdir}/udev
%dir %{_sysconfdir}/udev/rules.d
%dir %{_sysconfdir}/udev/hwdb.d

%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/modprobe.d/fbdev-blacklist.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/modprobe.d/udev_blacklist.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/udev/links.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/udev/rules.d/40-alsa-restore.rules
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/udev/rules.d/70-udev-pld.rules
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/udev/rules.d/80-net-name-slot.rules

%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/udev/udev.conf

# rules below are NOT supposed to be changed by users
/lib/udev/rules.d/42-usb-hid-pm.rules
/lib/udev/rules.d/50-udev-default.rules
/lib/udev/rules.d/60-cdrom_id.rules
/lib/udev/rules.d/60-persistent-alsa.rules
/lib/udev/rules.d/60-persistent-input.rules
/lib/udev/rules.d/60-persistent-serial.rules
/lib/udev/rules.d/60-persistent-storage-tape.rules
/lib/udev/rules.d/60-persistent-storage.rules
/lib/udev/rules.d/60-persistent-v4l.rules
/lib/udev/rules.d/61-accelerometer.rules
/lib/udev/rules.d/64-btrfs.rules
/lib/udev/rules.d/70-power-switch.rules
/lib/udev/rules.d/75-net-description.rules
/lib/udev/rules.d/75-probe_mtd.rules
/lib/udev/rules.d/75-tty-description.rules
/lib/udev/rules.d/78-sound-card.rules
/lib/udev/rules.d/80-drivers.rules
/lib/udev/rules.d/80-net-name-slot.rules
/lib/udev/rules.d/95-keyboard-force-release.rules
/lib/udev/rules.d/95-keymap.rules
/lib/udev/rules.d/95-udev-late.rules

%{_mandir}/man7/udev.7*
%{_mandir}/man8/udevadm.8*
%{_mandir}/man8/udevd.8*

%files -n udev-libs
%defattr(644,root,root,755)
%attr(755,root,root) /%{_lib}/libudev.so.*.*.*
%attr(755,root,root) %ghost /%{_lib}/libudev.so.1

%files -n udev-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libudev.so
%{_includedir}/libudev.h
%{_pkgconfigdir}/libudev.pc
%{_npkgconfigdir}/udev.pc

%files -n udev-static
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libudev.a

%files -n udev-apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/libudev

%files -n udev-glib
%defattr(644,root,root,755)
%attr(755,root,root) /%{_lib}/libgudev-1.0.so.*.*.*
%attr(755,root,root) %ghost /%{_lib}/libgudev-1.0.so.0
%{_libdir}/girepository-1.0/GUdev-1.0.typelib

%files -n udev-glib-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgudev-1.0.so
%{_includedir}/gudev-1.0
%{_pkgconfigdir}/gudev-1.0.pc
%{_datadir}/gir-1.0/GUdev-1.0.gir

%files -n udev-glib-static
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgudev-1.0.a

%files -n udev-glib-apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/gudev

%files -n bash-completion-udev
%defattr(644,root,root,755)
%{_datadir}/bash-completion/completions/udevadm

%files -n python-systemd
%defattr(644,root,root,755)
%dir %{py_sitedir}/systemd
%{py_sitedir}/systemd/*.py*
%attr(755,root,root) %{py_sitedir}/systemd/*.so
