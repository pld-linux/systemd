# TODO:
# - pldize vconsole setup:
# 	http://cgit.freedesktop.org/systemd/systemd/tree/src/vconsole/vconsole-setup.c
# - udev initrd needs love (is probably completly unusable in current form)
#
# Conditional build:
%bcond_without	audit		# without audit support
%bcond_without	cryptsetup	# without cryptsetup support
%bcond_without	pam		# PAM authentication support
%bcond_without	plymouth	# do not install plymouth units
%bcond_without	selinux		# without SELinux support
%bcond_without	tcpd		# libwrap (tcp_wrappers) support

%bcond_without	initrd		# build without udev-initrd
%bcond_with	uClibc		# link initrd version with static uClibc
%bcond_with	klibc		# link initrd version with static klibc
%bcond_with	dietlibc	# link initrd version with static dietlibc (currently broken and unsupported)
%bcond_without	glibc		# link initrd version with static glibc

%ifarch sparc sparc64
%define		with_glibc 1
%endif

# if one of the *libc is enabled disable default uClibc
%if %{with dietlibc} && %{with uClibc}
%undefine	with_uClibc
%endif

%if %{with glibc} && %{with uClibc}
%undefine	with_uClibc
%endif

%if %{with klibc} && %{with uClibc}
%undefine	with_uClibc
%endif

Summary:	A System and Service Manager
Summary(pl.UTF-8):	systemd - zarządca systemu i usług dla Linuksa
Name:		systemd
# Verify ChangeLog and NEWS when updating (since there are incompatible/breaking changes very often)
Version:	185
Release:	1.1
Epoch:		1
License:	GPL v2+
Group:		Base
Source0:	http://www.freedesktop.org/software/systemd/%{name}-%{version}.tar.xz
# Source0-md5:	a7dbbf05986eb0d2c164ec8e570eb78f
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
Patch5:		kmsg-to-syslog.patch
Patch6:		udev-so.patch
Patch7:		udev-uClibc.patch
Patch8:		udev-ploop-rules.patch
Patch9:		udevlibexecdir.patch
Patch10:	static-udev.patch
Patch11:	systemd-udev-service.patch
Patch12:	udevadm-in-sbin.patch
URL:		http://www.freedesktop.org/wiki/Software/systemd
BuildRequires:	acl-devel
%{?with_audit:BuildRequires:	audit-libs-devel}
BuildRequires:	autoconf >= 2.64
BuildRequires:	automake >= 1:1.11
BuildRequires:	binutils >= 3:2.22.52.0.1-2
%{?with_cryptsetup:BuildRequires:	cryptsetup-luks-devel}
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
%{?with_selinux:BuildRequires:	libselinux-devel >= 2.1.0}
BuildRequires:	libtool >= 2:2.2
%{?with_tcpd:BuildRequires:	libwrap-devel}
BuildRequires:	libxslt-progs
BuildRequires:	m4
%{?with_pam:BuildRequires:	pam-devel}
BuildRequires:	pciutils
BuildRequires:	pkgconfig >= 0.9.0
BuildRequires:	python-modules
BuildRequires:	rpmbuild(macros) >= 1.628
BuildRequires:	sed >= 4.0
BuildRequires:	usbutils >= 0.82
BuildRequires:	xz-devel
BuildRequires:	zlib-devel
%if %{with initrd}
BuildRequires:	acl-static
BuildRequires:	attr-static
%{?with_dietlibc:BuildRequires:	dietlibc-static}
BuildRequires:	glib2-static >= 1:2.22.0
%{?with_glibc:BuildRequires:	glibc-static}
%{?with_klibc:BuildRequires:	klibc-static}
BuildRequires:	kmod-libs-static >= 5
BuildRequires:	libblkid-static >= 2.20
%{?with_glibc:BuildRequires:	libselinux-static}
%{?with_glibc:BuildRequires:	libsepol-static}
%{?with_klibc:BuildRequires:	linux-libc-headers}
BuildRequires:	pcre-static
%{?with_uClibc:BuildRequires:	uClibc-static >= 4:0.9.30.3}
BuildRequires:	xz-static
BuildRequires:	zlib-static
%endif
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}
Requires:	%{name}-units = %{epoch}:%{version}-%{release}
Requires:	/etc/os-release
Requires:	SysVinit-tools
Requires:	agetty
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
Suggests:	nss_myhostname
Suggests:	service(klogd)
Suggests:	service(syslog)
Provides:	udev-acl
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

This package contains inet service generator that provides
the functionality of rc-inetd service and replaces a separate
inet daemon with systemd socket activation feature.

%description inetd -l pl.UTF-8
Natywna obsługa usług inet dla systemd.

Ten pakiet zawiera generator usług inet udostępniający funkcjonalność
serwisu rc-inetd i zastępujący osobny demon inet przez systemd i
aktywację usług przez gniazda.

%package plymouth
Summary:	Plymouth support units for systemd
Summary(pl.UTF-8):	Jednostki wspierające Plymouth dla systemd
Group:		Base
Requires:	%{name}-units = %{epoch}:%{version}-%{release}
Requires:	plymouth

%description plymouth
Plymouth (graphical boot) support units for systemd.

%description plymouth -l pl.UTF-8
Jednostki wspierające Plymouth (graficzny start systemu) dla systemd.

%package analyze
Summary:	Tool for processing systemd profiling information
Summary(pl.UTF-8):	Narzędzie do przetwarzania informacji profilujących systemd
Group:		Base
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	python-dbus
Requires:	python-modules
Requires:	python-pycairo
Conflicts:	%{name} < 44-3

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

%package -n bash-completion-systemd
Summary:	bash-completion for systemd
Summary(pl.UTF-8):	Bashowe dopełnianie składni dla systemd
Group:		Applications/Shells
Requires:	%{name} = %{epoch}:%{version}
Requires:	bash-completion

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
Obsoletes:	udev-compat
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
Requires:	udev-libs = %{epoch}:%{version}-%{release}
Requires:	coreutils
Requires:	filesystem >= 3.0-45
Requires:	setup >= 2.6.1-1
Requires:	uname(release) >= 2.6.32
Conflicts:	rc-scripts < 0.4.5.3-1
Conflicts:	systemd-units < 1:183
Conflicts:	udev < 1:118-1

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
Requires:	udev-libs = %{epoch}:%{version}-%{release}
Requires:	glib2 >= 1:2.22.0

%description -n udev-glib
Shared libgudev library - GObject bindings for libudev.

%description -n udev-glib -l pl.UTF-8
Biblioteka współdzielona libgudev - wiązania GObject do libudev.

%package -n udev-glib-devel
Summary:	Header file for libgudev library
Summary(pl.UTF-8):	Plik nagłówkowy biblioteki libgudev
Group:		Development/Libraries
Requires:	udev-devel = %{epoch}:%{version}-%{release}
Requires:	udev-glib = %{epoch}:%{version}-%{release}
Requires:	glib2-devel >= 1:2.22.0

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

%package -n udev-initrd
Summary:	A userspace implementation of devfs - static binary for initrd
Summary(pl.UTF-8):	Implementacja devfs w przestrzeni użytkownika - statyczna binarka dla initrd
Group:		Base
Requires:	udev-core = %{epoch}:%{version}-%{release}
Conflicts:	geninitrd < 10000.10

%description -n udev-initrd
A userspace implementation of devfs - static binary for initrd.

%description -n udev-initrd -l pl.UTF-8
Implementacja devfs w przestrzeni użytkownika - statyczna binarka dla
initrd.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
#patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%if %{with uClibc}
%patch7 -p1
%endif
%patch8 -p1
%patch9 -p1
%patch11 -p1
%patch12 -p1
cp -p %{SOURCE2} src/systemd_booted.c

%build
%{__gtkdocize}
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%if %{with initrd}
patch -p1 <%{PATCH10}
%configure \
%if "%{?configure_cache}" == "1"
	--cache-file=%{?configure_cache_file}%{!?configure_cache_file:configure}-initrd.cache \
%endif
	%{?with_uClibc:CC="%{_target_cpu}-uclibc-gcc"} \
	%{?with_dietlibc:CC="diet %{__cc} %{rpmcflags} %{rpmldflags} -Os -D_BSD_SOURCE"} \
	%{?with_klibc:CC="%{_bindir}/klcc"} \
	%{?debug:--enable-debug} \
	--disable-silent-rules \
	--disable-shared \
	--enable-static \
	--with-distro=pld \
	--with-rootprefix="" \
	--with-rootlibdir=/%{_lib} \
	--disable-gudev \
	--disable-keymap \
	--disable-gtk-doc \
	--disable-introspection \
	--with-pci-ids-path=%{_sysconfdir}/pci.ids \
	--disable-audit \
	--disable-pam \
	--disable-plymouth \
	--disable-selinux \
	--enable-split-usr

%{__make} \
	libudev-core.la \
	systemd-udevd \
	udevadm \
	ata_id \
	cdrom_id \
	collect \
	scsi_id \
	v4l_id \
	accelerometer \
	mtd_probe \
	LDFLAGS="-all-static" \
	KMOD_LIBS="-lkmod -lz -llzma"

mkdir udev-initrd
cp -a systemd-udevd \
	udevadm \
	ata_id \
	cdrom_id \
	collect \
	scsi_id \
	v4l_id \
	accelerometer \
	mtd_probe \
	udev-initrd/

%{__make} clean
patch -p1 -R <%{PATCH10}
%endif

%configure \
	%{?debug:--enable-debug} \
	%{__enable_disable audit} \
	%{__enable_disable cryptsetup libcryptsetup} \
	%{__enable_disable pam} \
	%{__enable_disable plymouth} \
	%{__enable_disable selinux} \
	%{__enable_disable tcpd tcpwrap} \
	--disable-silent-rules \
	--enable-shared \
	--enable-static \
	--with-distro=pld \
	--with-rootprefix="" \
	--with-rootlibdir=/%{_lib} \
	--with-html-dir=%{_gtkdocdir} \
	--with-pci-ids-path=%{_sysconfdir}/pci.ids \
	--enable-gtk-doc \
	--enable-introspection \
	--enable-split-usr

%{__make}
./libtool --mode=link --tag=CC %{__cc} %{rpmcppflags} %{rpmcflags} -o systemd_booted %{rpmldflags} src/systemd_booted.c -L. -lsystemd-daemon

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/var/lib/%{name}/coredump \
	$RPM_BUILD_ROOT{%{_sysconfdir}/modprobe.d,%{_sbindir}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

./libtool --mode=install install -p -m755 systemd_booted $RPM_BUILD_ROOT/bin/systemd_booted

# compatibility symlinks to udevd binary
mv $RPM_BUILD_ROOT/lib/{systemd/systemd-,udev/}udevd
ln -s /lib/udev/udevd $RPM_BUILD_ROOT/lib/systemd/systemd-udevd
ln -s /lib/udev/udevd $RPM_BUILD_ROOT%{_sbindir}/udevd

# compat symlinks for "/ merged into /usr" programs
mv $RPM_BUILD_ROOT{%{_bindir},%{_sbindir}}/udevadm
ln -s %{_sbindir}/udevadm $RPM_BUILD_ROOT%{_bindir}
ln -s /lib/udev $RPM_BUILD_ROOT/usr/lib/

# install custom udev rules from pld package
cp -a %{SOURCE101} $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d/40-alsa-restore.rules
cp -a %{SOURCE102} $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d/70-udev-pld.rules

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

%if %{with initrd}
install -d $RPM_BUILD_ROOT%{_libdir}/initrd/udev
install -p udev-initrd/udevadm $RPM_BUILD_ROOT%{_libdir}/initrd
install -p udev-initrd/systemd-udevd $RPM_BUILD_ROOT%{_libdir}/initrd
# hardlink udevd -> systemd-udevd
ln $RPM_BUILD_ROOT%{_libdir}/initrd/{systemd-,}udevd
ln -s udevd $RPM_BUILD_ROOT%{_libdir}/initrd/udevstart
install -p udev-initrd/*_id $RPM_BUILD_ROOT%{_libdir}/initrd/udev
install -p udev-initrd/collect $RPM_BUILD_ROOT%{_libdir}/initrd/udev
install -p udev-initrd/mtd_probe $RPM_BUILD_ROOT%{_libdir}/initrd/udev
%endif

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

# handled by rc-local sysv service, no need for generator
%{__rm} $RPM_BUILD_ROOT/lib/systemd/system-generators/systemd-rc-local-generator

# Make sure these directories are properly owned:
#	- halt,kexec,poweroff,reboot: generic ones used by ConsoleKit-systemd,
#	- syslog _might_ be used by some syslog implementation (none for now),
#	- isn't dbus populated by dbus-systemd only (so to be moved there)?
install -d $RPM_BUILD_ROOT%{systemdunitdir}/{dbus,halt,kexec,poweroff,reboot,syslog}.target.wants

# Create new-style configuration files so that we can ghost-own them
touch $RPM_BUILD_ROOT%{_sysconfdir}/{hostname,locale.conf,machine-id,machine-info,timezone,vconsole.conf}

# Install SysV conversion tool for systemd
install -p %{SOURCE1} $RPM_BUILD_ROOT%{_bindir}

install -d $RPM_BUILD_ROOT/var/log
:> $RPM_BUILD_ROOT/var/log/btmp
:> $RPM_BUILD_ROOT/var/log/wtmp

%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}
%{__rm} $RPM_BUILD_ROOT/%{_lib}/security/pam_systemd.la
%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post
/bin/systemd-machine-id-setup > /dev/null 2>&1 || :
/bin/systemctl daemon-reexec > /dev/null 2>&1 || :

%postun
if [ $1 -ge 1 ]; then
	/bin/systemctl try-restart systemd-logind.service >/dev/null 2>&1 || :
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

%post inetd
%systemd_reload
# Do not change it to restart, we only want to start new services here
%systemd_service_start sockets.target

%postun inetd
%systemd_reload

%post plymouth
%systemd_reload

%postun plymouth
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
		/bin/systemctl --quiet try-restart systemd-udev.service || :
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
%attr(755,root,root) %{_bindir}/systemd-cat
%attr(755,root,root) %{_bindir}/systemd-cgtop
%attr(755,root,root) %{_bindir}/systemd-cgls
%attr(755,root,root) %{_bindir}/systemd-delta
%attr(755,root,root) %{_bindir}/systemd-detect-virt
%attr(755,root,root) %{_bindir}/systemd-nspawn
%attr(755,root,root) %{_bindir}/systemd-stdio-bridge
%attr(755,root,root) %{_bindir}/systemd-sysv-convert
%attr(755,root,root) /lib/systemd/pld-clean-tmp
%attr(755,root,root) /lib/systemd/pld-storage-init
%attr(755,root,root) /lib/systemd/systemd-ac-power
%attr(755,root,root) /lib/systemd/systemd-binfmt
%attr(755,root,root) /lib/systemd/systemd-cgroups-agent
%attr(755,root,root) /lib/systemd/systemd-coredump
%attr(755,root,root) /lib/systemd/systemd-cryptsetup
%attr(755,root,root) /lib/systemd/systemd-fsck
%attr(755,root,root) /lib/systemd/systemd-hostnamed
%attr(755,root,root) /lib/systemd/systemd-initctl
%attr(755,root,root) /lib/systemd/systemd-journald
%attr(755,root,root) /lib/systemd/systemd-localed
%attr(755,root,root) /lib/systemd/systemd-logind
%attr(755,root,root) /lib/systemd/systemd-modules-load
%attr(755,root,root) /lib/systemd/systemd-multi-seat-x
%attr(755,root,root) /lib/systemd/systemd-quotacheck
%attr(755,root,root) /lib/systemd/systemd-random-seed
%attr(755,root,root) /lib/systemd/systemd-readahead-collect
%attr(755,root,root) /lib/systemd/systemd-readahead-replay
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
%dir /lib/systemd/system-shutdown
/lib/udev/rules.d/99-systemd.rules
/lib/udev/rules.d/70-uaccess.rules
/lib/udev/rules.d/71-seat.rules
/lib/udev/rules.d/73-seat-late.rules
%dir %{_libexecdir}/systemd
%{_libexecdir}/systemd/user
%dir %{_libexecdir}/systemd/user-generators
%config(noreplace,missingok) %{_libexecdir}/tmpfiles.d/legacy.conf
%config(noreplace,missingok) %{_libexecdir}/tmpfiles.d/systemd.conf
%config(noreplace,missingok) %{_libexecdir}/tmpfiles.d/tmp.conf
%config(noreplace,missingok) %{_libexecdir}/tmpfiles.d/x11.conf
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
%{_datadir}/systemd/kbd-model-map
%{_mandir}/man1/journalctl.1*
%{_mandir}/man1/loginctl.1*
%{_mandir}/man1/systemd.1*
%{_mandir}/man1/systemd-ask-password.1*
%{_mandir}/man1/systemd-cat.1*
%{_mandir}/man1/systemd-cgls.1*
%{_mandir}/man1/systemd-cgtop.1*
%{_mandir}/man1/systemd-delta.1*
%{_mandir}/man1/systemd-detect-virt.1*
%{_mandir}/man1/systemd-inhibit.1*
%{_mandir}/man1/systemd-machine-id-setup.1*
%{_mandir}/man1/systemd-notify.1*
%{_mandir}/man1/systemd-nspawn.1*
%{_mandir}/man5/binfmt.d.5*
%{_mandir}/man5/hostname.5*
%{_mandir}/man5/journald.conf.5*
%{_mandir}/man5/locale.conf.5*
%{_mandir}/man5/logind.conf.5*
%{_mandir}/man5/machine-id.5*
%{_mandir}/man5/machine-info.5*
%{_mandir}/man5/modules-load.d.5*
%{_mandir}/man5/os-release.5*
%{_mandir}/man5/sysctl.d.5*
%{_mandir}/man5/systemd.*.5*
%{_mandir}/man5/timezone.5*
%{_mandir}/man5/vconsole.conf.5*
%{_mandir}/man7/daemon.7*
%{_mandir}/man7/sd-daemon.7*
%{_mandir}/man7/sd-login.7*
%{_mandir}/man7/sd-readahead.7*
%{_mandir}/man7/systemd.special.7*
%{_mandir}/man7/systemd.journal-fields.7*
%{_mandir}/man8/systemd-binfmt.8*
%{_mandir}/man8/systemd-binfmt.service.8*
%{_mandir}/man8/systemd-journald.8*
%{_mandir}/man8/systemd-journald.service.8*
%{_mandir}/man8/systemd-logind.8*
%{_mandir}/man8/systemd-logind.service.8*
%{_mandir}/man8/systemd-modules-load.8*
%{_mandir}/man8/systemd-modules-load.service.8*
%{_mandir}/man8/systemd-sysctl.8*
%{_mandir}/man8/systemd-sysctl.service.8*
%{_mandir}/man8/systemd-udevd.8*
%dir /var/lib/%{name}
%dir /var/lib/%{name}/coredump
%attr(640,root,root) %ghost /var/log/btmp
%attr(664,root,utmp) %ghost /var/log/wtmp

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
%dir %{_sysconfdir}/tmpfiles.d
%dir %{_libexecdir}/binfmt.d
%dir %{_libexecdir}/modules-load.d
%dir %{_libexecdir}/sysctl.d
# Don't package the kernel.core_pattern setting until systemd-coredump
# is a part of an actual systemd release and it's made clear how to
# get the core dumps out of the journal.
#%{_libexecdir}/sysctl.d/coredump.conf
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
%{systemdunitdir}/*.socket
%{systemdunitdir}/*.target
%{systemdunitdir}/*.timer
%if %{with plymouth}
%exclude %{systemdunitdir}/plymouth*.service
%exclude %{systemdunitdir}/systemd-ask-password-plymouth.*
%endif
%dir %{systemdunitdir}/basic.target.wants
%dir %{systemdunitdir}/dbus.target.wants
%dir %{systemdunitdir}/final.target.wants
%dir %{systemdunitdir}/graphical.target.wants
%dir %{systemdunitdir}/halt.target.wants
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
%config(noreplace,missingok) %{systemdunitdir}/basic.target.wants/*
%config(noreplace,missingok) %{systemdunitdir}/final.target.wants/*
%config(noreplace,missingok) %{systemdunitdir}/graphical.target.wants/*
%config(noreplace,missingok) %{systemdunitdir}/local-fs.target.wants/*
%config(noreplace,missingok) %{systemdunitdir}/multi-user.target.wants/getty.target
%config(noreplace,missingok) %{systemdunitdir}/multi-user.target.wants/rc-local.service
%config(noreplace,missingok) %{systemdunitdir}/multi-user.target.wants/systemd-ask-password-wall.path
%config(noreplace,missingok) %{systemdunitdir}/multi-user.target.wants/systemd-logind.service
%config(noreplace,missingok) %{systemdunitdir}/multi-user.target.wants/systemd-user-sessions.service
%config(noreplace,missingok) %{systemdunitdir}/runlevel[12345].target.wants/*
%config(noreplace,missingok) %{systemdunitdir}/shutdown.target.wants/*
%config(noreplace,missingok) %{systemdunitdir}/sockets.target.wants/*
%{?with_cryptsetup:%config(noreplace,missingok) %{systemdunitdir}/sysinit.target.wants/cryptsetup.target}
%config(noreplace,missingok) %{systemdunitdir}/sysinit.target.wants/dev-hugepages.mount
%config(noreplace,missingok) %{systemdunitdir}/sysinit.target.wants/dev-mqueue.mount
%config(noreplace,missingok) %{systemdunitdir}/sysinit.target.wants/proc-sys-fs-binfmt_misc.automount
%config(noreplace,missingok) %{systemdunitdir}/sysinit.target.wants/sys-*.mount
%config(noreplace,missingok) %{systemdunitdir}/sysinit.target.wants/systemd-*

%files inetd
%defattr(644,root,root,755)
%attr(755,root,root) /lib/systemd/system-generators/pld-rc-inetd-generator
%{systemdunitdir}/rc-inetd.service

%if %{with plymouth}
%files plymouth
%defattr(644,root,root,755)
%{systemdunitdir}/plymouth-halt.service
%{systemdunitdir}/plymouth-kexec.service
%{systemdunitdir}/plymouth-poweroff.service
%{systemdunitdir}/plymouth-quit-wait.service
%{systemdunitdir}/plymouth-quit.service
%{systemdunitdir}/plymouth-read-write.service
%{systemdunitdir}/plymouth-reboot.service
%{systemdunitdir}/plymouth-start.service
%{systemdunitdir}/systemd-ask-password-plymouth.path
%{systemdunitdir}/systemd-ask-password-plymouth.service
%config(noreplace,missingok) %{systemdunitdir}/halt.target.wants/plymouth-halt.service
%config(noreplace,missingok) %{systemdunitdir}/kexec.target.wants/plymouth-kexec.service
%config(noreplace,missingok) %{systemdunitdir}/multi-user.target.wants/plymouth-quit.service
%config(noreplace,missingok) %{systemdunitdir}/multi-user.target.wants/plymouth-quit-wait.service
%config(noreplace,missingok) %{systemdunitdir}/poweroff.target.wants/plymouth-poweroff.service
%config(noreplace,missingok) %{systemdunitdir}/reboot.target.wants/plymouth-reboot.service
%config(noreplace,missingok) %{systemdunitdir}/sysinit.target.wants/plymouth-read-write.service
%config(noreplace,missingok) %{systemdunitdir}/sysinit.target.wants/plymouth-start.service
%endif

%files analyze
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/systemd-analyze

%files libs
%defattr(644,root,root,755)
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
%{_mandir}/man3/sd_booted.3*
%{_mandir}/man3/sd_get_seats.3*
%{_mandir}/man3/sd_get_sessions.3*
%{_mandir}/man3/sd_get_uids.3*
%{_mandir}/man3/sd_is_fifo.3*
%{_mandir}/man3/sd_is_mq.3*
%{_mandir}/man3/sd_is_socket.3
%{_mandir}/man3/sd_is_socket_inet.3
%{_mandir}/man3/sd_is_socket_unix.3
%{_mandir}/man3/sd_listen_fds.3*
%{_mandir}/man3/sd_login_monitor_flush.3*
%{_mandir}/man3/sd_login_monitor_get_fd.3*
%{_mandir}/man3/sd_login_monitor_new.3*
%{_mandir}/man3/sd_login_monitor_unref.3*
%{_mandir}/man3/sd_notify.3*
%{_mandir}/man3/sd_notifyf.3
%{_mandir}/man3/sd_pid_get_owner_uid.3*
%{_mandir}/man3/sd_pid_get_session.3*
%{_mandir}/man3/sd_pid_get_unit.3*
%{_mandir}/man3/sd_readahead.3*
%{_mandir}/man3/sd_seat_can_multi_session.3*
%{_mandir}/man3/sd_seat_get_active.3*
%{_mandir}/man3/sd_seat_get_sessions.3*
%{_mandir}/man3/sd_session_get_class.3*
%{_mandir}/man3/sd_session_get_display.3*
%{_mandir}/man3/sd_session_get_seat.3*
%{_mandir}/man3/sd_session_get_service.3*
%{_mandir}/man3/sd_session_get_type.3*
%{_mandir}/man3/sd_session_get_uid.3*
%{_mandir}/man3/sd_session_is_active.3*
%{_mandir}/man3/sd_uid_get_seats.3*
%{_mandir}/man3/sd_uid_get_sessions.3*
%{_mandir}/man3/sd_uid_get_state.3*
%{_mandir}/man3/sd_uid_is_on_seat.3*

%files -n bash-completion-systemd
%defattr(644,root,root,755)
/etc/bash_completion.d/systemd-bash-completion.sh

%files -n udev
%defattr(644,root,root,755)
%dev(c,1,3) %attr(666,root,root) /dev/null
%dev(c,5,1) %attr(660,root,console) /dev/console
%dev(c,1,5) %attr(666,root,root) /dev/zero

%files -n udev-core
%defattr(644,root,root,755)

/usr/lib/udev

# /lib/udev/devices/ are not read anymore; systemd-tmpfiles
# should be used to create dead device nodes as workarounds for broken
# subsystems.
%dir /lib/udev/devices

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

%attr(755,root,root) %{_sbindir}/start_udev
%attr(755,root,root) %{_sbindir}/udevd
%attr(755,root,root) %{_sbindir}/udevadm
%attr(755,root,root) %{_bindir}/udevadm

%dir %{_sysconfdir}/udev
%dir %{_sysconfdir}/udev/rules.d

%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/modprobe.d/fbdev-blacklist.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/modprobe.d/udev_blacklist.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/udev/links.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/udev/rules.d/40-alsa-restore.rules
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/udev/rules.d/70-udev-pld.rules

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
/lib/udev/rules.d/70-power-switch.rules
/lib/udev/rules.d/75-net-description.rules
/lib/udev/rules.d/75-probe_mtd.rules
/lib/udev/rules.d/75-tty-description.rules
/lib/udev/rules.d/78-sound-card.rules
/lib/udev/rules.d/80-drivers.rules
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

%if %{with initrd}
%files -n udev-initrd
%defattr(644,root,root,755)
%dir %{_libdir}/initrd/udev
%attr(755,root,root) %{_libdir}/initrd/systemd-udevd
%attr(755,root,root) %{_libdir}/initrd/udevd
%attr(755,root,root) %{_libdir}/initrd/udevadm
%attr(755,root,root) %{_libdir}/initrd/udevstart
%attr(755,root,root) %{_libdir}/initrd/udev/*_id
%attr(755,root,root) %{_libdir}/initrd/udev/collect
%attr(755,root,root) %{_libdir}/initrd/udev/mtd_probe
%endif
