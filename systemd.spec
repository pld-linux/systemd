# TODO:
# - consider providing the factory files via appropriate packages (setup, pam)
# - merge rpm macros provided by systemd with ours
# - handle udev package removal:
#   - http://lists.pld-linux.org/mailman/pipermail/pld-devel-en/2014-March/023852.html
#   - restore (write) sane value for kernel.hotplug, i.e from rc-scripts: sysctl -q -e -w kernel.hotplug=/lib/firmware/firmware-loader.sh
# - dev->udev upgrade:
#   - /dev/urandom remains missing, not created with start_udev anymore
# - clean up unpackaged files
#
# Conditional build:
%bcond_without	audit		# audit support
%bcond_without	bpf		# BPF programs in restricted C support
%bcond_without	cryptsetup	# cryptsetup support
%bcond_without	microhttpd	# use microhttpd for network journal access
%bcond_without	pam		# PAM authentication support
%bcond_without	qrencode	# QRencode support
%bcond_without	selinux		# SELinux support
%bcond_without	efi		# EFI boot support
%bcond_without	fido2		# FIDO2 support
%bcond_without	tpm2		# TPM2 support
%bcond_with	tests		# "make check" (requires systemd already installed)
%bcond_with	xen		# Xen kexec support

%define         min_kernel      3.15

%ifnarch %{ix86} %{x8664} aarch64
# x32 disabled - maybe it's possible to build x64 EFI, but it requires some hacking (add -m64 to EFI gcc command line?)
%undefine	with_efi
%endif
Summary:	A System and Service Manager
Summary(pl.UTF-8):	systemd - zarządca systemu i usług dla Linuksa
Name:		systemd
# Verify ChangeLog and NEWS when updating (since there are incompatible/breaking changes very often)
Version:	253.7
Release:	1
Epoch:		1
License:	GPL v2+ (udev), LGPL v2.1+ (the rest)
Group:		Base
#Source0Download: https://github.com/systemd/systemd/releases
Source0:	https://github.com/systemd/systemd-stable/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	08469f585a4c825957051978df079b1a
Source1:	%{name}-sysv-convert
Source2:	%{name}_booted.c
Source3:	network.service
Source4:	var-lock.mount
Source5:	var-run.mount
Source14:	pld-clean-tmp.service
Source15:	pld-clean-tmp.sh
Source16:	pld-rc-inetd-generator.sh
Source17:	rc-inetd.service
Source18:	default.preset
Source19:	prefdm.service
Source20:	sigpwr-container-shutdown.service

# rules
Source101:	udev-alsa.rules
Source102:	udev.rules
Source103:	udev-links.conf
Source104:	udev-uinput.rules
Source105:	udev-steam_controller.rules
Source106:	udev-i2c.rules
Source107:	udev-raspberrypi.rules
# scripts / helpers
Source110:	udev-net.helper
Source111:	start_udev
# misc
Source120:	udev.blacklist
Source121:	fbdev.blacklist
Patch0:		target-pld.patch
Patch1:		config-pld.patch
Patch2:		pld-sysv-network.patch
Patch3:		tmpfiles-not-fatal.patch
Patch4:		udev-ploop-rules.patch
Patch5:		%{name}-split-usr-fix.patch
Patch6:		net-rename-revert.patch
Patch7:		%{name}-completion.patch
Patch8:		proc-hidepid.patch
Patch9:		%{name}-configfs.patch
Patch10:	pld-boot_efi_mount.patch
Patch11:	optional-tmp-on-tmpfs.patch
Patch13:	sysctl.patch
Patch14:	pld-pam-%{name}-user.patch
Patch15:	%{name}-x32.patch
Patch16:	rpm-macros.patch
Patch17:	%{name}-glibc.patch
URL:		https://www.freedesktop.org/wiki/Software/systemd/
BuildRequires:	acl-devel
%{?with_audit:BuildRequires:	audit-libs-devel}
%if %{with efi}
BuildRequires:	binutils >= 4:2.38
%else
BuildRequires:	binutils >= 3:2.22.52.0.1-2
%endif
BuildRequires:	bzip2-devel
%{?with_bpf:BuildRequires:	clang >= 10.0.0}
# ln --relative
BuildRequires:	coreutils >= 8.16
%{?with_cryptsetup:BuildRequires:	cryptsetup-devel >= 2.4.0}
BuildRequires:	curl-devel >= 7.32.0
BuildRequires:	dbus-devel >= 1.9.18
BuildRequires:	docbook-dtd42-xml
BuildRequires:	docbook-dtd45-xml
BuildRequires:	docbook-style-xsl-nons
BuildRequires:	elfutils-devel >= 0.177
BuildRequires:	gcc >= 6:4.9
BuildRequires:	gettext-tools
BuildRequires:	glib2-devel >= 1:2.22.0
BuildRequires:	glibc-misc
%{?with_efi:BuildRequires:	gnu-efi}
BuildRequires:	gnutls-devel >= 3.6.0
BuildRequires:	gperf
BuildRequires:	intltool >= 0.40.0
# pkgconfig(libiptc)
BuildRequires:	iptables-devel
%{?with_bpf:BuildRequires:	kernel-tools >= 5.13.0}
BuildRequires:	kmod-devel >= 15
BuildRequires:	libapparmor-devel >= 1:2.13
BuildRequires:	libblkid-devel >= 2.24
%{?with_bpf:BuildRequires:	libbpf-devel >= 0.1.0}
BuildRequires:	libcap-devel
BuildRequires:	libfdisk-devel >= 2.32
%{?with_fido2:BuildRequires:	libfido2-devel}
BuildRequires:	libgcrypt-devel >= 1.4.5
BuildRequires:	libgpg-error-devel >= 1.12
BuildRequires:	libidn2-devel
%{?with_microhttpd:BuildRequires:	libmicrohttpd-devel >= 0.9.33}
BuildRequires:	libmount-devel >= 2.30
BuildRequires:	libpwquality-devel
BuildRequires:	libseccomp-devel >= 2.4.0
%{?with_selinux:BuildRequires:	libselinux-devel >= 2.6}
BuildRequires:	libtool >= 2:2.2
BuildRequires:	libxslt-progs
BuildRequires:	lz4-devel >= 1:1.3.0
BuildRequires:	m4
BuildRequires:	meson >= 0.53.2
BuildRequires:	ninja
BuildRequires:	openssl-devel
BuildRequires:	p11-kit-devel >= 0.23.3
%{?with_pam:BuildRequires:	pam-devel >= 1.1.2}
BuildRequires:	pcre2-8-devel
# for sbat-distro* in src/boot/efi/meson.build
BuildRequires:	pld-release
BuildRequires:	pkgconfig >= 1:0.9.0
BuildRequires:	polkit-devel >= 0.106
BuildRequires:	python3 >= 1:3.9
BuildRequires:	python3-jinja2
BuildRequires:	python3-lxml
%{?with_qrencode:BuildRequires:	qrencode-devel >= 3}
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.752
BuildRequires:	sed >= 4.0
%{?with_tests:BuildRequires:	systemd}
%{?with_tpm2:BuildRequires:	tpm2-tss-devel >= 3.0.0}
BuildRequires:	usbutils >= 0.82
%{?with_xen:BuildRequires:	xen-devel}
BuildRequires:	xorg-lib-libxkbcommon-devel >= 0.5.0
BuildRequires:	xz-devel
BuildRequires:	zlib-devel
BuildRequires:	zstd-devel >= 1.4.0
Requires(post,postun):	%{name}-units = %{epoch}:%{version}-%{release}
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(post):	/bin/setfacl
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}
Requires:	%{name}-units = %{epoch}:%{version}-%{release}
Requires:	%{name}-tools = %{epoch}:%{version}-%{release}
Requires:	/etc/os-release
Requires:	SysVinit-tools
Requires:	agetty
Requires:	dbus >= 1.9.18
Requires:	elfutils >= 0.177
Requires:	filesystem >= 4.0-39
Requires:	glibc >= 2.16
Requires:	kmod >= 25-2
Requires:	libgpg-error >= 1.12
Requires:	libutempter
Requires:	polkit >= 0.106
Requires:	rc-scripts >= 0.4.5.3-7
Requires:	setup >= 2.10.1
Requires:	udev-core = %{epoch}:%{version}-%{release}
Requires:	udev-libs = %{epoch}:%{version}-%{release}
Requires:	uname(release) >= %{min_kernel}
Requires:	util-linux >= 2.30
Suggests:	%{name}-container = %{epoch}:%{version}-%{release}
Suggests:	%{name}-sysv-compat = %{epoch}:%{version}-%{release}
%{?with_cryptsetup:Suggests:	cryptsetup >= 2.4.0}
Suggests:	fsck >= 2.25.0
%{?with_fido2:Suggests:	libfido2}
Suggests:	libidn2
Suggests:	libpwquality
Suggests:	pcre2-8
%{?with_qrencode:Suggests:	qrencode-libs >= 3}
Suggests:	service(klogd)
Suggests:	service(syslog)
Suggests:	xorg-lib-libxkbcommon >= 0.5.0
Provides:	group(systemd-coredump)
Provides:	group(systemd-journal)
Provides:	group(systemd-network)
Provides:	group(systemd-oom)
Provides:	group(systemd-resolve)
Provides:	group(systemd-timesync)
Provides:	udev-acl = %{epoch}:%{version}-%{release}
Provides:	user(systemd-coredump)
Provides:	user(systemd-network)
Provides:	user(systemd-oom)
Provides:	user(systemd-resolve)
Provides:	user(systemd-timesync)
# kde4 still can't live without ConsoleKit
#Obsoletes:	ConsoleKit
#Obsoletes:	ConsoleKit-x11
Obsoletes:	elogind
Obsoletes:	systemd-no-compat-tmpfiles < 1:183-1
Obsoletes:	udev-acl < 1:181-1
Obsoletes:	udev-systemd < 1:182-1
# for storage detection / activation services
Conflicts:	dmraid < 1.0.0-0.rc16.3.3
Conflicts:	mdadm < 4.0-2
# sytemd wants pam with pam_systemd.so in system-auth...
Conflicts:	pam < 1:1.1.5-5
# ...and sudo hates it
Conflicts:	sudo < 1:1.7.8p2-4
# for prefdm script
Conflicts:	xinitrc-ng < 1.0
# systemd scripts use options not present in older versions
Conflicts:	kpartx < 0.6.1-1
Conflicts:	multipath-tools < 0.6.1-1
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
Conflicts:	fsck < 2.25.0
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
# Needed for vgscan --cache ( perhaps < 2.02.96 would be enough, but not tested)
Conflicts:	lvm2 < 2.02.132
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

%define		_rootsbindir	/sbin

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
Provides:	virtual-init-daemon
Obsoletes:	SysVinit
Obsoletes:	virtual-init-daemon
Conflicts:	rc-scripts < 0.4.5.5-2
Conflicts:	upstart
# systemd takes care of that and causes problems
Conflicts:	binfmt-detector
# for /lib/systemd/systemd-sysv-install
Conflicts:	chkconfig < 2:1.5-1

%description init
Install this package when you are ready to final switch to systemd.

%description init -l pl.UTF-8
Ten pakiet należy zainstalować po przygotowaniu się do ostatecznego
przejścia na systemd.

%package sysv-compat
Summary:	systemd/SysV interoperability tools
Summary(pl.UTF-8):	Narzędzia wspomagające współpracę między systemd a SysV
Group:		Base
Requires:	python3
Requires:	python3-modules

%description sysv-compat
systemd/SysV interoperability tools.

%description sysv-compat -l pl.UTF-8
Narzędzia wspomagające współpracę między systemd a SysV.

%package units
Summary:	Configuration files, directories and installation tool for systemd
Summary(pl.UTF-8):	Pliki konfiguracyjne, katalogi i narzędzie instalacyjne dla systemd
Group:		Base
Requires(post):	coreutils
Requires(post):	/bin/awk
Requires:	less >= 568

%description units
Basic configuration files, directories and installation tool for the
systemd system and service manager.

This is common config, use %{_sysconfdir}/systemd/system to override.

%description units -l pl.UTF-8
Podstawowe pliki konfiguracyjne, katalogi i narzędzie instalacyjne dla
zarządcy systemu i usług systemd.

Ten pakiet zawiera ogólną konfigurację, ustawienia można nadpisać
poprzez katalog %{_sysconfdir}/systemd/system.

%package tools
Summary:	Tools that work with and without systemd started
Summary(pl.UTF-8):	Narzędzia działające przy uruchomionym jak i bez systemd
Group:		Base
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}

%description tools
Tools that work with and without systemd started.

%description tools -l pl.UTF-8
Narzędzia działające przy uruchomionym jak i bez systemd.

%package container
Summary:	Tools for container/VM management
Summary(pl.UTF-8):	Narzędzia do zarządzania kontenerami/wirtualnymi maszynami
License:	LGPL v2.1+
Group:		Base
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	curl-libs >= 7.32.0

%description container
Tools for container/VM management.

%description container -l pl.UTF-8
Narzędzia do zarządzania kontenerami/wirtualnymi maszynami.

%package journal-remote
Summary:	Tools for sending and receiving remote journal logs
Summary(pl.UTF-8):	Narzędzia do wysyłania i odbierania zdarzeń dziennika po sieci
License:	LGPL v2.1+
Group:		Base
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires:	curl-libs >= 7.32.0
Requires:	gnutls-libs >= 3.6.0
Requires:	libmicrohttpd >= 0.9.33
Provides:	group(systemd-journal-gateway)
Provides:	group(systemd-journal-remote)
Provides:	group(systemd-journal-upload)
Provides:	user(systemd-journal-gateway)
Provides:	user(systemd-journal-remote)
Provides:	user(systemd-journal-upload)
Obsoletes:	systemd-journal-gateway < 1:251.4-3
Conflicts:	systemd < 1:206-3

%description journal-remote
Tools for sending and receiving remote journal logs.

%description journal-remote -l pl.UTF-8
Narzędzia do wysyłania i odbierania zdarzeń dziennika po sieci.

%package homed
Summary:	systemd home area/user account manager
Summary(pl.UTF-8):	Zarządca obszarów domowych/kont użytkownika dla systemd
Group:		Base
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	libfdisk >= 2.32

%description homed
systemd-homed is a system service that may be used to create, remove,
change or inspect home areas (directories and network mounts and real
or loopback block devices with a filesystem, optionally encrypted).

%description homed -l pl.UTF-8
systemd-homed to usługa systemowa służąca do tworzenia, usuwania,
zmiany lub dozorowania obszarów domowych (katalogów, montowań
sieciowych oraz prawdziwych lub symulowanych urządzeń blokowych z
systemami plików, opcjonalnie szyfrowanymi).

%package networkd
Summary:	systemd network manager
Summary(pl.UTF-8):	Zarządca sieci systemd
Group:		Base
Requires:	%{name} = %{epoch}:%{version}-%{release}
Suggests:	%{name}-resolved = %{epoch}:%{version}-%{release}

%description networkd
systemd-networkd is a system service that manages networks. It detects
and configures network devices as they appear, as well as creating
virtual network devices.

%description networkd -l pl.UTF-8
systemd-networkd to usługa systemowa zarządzająca siecią. Wykrywa i
konfiguruje interfejsy sieciowe gdy się pojawiają, a także tworzy
wirtualne urządzenia sieciowe.

%package oomd
Summary:	systemd userspace OOM killer service
Summary(pl.UTF-8):	Usługa systemd zabójcy OOM w przestrzeni użytkownika
Group:		Base
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	uname(release) >= 4.20

%description oomd
systemd-oomd is a system service which monitors resource contention
for selected parts of the unit hierarchy using the PSI information
reported by the kernel, and kills processes when memory or swap
pressure is above configured limits.

%description oomd -l pl.UTF-8
systemd-oomd to usługa systemowa monitorująca wykorzystanie zasobów
dla wybranych części hierarchii jednostek przy użyciu informacji PSI,
zgłaszanych przez jądro, oraz zabijająca procesy, kiedy niedobór
pamięci lub przestrzeni wymiany jest powyżej skonfigurowanych limitów.

%package portabled
Summary:	systemd portable service images service
Summary(pl.UTF-8):	Usługa systemd do obrazów usług przenośnych
Group:		Base
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description portabled
systemd-portabled is a system service that may be used to attach,
detach and inspect portable service images.

%description portabled -l pl.UTF-8
systemd-portabled to usługa systemowa służąca do podłączania,
odłączania i badania obrazów usług przenośnych.

%package repart
Summary:	systemd service to automatically grow and add partitions
Summary(pl.UTF-8):	Usługa systemd do automatycznego powiększania lub dodawania partycji
Group:		Base
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	libfdisk >= 2.32

%description repart
systemd-repart grows and adds partitions to a partition table, based
on the configuration files.

%description repart -l pl.UTF-8
systemd-repart powiększa i dodaje partycje do tablicy partycji w
oparciu o pliki konfiguracyjne.

%package resolved
Summary:	systemd network name resolution manager
Summary(pl.UTF-8):	Zarządca rozwiązywania nazw sieciowych systemd
Group:		Base
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	gnutls-libs >= 3.6.0

%description resolved
systemd-resolved is a system service that manages network name
resolution. It implements a caching DNS stub resolver and an LLMNR
resolver and responder.

It also generates /run/systemd/resolve/resolv.conf for compatibility
which may be symlinked from /etc/resolv.conf.

%description resolved -l pl.UTF-8
systemd-resolved to usługa systemowa zarządzająca rozwiązywaniem nazw
sieciowych. Implementuje keszujący resolver DNS oraz resolver i
responder LLMNR.

Generuje także dla zgodności plik /run/systemd/resolve/resolv.conf,
który można użyć do dowiązania symbolicznego z /etc/resolv.conf.

%package sysupdate
Summary:	systemd service for automatic system update
Summary(pl.UTF-8):	Usługa systemd do automatycznych aktualizacji systemu
Group:		Base
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description sysupdate
systemd service for automatic system update.

%description sysupdate -l pl.UTF-8
Usługa systemd do automatycznych aktualizacji systemu.

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

%package ukify
Summary:	Tool for combining kernel and initrd into Unified Kernel Image (UKI)
Summary(pl.UTF-8):	Narzędzie do łączenia jądra oraz initrd w Unified Kernel Image (UKI)
Group:		Base
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	python3-modules >= 1:3.9

%description ukify
Tool for combining kernel and initrd into Unified Kernel Image (UKI).

%description ukify -l pl.UTF-8
Narzędzie do łączenia jądra oraz initrd w Unified Kernel Image (UKI).

%package libs
Summary:	Shared systemd libraries
Summary(pl.UTF-8):	Biblioteki współdzielone systemd
Group:		Libraries
Requires:	libgcrypt >= 1.4.5
Requires:	libseccomp >= 2.4.0
%{?with_selinux:Requires:	libselinux >= 2.6}
Requires:	lz4-libs >= 1:1.3.0
Requires:	zstd >= 1.4.0
Obsoletes:	nss_myhostname < 0.4

%description libs
Shared systemd libraries.

%description libs -l pl.UTF-8
Biblioteki współdzielone systemd.

%package devel
Summary:	Header files for systemd libraries
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotek systemd
Group:		Development/Libraries
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}
Requires:	%{name}-units = %{epoch}:%{version}-%{release}
Obsoletes:	systemd-static < 1:205

%description devel
Header files for systemd libraries.

%description devel -l pl.UTF-8
Pliki nagłówkowe bibliotek systemd.

%package -n bash-completion-systemd
Summary:	bash-completion for systemd
Summary(pl.UTF-8):	Bashowe dopełnianie składni dla systemd
Group:		Applications/Shells
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	bash-completion >= 1:2.0
Obsoletes:	bash-completion-elogind
BuildArch:	noarch

%description -n bash-completion-systemd
bash-completion for systemd.

%description -n bash-completion-systemd -l pl.UTF-8
Bashowe dopełnianie składni dla systemd.

%package -n zsh-completion-systemd
Summary:	zsh completion for systemd commands
Summary(pl.UTF-8):	Uzupełnianie parametrów w zsh dla poleceń systemd
Group:		Applications/Shells
Requires:	%{name} = %{epoch}:%{version}-%{release}
Obsoletes:	zsh-completion-elogind
BuildArch:	noarch

%description -n zsh-completion-systemd
zsh completion for systemd commands.

%description -n zsh-completion-systemd -l pl.UTF-8
Uzupełnianie parametrów w zsh dla poleceń systemd.

%package -n udev
Summary:	Device manager for the Linux 2.6 kernel series
Summary(pl.UTF-8):	Zarządca urządzeń dla Linuksa 2.6
Group:		Base
Requires:	udev-core = %{epoch}:%{version}-%{release}
Provides:	dev = 3.5.0
Obsoletes:	dev < 3.5
Obsoletes:	hotplug < 2005
Obsoletes:	hotplug-digicam < 2005
Obsoletes:	hotplug-input < 2005
Obsoletes:	hotplug-isapnp < 2005
Obsoletes:	hotplug-net < 2005
Obsoletes:	hotplug-pci < 2005
Obsoletes:	udev-dev < 032
Obsoletes:	udev-extras < 20090628
Obsoletes:	udev-tools < 1:125-2

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
Requires:	kmod >= 15
Requires:	libblkid >= 2.24
%{?with_selinux:Requires:	libselinux >= 2.6}
Requires:	setup >= 2.10.1
Requires:	systemd-libs = %{epoch}:%{version}-%{release}
Requires:	udev-libs = %{epoch}:%{version}-%{release}
Requires:	uname(release) >= %{min_kernel}
Obsoletes:	udev-compat < 1:182-1
Obsoletes:	udev-dbus < 027
Obsoletes:	udev-digicam < 1:079-2
Obsoletes:	udev-initramfs < 1:182-5
Obsoletes:	udev-initrd < 1:198-1
Conflicts:	geninitrd < 12639
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
Obsoletes:	udev-apidocs < 1:221-1
Obsoletes:	udev-static < 1:205

%description -n udev-devel
Header file for libudev library.

%description -n udev-devel -l pl.UTF-8
Plik nagłówkowy biblioteki libudev.

%package -n bash-completion-udev
Summary:	bash-completion for udev
Summary(pl.UTF-8):	Bashowe dopełnianie składni dla udev
Group:		Applications/Shells
Requires:	bash-completion >= 1:2.0
Requires:	udev = %{epoch}:%{version}-%{release}
BuildArch:	noarch

%description -n bash-completion-udev
bash-completion for udev.

%description -n bash-completion-udev -l pl.UTF-8
Bashowe dopełnianie składni dla udev.

%package -n zsh-completion-udev
Summary:	zsh completion for udev commands
Summary(pl.UTF-8):	Uzupełnianie parametrów w zsh dla poleceń udev
Group:		Applications/Shells
Requires:	%{name} = %{epoch}:%{version}-%{release}
BuildArch:	noarch

%description -n zsh-completion-udev
zsh completion for udev commands.

%description -n zsh-completion-udev -l pl.UTF-8
Uzupełnianie parametrów w zsh dla poleceń udev.

%package -n rpm-macros-systemd
Summary:	RPM macros that define paths and scriptlets related to systemd
Summary(pl.UTF-8):	Makra RPM-a definiujące ścieżki i skryptlety związane z systemd
Group:		Development/Building
BuildArch:	noarch

%description -n rpm-macros-systemd
RPM macros that define paths and scriptlets related to systemd.

%description -n rpm-macros-systemd -l pl.UTF-8
Makra RPM-a definiujące ścieżki i skryptlety związane z systemd.

%prep
%setup -q -n systemd-stable-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
# rejected upstream (do not disable!)
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p1

cp -p %{SOURCE2} src/systemd_booted.c

grep -rlZ -0 '#!/usr/bin/env bash' . | xargs -0 sed -i -e 's,#!/usr/bin/env bash,#!/bin/bash,g'

%{__sed} -i -e '1 s,#!.*env python3,#!%{__python3},' src/ukify/ukify.py

%build
%meson build \
	-Dadm-gid=3 \
	-Daudio-gid=23 \
	-Dcdrom-gid=27 \
	-Ddialout-gid=16 \
	-Ddisk-gid=6 \
	-Dinput-gid=182 \
	-Dkmem-gid=9 \
	-Dkvm-gid=160 \
	-Dlp-gid=7 \
	-Dsgx-gid=344 \
	-Dtape-gid=68 \
	-Dusers-gid=1000 \
	-Dutmp-gid=22 \
	-Dvideo-gid=24 \
	-Dwheel-gid=10 \
	-Dsystemd-journal-gid=288 \
	-Dsystemd-network-uid=316 \
	-Dsystemd-resolve-uid=317 \
	-Dsystemd-timesync-uid=318 \
	-Dnobody-user="nobody" \
	-Dnobody-group="nogroup" \
	-Daudit=%{__true_false audit} \
	-Dbpf-framework=%{__true_false bpf} \
	-Ddefault-kill-user-processes=false \
	%{?debug:--buildtype=debug} \
	-Defi=%{__true_false efi} \
	-Dlibfido2=%{__true_false fido2} \
	-Dkexec-path=/sbin/kexec \
	-Dkmod-path=/sbin/kmod \
	-Dlibcryptsetup=%{__true_false cryptsetup} \
	-Dlibcryptsetup-plugins-dir=/usr/%{_lib}/cryptsetup \
	-Dlibidn2=true \
	-Dloadkeys-path=/usr/bin/loadkeys \
	-Dlz4=true \
	-Dman=true \
	-Dmicrohttpd=%{__true_false microhttpd} \
	-Dmount-path=/bin/mount \
	-Dntp-servers='0.pool.ntp.org 1.pool.ntp.org 2.pool.ntp.org 3.pool.ntp.org' \
	-Dpam=%{__true_false pam} \
	-Dqrencode=%{__true_false qrencode} \
	-Dquotacheck=true \
	-Dquotacheck-path=/sbin/quotacheck \
	-Dquotaon-path=/sbin/quotaon \
	-Drc-local=/etc/rc.d/rc.local \
	-Drootlibdir=/%{_lib} \
	-Drootprefix="" \
	-Dsbat-distro="%vendor" \
	-Dsbat-distro-pkgname="%name" \
	-Dsbat-distro-summary="%distribution" \
	-Dsbat-distro-url="https://git.pld-linux.org/?p=packages/systemd.git" \
	-Dsbat-distro-version="%version-%release" \
	-Dselinux=%{__true_false selinux} \
	-Dsetfont-path=/bin/setfont \
	-Dsplit-bin=true \
	-Dsplit-usr=true \
	-Dsulogin-path=/sbin/sulogin \
	-Dsysvinit-path=/etc/rc.d/init.d \
	-Dsysvrcnd-path=/etc/rc.d \
	-Dtpm2=%{__true_false tpm2} \
	-Dumount-path=/bin/umount \
	-Dxenctrl=%{__true_false xen}

%ninja_build -C build

%{__cc} %{rpmcppflags} %{rpmcflags} -o build/systemd_booted %{rpmldflags} src/systemd_booted.c -Lbuild -lsystemd

%{?with_tests:%ninja_test -C build}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/var/lib/{%{name}/{catalog,coredump},machines} \
	$RPM_BUILD_ROOT%{_rootsbindir} \
	$RPM_BUILD_ROOT%{_sysconfdir}/{modprobe.d,repart.d,systemd/{system,user}-preset,sysupdate.d} \
	$RPM_BUILD_ROOT%{systemduserunitdir}/sockets.target.wants \
	$RPM_BUILD_ROOT%{systemdunitdir}/{final,sound,system-update}.target.wants \
	$RPM_BUILD_ROOT%{systemdunitdir}/systemd-udevd.service.d \
	$RPM_BUILD_ROOT%{_prefix}/lib/{repart.d,systemd/system-environment-generators,sysupdate.d}

%ninja_install -C build

touch $RPM_BUILD_ROOT/var/lib/%{name}/random-seed

install -p -m755 build/systemd_booted $RPM_BUILD_ROOT/bin/systemd_booted

# target-pld.patch supplements
%{__rm} $RPM_BUILD_ROOT%{systemdunitdir}/sysinit.target.wants/sys-kernel-config.mount
ln -s %{systemdunitdir}/prefdm.service $RPM_BUILD_ROOT%{systemdunitdir}/graphical.target.wants/display-manager.service
ln -s prefdm.service $RPM_BUILD_ROOT%{systemdunitdir}/display-manager.service
ln -s rescue.service $RPM_BUILD_ROOT%{systemdunitdir}/single.service
ln -s %{systemdunitdir}/rc-local.service $RPM_BUILD_ROOT%{systemdunitdir}/multi-user.target.wants/rc-local.service

# compatibility symlinks to udevd binary
mv $RPM_BUILD_ROOT/lib/{systemd/systemd-,udev/}udevd
ln -s /lib/udev/udevd $RPM_BUILD_ROOT/lib/systemd/systemd-udevd
ln -s /lib/udev/udevd $RPM_BUILD_ROOT%{_rootsbindir}/udevd

# compat symlinks for "/ merged into /usr" programs
ln -s ../bin/udevadm $RPM_BUILD_ROOT%{_rootsbindir}
ln -s /lib/udev $RPM_BUILD_ROOT%{_prefix}/lib

# install custom udev rules from pld package
cp -a %{SOURCE101} $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d/40-alsa-restore.rules
cp -a %{SOURCE102} $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d/70-udev-pld.rules
cp -a %{SOURCE104} $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d/70-uinput.rules
cp -a %{SOURCE105} $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d/70-steam_controller.rules
cp -a %{SOURCE106} $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d/70-i2c.rules
%ifarch %{arm} aarch64
cp -a %{SOURCE107} $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d/70-raspberrypi.rules
%endif

# http://www.freedesktop.org/wiki/Software/systemd/PredictableNetworkInterfaceNames
ln -s /dev/null $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d/80-net-setup-link.rules

# install udev configs
cp -a %{SOURCE103} $RPM_BUILD_ROOT%{_sysconfdir}/udev/links.conf

# install udev executables (scripts, helpers, etc.)
install -p %{SOURCE110} $RPM_BUILD_ROOT/lib/udev/net_helper
install -p %{SOURCE111} $RPM_BUILD_ROOT%{_rootsbindir}/start_udev

# install misc udev stuff
cp -a %{SOURCE120} $RPM_BUILD_ROOT%{_sysconfdir}/modprobe.d/udev_blacklist.conf
cp -a %{SOURCE121} $RPM_BUILD_ROOT%{_sysconfdir}/modprobe.d/fbdev-blacklist.conf

:>$RPM_BUILD_ROOT%{_sysconfdir}/udev/hwdb.bin

%{__mv} $RPM_BUILD_ROOT%{_mandir}/man8/{systemd-,}udevd.8
echo ".so man8/udevd.8" >$RPM_BUILD_ROOT%{_mandir}/man8/systemd-udevd.8

# Main binary has been moved, but we don't want to break existing installs
ln -s ../lib/systemd/systemd $RPM_BUILD_ROOT/bin/systemd

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

# and remove mounting tmp on tmpfs by default
%{__rm} $RPM_BUILD_ROOT%{systemdunitdir}/local-fs.target.wants/tmp.mount

# add /tmp cleanup service
cp -p %{SOURCE14} $RPM_BUILD_ROOT%{systemdunitdir}/pld-clean-tmp.service
install -p %{SOURCE15} $RPM_BUILD_ROOT/lib/systemd/pld-clean-tmp
ln -s ../pld-clean-tmp.service $RPM_BUILD_ROOT%{systemdunitdir}/local-fs.target.wants

# Add inside container only SIGPWR handler which is used by lxc-stop
install -p %{SOURCE20} $RPM_BUILD_ROOT%{systemdunitdir}/sigpwr-container-shutdown.service
install -d $RPM_BUILD_ROOT%{systemdunitdir}/sigpwr.target.wants
ln -s ../sigpwr-container-shutdown.service $RPM_BUILD_ROOT%{systemdunitdir}/sigpwr.target.wants

# As of 207 the systemd-sysctl tool no longer natively reads the file /etc/sysctl.conf.
# If desired, the file should be symlinked from /etc/sysctl.d/99-sysctl.conf.
ln -s /etc/sysctl.conf $RPM_BUILD_ROOT/etc/sysctl.d/99-sysctl.conf

# Install rc-inetd replacement
cp -p %{SOURCE16} $RPM_BUILD_ROOT%{systemdunitdir}-generators/pld-rc-inetd-generator
cp -p %{SOURCE17} $RPM_BUILD_ROOT%{systemdunitdir}/rc-inetd.service

cp -p %{SOURCE18} $RPM_BUILD_ROOT%{_sysconfdir}/systemd/system-preset/default.preset

cp -p %{SOURCE19} $RPM_BUILD_ROOT%{systemdunitdir}/prefdm.service

# handled by rc-local sysv service, no need for generator
%{__rm} $RPM_BUILD_ROOT%{systemdunitdir}-generators/systemd-rc-local-generator \
	$RPM_BUILD_ROOT%{_mandir}/man8/systemd-rc-local-generator.8

# provided by rc-scripts
%{__rm} $RPM_BUILD_ROOT%{systemdunitdir}/rc-local.service \
	$RPM_BUILD_ROOT%{_mandir}/man8/rc-local.service.8

# Make sure these directories are properly owned:
#	- halt,kexec,poweroff,reboot: generic ones used by ConsoleKit-systemd,
#	- syslog _might_ be used by some syslog implementation (none for now),
#	- isn't dbus populated by dbus-systemd only (so to be moved there)?
install -d $RPM_BUILD_ROOT%{systemdunitdir}/{basic,dbus,halt,initrd,kexec,poweroff,reboot,shutdown,syslog}.target.wants

# Make sure the shutdown/sleep drop-in dirs exist
install -d $RPM_BUILD_ROOT%{_prefix}/lib/systemd/system-{shutdown,sleep}

# Create new-style configuration files so that we can ghost-own them
touch $RPM_BUILD_ROOT%{_sysconfdir}/{hostname,locale.conf,machine-id,machine-info,vconsole.conf}

# Install SysV conversion tool for systemd
install -p %{SOURCE1} $RPM_BUILD_ROOT%{_bindir}

# Create directory for service helper scripts
install -d $RPM_BUILD_ROOT/lib/systemd/pld-helpers.d

install -d $RPM_BUILD_ROOT/var/log
:> $RPM_BUILD_ROOT/var/log/btmp
:> $RPM_BUILD_ROOT/var/log/wtmp

%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 288 systemd-journal
%groupadd -g 316 systemd-network
%useradd -u 316 -g 316 -d /var/log/journal -s /bin/false -c "Systemd Network Management" systemd-network
%groupadd -g 317 systemd-resolve
%useradd -u 317 -g 317 -d /var/log/journal -s /bin/false -c "Systemd Resolver" systemd-resolve
%groupadd -g 318 systemd-timesync
%useradd -u 318 -g 318 -d /var/log/journal -s /bin/false -c "Systemd Time Synchronization" systemd-timesync
%groupadd -g 333 systemd-coredump
%useradd -u 333 -g 333 -d /var/log/journal -s /bin/false -c "Systemd Core Dumper" systemd-coredump
%groupadd -g 341 systemd-oom
%useradd -u 341 -g 341 -d /var/log/journal -s /bin/false -c "Systemd Userspace OOM Killer" systemd-oom

%post
/bin/systemd-machine-id-setup || :
/lib/systemd/systemd-random-seed save || :
/bin/systemctl --system daemon-reexec || :
/bin/journalctl --update-catalog || :
/bin/systemd-sysusers || :

%postun
if [ $1 -ge 1 ]; then
	/bin/systemctl --system daemon-reload || :
	/bin/systemctl try-restart systemd-logind.service || :
fi
if [ "$1" = "0" ]; then
	%userremove systemd-coredump
	%groupremove systemd-coredump
	%userremove systemd-network
	%groupremove systemd-network
	%userremove systemd-oom
	%groupremove systemd-oom
	%userremove systemd-resolve
	%groupremove systemd-resolve
	%userremove systemd-timesync
	%groupremove systemd-timesync
	%groupremove systemd-journal
fi

%triggerpostun -- systemd < 1:220-1
# systemd < 1:208-1
chgrp -R systemd-journal /var/log/journal
chmod g+s /var/log/journal
# systemd < 1:220-1
# https://bugs.freedesktop.org/show_bug.cgi?id=89202
/bin/getfacl -p /var/log/journal/$(cat /etc/machine-id) | grep -v '^#' | sort -u | /bin/setfacl -R --set-file=- /var/log/journal/$(cat /etc/machine-id) || :

%triggerpostun -- systemd-consoled < 1:232-1
if [ -f %{_sysconfdir}/vconsole.conf.rpmsave ]; then
	%{__mv} -f %{_sysconfdir}/vconsole.conf %{_sysconfdir}/vconsole.conf.rpmnew
	%{__mv} -f %{_sysconfdir}/vconsole.conf.rpmsave %{_sysconfdir}/vconsole.conf
fi

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%post units
if [ $1 -eq 1 ]; then
	# Try to read default runlevel from the old inittab if it exists
	runlevel=$(/bin/awk -F ':' '$3 == "initdefault" && $1 !~ "^#" { print $2 }' /etc/inittab 2>/dev/null)
	if [ -z "$runlevel" ] ; then
		target="%{systemdunitdir}/graphical.target"
	else
		target="%{systemdunitdir}/runlevel$runlevel.target"
	fi

	# And symlink what we found to the new-style default.target
	ln -s "$target" %{_sysconfdir}/systemd/system/default.target || :

	# Setup hostname if not yet done so
	if [ ! -s /etc/hostname ]; then
		HOSTNAME=
		[ -f /etc/sysconfig/network ] && . /etc/sysconfig/network
		if [ -n "$HOSTNAME" -a "$HOSTNAME" != "pldmachine" ]; then
			echo $HOSTNAME > /etc/hostname
			chmod 644 /etc/hostname
		fi
	fi

	# Enable the services we install by default.
	/bin/systemctl enable \
		network.service \
		remote-fs.target \
		systemd-udev-settle.service || :
fi

%preun units
if [ $1 -eq 0 ] ; then
	/bin/systemctl disable \
		network.service \
		remote-fs.target \
		systemd-udev-settle.service || :

	%{__rm} -f %{_sysconfdir}/systemd/system/default.target || :
fi

%postun units
if [ $1 -ge 1 ]; then
	/bin/systemctl daemon-reload || :
fi

%triggerpostun units -- systemd-units < 1:242
# systemd-units < 43-7
# Remove design fialures
%{__rm} -f %{_sysconfdir}/systemd/system/network.target.wants/ifcfg@*.service || :
%{__rm} -f %{_sysconfdir}/systemd/system/network.target.wants/network-post.service || :
%{__rm} -f %{_sysconfdir}/systemd/system/multi-user.target.wants/network-post.service || :
/bin/systemctl reenable network.service || :
# systemd-units < 1:183
/bin/systemctl --quiet enable systemd-udev-settle.service || :
%{__rm} -f /etc/systemd/system/basic.target.wants/udev-settle.service || :
# preserve renamed configs
if [ -f /etc/systemd/systemd-journald.conf.rpmsave ]; then
	%{__mv} /etc/systemd/journald.conf{,.rpmnew}
	%{__mv} -f /etc/systemd/systemd-journald.conf.rpmsave /etc/systemd/journald.conf
fi
if [ -f /etc/systemd/systemd-logind.conf.rpmsave ]; then
	%{__mv} /etc/systemd/logind.conf{,.rpmnew}
	%{__mv} -f /etc/systemd/systemd-logind.conf.rpmsave /etc/systemd/logind.conf
fi
# systemd-units < 1:187-3
if [ -f /etc/sysconfig/rpm ]; then
	. /etc/sysconfig/rpm
	if [ ${RPM_ENABLE_SYSTEMD_SERVICE:-yes} = no ]; then
		echo "disable *" >>%{_sysconfdir}/systemd/system-preset/default.preset
	fi
fi
# systemd-units < 1:208-9
# remove buggy symlink
if [ -L /etc/systemd/system/getty.target.wants/getty@.service ] ; then
	rm -f /etc/systemd/system/getty.target.wants/getty@.service || :
fi
# systemd-units < 1:242
if [ -L /var/lib/systemd/timesync ] ; then
	rm -f /var/lib/systemd/timesync || :
fi

%post inetd
%systemd_reload
# Do not change it to restart, we only want to start new services here
%systemd_service_start sockets.target

%postun inetd
%systemd_reload

%pre journal-remote
%groupadd -g 287 systemd-journal-gateway
%useradd -u 287 -g 287 -d /var/log/journal -s /bin/false -c "Systemd Journal Gateway" systemd-journal-gateway
%groupadd -g 319 systemd-journal-remote
%useradd -u 319 -g 319 -d /var/log/journal -s /bin/false -c "Systemd Journal Remote" systemd-journal-remote
%groupadd -g 320 systemd-journal-upload
%useradd -u 320 -g 320 -d /var/log/journal -s /bin/false -c "Systemd Journal Upload" systemd-journal-upload

%post journal-remote
%systemd_post systemd-journal-gatewayd.socket systemd-journal-gatewayd.service

%preun journal-remote
%systemd_preun systemd-journal-gatewayd.socket systemd-journal-gatewayd.service

%postun journal-remote
%systemd_reload

if [ "$1" = "0" ]; then
	%userremove systemd-journal-gateway
	%groupremove systemd-journal-gateway
	%userremove systemd-journal-remote
	%groupremove systemd-journal-remote
	%userremove systemd-journal-upload
	%groupremove systemd-journal-upload
fi

%post networkd
%systemd_post systemd-networkd.socket systemd-networkd.service

%preun networkd
%systemd_preun systemd-networkd.socket systemd-networkd.service

%postun networkd
%systemd_reload

%post resolved
%systemd_post systemd-resolved.service

%preun resolved
%systemd_preun systemd-resolved.service

%postun resolved
%systemd_reload

%triggerpostun -n udev-core -- dev
if [ "$2" = 0 ]; then
	# need to kill and restart udevd as after obsoleting dev package the
	# /dev tree will remain empty. umask is needed as otherwise udev will
	# create devices with strange permissions (udev bug probably)
	umask 000
	/sbin/start_udev || exit 0
fi

%triggerpostun -n udev-core -- udev < 165
# udev < 108
%{__sed} -i -e 's#IMPORT{program}="/sbin/#IMPORT{program}="#g' /etc/udev/rules.d/*.rules
%if "%{_lib}" != "lib"
%{__sed} -i -e 's#/%{_lib}/udev/#/lib/udev/#g' /etc/udev/rules.d/*.rules
%endif

# udev < 165
/bin/udevadm info --convert-db

%post -n udev-core
/bin/udevadm hwdb --update || :
if [ $1 -gt 1 ]; then
	if [ ! -x /bin/systemd_booted ] || ! /bin/systemd_booted; then
		if grep -qs devtmpfs /proc/mounts && [ -n "$(pidof udevd)" ]; then
			/bin/udevadm control --exit
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

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc docs/{AUTOMATIC_BOOT_ASSESSMENT,BLOCK_DEVICE_LOCKING,BOOT_LOADER_INTERFACE,BOOT_LOADER_SPECIFICATION,DISTRO_PORTING,ENVIRONMENT,GROUP_RECORD,PREDICTABLE_INTERFACE_NAMES,TRANSIENT-SETTINGS,UIDS-GIDS,USER_GROUP_API,USER_RECORD}.md NEWS README TODO
%{_datadir}/dbus-1/interfaces/org.freedesktop.LogControl1.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.hostname1.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.locale1.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.login1.*.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.systemd1.*.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.timedate1.xml
%{_datadir}/dbus-1/system.d/org.freedesktop.hostname1.conf
%{_datadir}/dbus-1/system.d/org.freedesktop.locale1.conf
%{_datadir}/dbus-1/system.d/org.freedesktop.login1.conf
%{_datadir}/dbus-1/system.d/org.freedesktop.systemd1.conf
%{_datadir}/dbus-1/system.d/org.freedesktop.timedate1.conf
%{_datadir}/dbus-1/system.d/org.freedesktop.timesync1.conf
%attr(755,root,root) %{_sysconfdir}/X11/xinit/xinitrc.d/50-systemd-user.sh
%attr(444,root,root) %ghost %config(noreplace) %{_sysconfdir}/machine-id
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/hostname
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/locale.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/machine-info
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/vconsole.conf
%dir %{_sysconfdir}/kernel
%dir %{_sysconfdir}/kernel/install.d
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/systemd/coredump.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/systemd/journald.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/systemd/logind.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/systemd/pstore.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/systemd/sleep.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/systemd/system.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/systemd/timesyncd.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/systemd/user.conf
%dir %{_sysconfdir}/systemd/user

%config(noreplace) %verify(not md5 mtime size) /usr/lib/pam.d/systemd-user
/etc/xdg/systemd
%attr(755,root,root) /bin/journalctl
%attr(755,root,root) /bin/loginctl
%attr(755,root,root) /bin/systemd
%attr(755,root,root) /bin/systemd-ask-password
%attr(755,root,root) /bin/systemd-creds
%attr(755,root,root) /bin/systemd-escape
%attr(755,root,root) /bin/systemd-firstboot
%attr(755,root,root) /bin/systemd-inhibit
%attr(755,root,root) /bin/systemd-machine-id-setup
%attr(755,root,root) /bin/systemd-notify
%attr(755,root,root) /bin/systemd-sysext
%attr(755,root,root) /bin/systemd-sysusers
%attr(755,root,root) /bin/systemd-tty-ask-password-agent
%{?with_efi:%attr(755,root,root) %{_bindir}/bootctl}
%attr(755,root,root) %{_bindir}/busctl
%attr(755,root,root) %{_bindir}/coredumpctl
%attr(755,root,root) %{_bindir}/hostnamectl
%attr(755,root,root) %{_bindir}/kernel-install
%attr(755,root,root) %{_bindir}/localectl
%attr(755,root,root) %{_bindir}/systemd-ac-power
%attr(755,root,root) %{_bindir}/systemd-cat
%{?with_cryptsetup:%attr(755,root,root) %{_bindir}/systemd-cryptenroll}
%attr(755,root,root) %{_bindir}/systemd-delta
%attr(755,root,root) %{_bindir}/systemd-detect-virt
%attr(755,root,root) %{_bindir}/systemd-id128
%attr(755,root,root) %{_bindir}/systemd-mount
%attr(755,root,root) %{_bindir}/systemd-nspawn
%attr(755,root,root) %{_bindir}/systemd-path
%attr(755,root,root) %{_bindir}/systemd-resolve
%attr(755,root,root) %{_bindir}/systemd-run
%attr(755,root,root) %{_bindir}/systemd-socket-activate
%attr(755,root,root) %{_bindir}/systemd-stdio-bridge
%attr(755,root,root) %{_bindir}/systemd-umount
%attr(755,root,root) %{_bindir}/timedatectl
%attr(755,root,root) %{_bindir}/userdbctl
/lib/modprobe.d/systemd.conf
/lib/systemd/resolv.conf
%attr(755,root,root) /lib/systemd/pld-clean-tmp
%attr(755,root,root) /lib/systemd/systemd-backlight
%attr(755,root,root) /lib/systemd/systemd-binfmt
%{?with_efi:%attr(755,root,root) /lib/systemd/systemd-bless-boot}
%attr(755,root,root) /lib/systemd/systemd-boot-check-no-failures
%attr(755,root,root) /lib/systemd/systemd-cgroups-agent
%attr(755,root,root) /lib/systemd/systemd-coredump
%if %{with cryptsetup}
%attr(755,root,root) /lib/systemd/systemd-cryptsetup
%attr(755,root,root) /lib/systemd/systemd-integritysetup
%{?with_fido2:%attr(755,root,root) /usr/%{_lib}/cryptsetup/libcryptsetup-token-systemd-fido2.so}
%attr(755,root,root) /usr/%{_lib}/cryptsetup/libcryptsetup-token-systemd-pkcs11.so
%{?with_tpm2:%attr(755,root,root) /usr/%{_lib}/cryptsetup/libcryptsetup-token-systemd-tpm2.so}
%endif
%attr(755,root,root) /lib/systemd/systemd-fsck
%attr(755,root,root) /lib/systemd/systemd-growfs
%attr(755,root,root) /lib/systemd/systemd-hibernate-resume
%attr(755,root,root) /lib/systemd/systemd-hostnamed
%attr(755,root,root) /lib/systemd/systemd-initctl
%attr(755,root,root) /lib/systemd/systemd-journald
%attr(755,root,root) /lib/systemd/systemd-localed
%attr(755,root,root) /lib/systemd/systemd-logind
%attr(755,root,root) /lib/systemd/systemd-makefs
%if %{with efi} && %{with tpm2}
%attr(755,root,root) /lib/systemd/systemd-measure
%endif
%attr(755,root,root) /lib/systemd/systemd-modules-load
%if %{with efi} && %{with tpm2}
%attr(755,root,root) /lib/systemd/systemd-pcrphase
%endif
%attr(755,root,root) /lib/systemd/systemd-pstore
%attr(755,root,root) /lib/systemd/systemd-quotacheck
%attr(755,root,root) /lib/systemd/systemd-random-seed
%attr(755,root,root) /lib/systemd/systemd-remount-fs
%attr(755,root,root) /lib/systemd/systemd-reply-password
%attr(755,root,root) /lib/systemd/systemd-rfkill
%attr(755,root,root) /lib/systemd/systemd-shutdown
%attr(755,root,root) /lib/systemd/systemd-sleep
%attr(755,root,root) /lib/systemd/systemd-socket-proxyd
%attr(755,root,root) /lib/systemd/systemd-sulogin-shell
%attr(755,root,root) /lib/systemd/systemd-sysctl
%attr(755,root,root) /lib/systemd/systemd-sysroot-fstab-check
%attr(755,root,root) /lib/systemd/systemd-time-wait-sync
%attr(755,root,root) /lib/systemd/systemd-timedated
%attr(755,root,root) /lib/systemd/systemd-timesyncd
%attr(755,root,root) /lib/systemd/systemd-udevd
%attr(755,root,root) /lib/systemd/systemd-update-utmp
%attr(755,root,root) /lib/systemd/systemd-update-done
%attr(755,root,root) /lib/systemd/systemd-user-runtime-dir
%attr(755,root,root) /lib/systemd/systemd-user-sessions
%attr(755,root,root) /lib/systemd/systemd-userdbd
%attr(755,root,root) /lib/systemd/systemd-userwork
%attr(755,root,root) /lib/systemd/systemd-vconsole-setup
%attr(755,root,root) /lib/systemd/systemd-veritysetup
%attr(755,root,root) /lib/systemd/systemd-volatile-root
%attr(755,root,root) /lib/systemd/systemd-xdg-autostart-condition
%attr(755,root,root) /lib/systemd/systemd
%if %{with cryptsetup}
%attr(755,root,root) /lib/systemd/system-generators/systemd-cryptsetup-generator
%attr(755,root,root) /lib/systemd/system-generators/systemd-integritysetup-generator
%endif
%{?with_efi:%attr(755,root,root) /lib/systemd/system-generators/systemd-bless-boot-generator}
%attr(755,root,root) /lib/systemd/system-generators/systemd-debug-generator
%attr(755,root,root) /lib/systemd/system-generators/systemd-fstab-generator
%attr(755,root,root) /lib/systemd/system-generators/systemd-getty-generator
%attr(755,root,root) /lib/systemd/system-generators/systemd-gpt-auto-generator
%attr(755,root,root) /lib/systemd/system-generators/systemd-hibernate-resume-generator
%attr(755,root,root) /lib/systemd/system-generators/systemd-run-generator
%attr(755,root,root) /lib/systemd/system-generators/systemd-system-update-generator
%attr(755,root,root) /lib/systemd/system-generators/systemd-sysv-generator
%attr(755,root,root) /lib/systemd/system-generators/systemd-veritysetup-generator
%dir /lib/systemd/network
/lib/systemd/network/99-default.link
/lib/udev/rules.d/99-systemd.rules
%{_prefix}/lib/environment.d/99-environment.conf
%dir %{_prefix}/lib/kernel
%dir %{_prefix}/lib/kernel/install.d
%{_prefix}/lib/kernel/install.d/50-depmod.install
%{_prefix}/lib/kernel/install.d/90-loaderentry.install
%{_prefix}/lib/kernel/install.d/90-uki-copy.install
%if %{with efi}
%dir %{_prefix}/lib/systemd/boot
%dir %{_prefix}/lib/systemd/boot/efi
%ifarch %{ix86}
%{_prefix}/lib/systemd/boot/efi/linuxia32.efi.stub
%{_prefix}/lib/systemd/boot/efi/linuxia32.elf.stub
%{_prefix}/lib/systemd/boot/efi/systemd-bootia32.efi
%endif
%ifarch %{x8664} x32
%{_prefix}/lib/systemd/boot/efi/linuxx64.efi.stub
%{_prefix}/lib/systemd/boot/efi/linuxx64.elf.stub
%{_prefix}/lib/systemd/boot/efi/systemd-bootx64.efi
%endif
%ifarch aarch64
%{_prefix}/lib/systemd/boot/efi/linuxaa64.efi.stub
%{_prefix}/lib/systemd/boot/efi/linuxaa64.elf.stub
%{_prefix}/lib/systemd/boot/efi/systemd-bootaa64.efi
%endif
%endif
%{_prefix}/lib/systemd/catalog/systemd.catalog
%lang(be) %{_prefix}/lib/systemd/catalog/systemd.be.catalog
%lang(be) %{_prefix}/lib/systemd/catalog/systemd.be@latin.catalog
%lang(bg) %{_prefix}/lib/systemd/catalog/systemd.bg.catalog
%lang(da) %{_prefix}/lib/systemd/catalog/systemd.da.catalog
%lang(de) %{_prefix}/lib/systemd/catalog/systemd.de.catalog
%lang(fr) %{_prefix}/lib/systemd/catalog/systemd.fr.catalog
%lang(hr) %{_prefix}/lib/systemd/catalog/systemd.hr.catalog
%lang(hu) %{_prefix}/lib/systemd/catalog/systemd.hu.catalog
%lang(it) %{_prefix}/lib/systemd/catalog/systemd.it.catalog
%lang(ko) %{_prefix}/lib/systemd/catalog/systemd.ko.catalog
%lang(pl) %{_prefix}/lib/systemd/catalog/systemd.pl.catalog
%lang(pt_BR) %{_prefix}/lib/systemd/catalog/systemd.pt_BR.catalog
%lang(ru) %{_prefix}/lib/systemd/catalog/systemd.ru.catalog
%lang(sr) %{_prefix}/lib/systemd/catalog/systemd.sr.catalog
%lang(zh_CN) %{_prefix}/lib/systemd/catalog/systemd.zh_CN.catalog
%lang(zh_TW) %{_prefix}/lib/systemd/catalog/systemd.zh_TW.catalog
%dir %{_prefix}/lib/sysusers.d
%{_prefix}/lib/sysusers.d/basic.conf
%{_prefix}/lib/sysusers.d/systemd-coredump.conf
%{_prefix}/lib/sysusers.d/systemd-journal.conf
%{_prefix}/lib/sysusers.d/systemd-timesync.conf
%{_prefix}/lib/tmpfiles.d/credstore.conf
%{_prefix}/lib/tmpfiles.d/etc.conf
%{_prefix}/lib/tmpfiles.d/home.conf
%{_prefix}/lib/tmpfiles.d/journal-nocow.conf
%{_prefix}/lib/tmpfiles.d/legacy.conf
%{_prefix}/lib/tmpfiles.d/provision.conf
%{_prefix}/lib/tmpfiles.d/static-nodes-permissions.conf
%{_prefix}/lib/tmpfiles.d/systemd.conf
%{_prefix}/lib/tmpfiles.d/systemd-nologin.conf
%{_prefix}/lib/tmpfiles.d/systemd-nspawn.conf
%{_prefix}/lib/tmpfiles.d/systemd-pstore.conf
%{_prefix}/lib/tmpfiles.d/systemd-tmp.conf
%{_prefix}/lib/tmpfiles.d/tmp.conf
%{_prefix}/lib/tmpfiles.d/var.conf
%{_prefix}/lib/tmpfiles.d/x11.conf
%{_prefix}/lib/sysctl.d/50-coredump.conf
# if cc.sizeof('long') > 4
%ifarch %{x8664} aarch64
%{_prefix}/lib/sysctl.d/50-pid-max.conf
%endif
%{_datadir}/dbus-1/services/org.freedesktop.systemd1.service
%{_datadir}/dbus-1/system-services/org.freedesktop.hostname1.service
%{_datadir}/dbus-1/system-services/org.freedesktop.locale1.service
%{_datadir}/dbus-1/system-services/org.freedesktop.login1.service
%{_datadir}/dbus-1/system-services/org.freedesktop.systemd1.service
%{_datadir}/dbus-1/system-services/org.freedesktop.timedate1.service
%{_datadir}/dbus-1/system-services/org.freedesktop.timesync1.service
%{_datadir}/polkit-1/actions/org.freedesktop.hostname1.policy
%{_datadir}/polkit-1/actions/org.freedesktop.locale1.policy
%{_datadir}/polkit-1/actions/org.freedesktop.login1.policy
%{_datadir}/polkit-1/actions/org.freedesktop.systemd1.policy
%{_datadir}/polkit-1/actions/org.freedesktop.timedate1.policy
%{_datadir}/polkit-1/actions/org.freedesktop.timesync1.policy
%{_datadir}/polkit-1/rules.d/systemd-networkd.rules
%dir %{_datadir}/systemd
%{_datadir}/systemd/kbd-model-map
%{_datadir}/systemd/language-fallback-map
%{_datadir}/factory/etc/issue
%{_datadir}/factory/etc/locale.conf
%{_datadir}/factory/etc/nsswitch.conf
%{_datadir}/factory/etc/pam.d/other
%{_datadir}/factory/etc/pam.d/system-auth
%{?with_efi:%{_mandir}/man1/bootctl.1*}
%{_mandir}/man1/busctl.1*
%{_mandir}/man1/coredumpctl.1*
%{_mandir}/man1/hostnamectl.1*
%{_mandir}/man1/journalctl.1*
%{_mandir}/man1/localectl.1*
%{_mandir}/man1/loginctl.1*
%{_mandir}/man1/systemd.1*
%{_mandir}/man1/systemd-ac-power.1*
%{_mandir}/man1/systemd-ask-password.1*
%{_mandir}/man1/systemd-cat.1*
%{_mandir}/man1/systemd-creds.1*
%{?with_cryptsetup:%{_mandir}/man1/systemd-cryptenroll.1*}
%{_mandir}/man1/systemd-delta.1*
%{_mandir}/man1/systemd-detect-virt.1*
%{_mandir}/man1/systemd-dissect.1*
%{_mandir}/man1/systemd-escape.1*
%{_mandir}/man1/systemd-firstboot.1*
%{_mandir}/man1/systemd-firstboot.service.1*
%{_mandir}/man1/systemd-id128.1*
%{_mandir}/man1/systemd-inhibit.1*
%{_mandir}/man1/systemd-machine-id-setup.1*
%if %{with efi} && %{with tpm2}
%{_mandir}/man1/systemd-measure.1*
%endif
%{_mandir}/man1/systemd-mount.1*
%{_mandir}/man1/systemd-notify.1*
%{_mandir}/man1/systemd-nspawn.1*
%{_mandir}/man1/systemd-path.1*
%{_mandir}/man1/systemd-run.1*
%{_mandir}/man1/systemd-socket-activate.1*
%{_mandir}/man1/systemd-stdio-bridge.1*
%{_mandir}/man1/systemd-tty-ask-password-agent.1*
%{_mandir}/man1/systemd-umount.1*
%{_mandir}/man1/timedatectl.1*
%{_mandir}/man1/userdbctl.1*
%{_mandir}/man5/binfmt.d.5*
%{_mandir}/man5/coredump.conf.5*
%{_mandir}/man5/coredump.conf.d.5*
%{_mandir}/man5/dnssec-trust-anchors.d.5*
%{_mandir}/man5/extension-release.5*
%{_mandir}/man5/hostname.5*
%{_mandir}/man5/initrd-release.5*
%{_mandir}/man5/journald@.conf.5*
%{?with_efi:%{_mandir}/man5/loader.conf.5*}
%{_mandir}/man5/journald.conf.5*
%{_mandir}/man5/journald.conf.d.5*
%{_mandir}/man5/locale.conf.5*
%{_mandir}/man5/localtime.5*
%{_mandir}/man5/logind.conf.5*
%{_mandir}/man5/logind.conf.d.5*
%{_mandir}/man5/machine-id.5*
%{_mandir}/man5/machine-info.5*
%{_mandir}/man5/modules-load.d.5*
%{_mandir}/man5/org.freedesktop.LogControl1.5*
%{_mandir}/man5/org.freedesktop.hostname1.5*
%{_mandir}/man5/org.freedesktop.locale1.5*
%{_mandir}/man5/org.freedesktop.login1.5*
%{_mandir}/man5/org.freedesktop.systemd1.5*
%{_mandir}/man5/org.freedesktop.timedate1.5*
%{_mandir}/man5/os-release.5*
%{_mandir}/man5/pstore.conf.5*
%{_mandir}/man5/pstore.conf.d.5*
%{_mandir}/man5/sleep.conf.d.5*
%{_mandir}/man5/sysctl.d.5*
%{_mandir}/man5/system.conf.d.5*
%{_mandir}/man5/systemd.*.5*
%{_mandir}/man5/systemd-sleep.conf.5*
%{_mandir}/man5/systemd-system.conf.5*
%{_mandir}/man5/systemd-user.conf.5*
%{_mandir}/man5/systemd-user-runtime-dir.5*
%{_mandir}/man5/sysusers.d.5*
%{_mandir}/man5/timesyncd.conf.5*
%{_mandir}/man5/timesyncd.conf.d.5*
%{_mandir}/man5/user.conf.d.5*
%{_mandir}/man5/vconsole.conf.5*
%{_mandir}/man7/bootup.7*
%{_mandir}/man7/daemon.7*
%{_mandir}/man7/file-hierarchy.7*
%{_mandir}/man7/kernel-command-line.7*
%if %{with efi}
%ifarch %{ix86}
%{_mandir}/man7/linuxia32.efi.stub.7*
%endif
%ifarch %{x8664}
%{_mandir}/man7/linuxx64.efi.stub.7*
%endif
%ifarch aarch64
%{_mandir}/man7/linuxaa64.efi.stub.7*
%endif
%{_mandir}/man7/sd-boot.7*
%{_mandir}/man7/sd-stub.7*
%{_mandir}/man7/systemd-boot.7*
%{_mandir}/man7/systemd-stub.7*
%endif
%{_mandir}/man7/systemd.directives.7*
%{_mandir}/man7/systemd.environment-generator.7*
%{_mandir}/man7/systemd.generator.7*
%{_mandir}/man7/systemd.index.7*
%{_mandir}/man7/systemd.journal-fields.7*
%{_mandir}/man7/systemd.offline-updates.7*
%{_mandir}/man7/systemd.special.7*
%{_mandir}/man7/systemd.syntax.7*
%{_mandir}/man7/systemd.system-credentials.7*
%{_mandir}/man7/systemd.time.7*
%{_mandir}/man8/kernel-install.8*
%{_mandir}/man8/libnss_myhostname.so.2.8*
%{_mandir}/man8/libnss_mymachines.so.2.8*
%{_mandir}/man8/nss-myhostname.8*
%{_mandir}/man8/nss-mymachines.8*
%{_mandir}/man8/systemd-backlight.8*
%{_mandir}/man8/systemd-binfmt.8*
%if %{with efi}
%{_mandir}/man8/systemd-bless-boot.8*
%{_mandir}/man8/systemd-bless-boot-generator.8*
%endif
%{_mandir}/man8/systemd-boot-check-no-failures.8*
%{_mandir}/man8/systemd-coredump.8*
%if %{with cryptsetup}
%{_mandir}/man8/systemd-cryptsetup-generator.8*
%{_mandir}/man8/systemd-integritysetup-generator.8*
%endif
%{_mandir}/man8/systemd-debug-generator.8*
%{_mandir}/man8/systemd-fsck.8*
%{_mandir}/man8/systemd-fsck-usr.service.8*
%{_mandir}/man8/systemd-fstab-generator.8*
%{_mandir}/man8/systemd-getty-generator.8*
%{_mandir}/man8/systemd-gpt-auto-generator.8*
%{_mandir}/man8/systemd-growfs.8*
%{_mandir}/man8/systemd-growfs-root.service.8*
%{_mandir}/man8/systemd-growfs@.service.8*
%{_mandir}/man8/systemd-hibernate-resume-generator.8*
%{_mandir}/man8/systemd-hibernate-resume.8*
%{_mandir}/man8/systemd-hibernate-resume@.service.8*
%{_mandir}/man8/systemd-hostnamed.8*
%{_mandir}/man8/systemd-initctl.8*
%{_mandir}/man8/systemd-journald-dev-log.socket.8*
%{_mandir}/man8/systemd-journald-varlink@.socket.8*
%{_mandir}/man8/systemd-journald.8*
%{_mandir}/man8/systemd-journald@.service.8*
%{_mandir}/man8/systemd-journald@.socket.8*
%{_mandir}/man8/systemd-localed.8*
%{_mandir}/man8/systemd-logind.8*
%{_mandir}/man8/systemd-machine-id-commit.service.8*
%{_mandir}/man8/systemd-makefs.8*
%{_mandir}/man8/systemd-makefs@.service.8*
%{_mandir}/man8/systemd-mkswap@.service.8*
%{_mandir}/man8/systemd-modules-load.8*
%{_mandir}/man8/systemd-pstore.8*
%{_mandir}/man8/systemd-pstore.service.8*
%{_mandir}/man8/systemd-quotacheck.8*
%{_mandir}/man8/systemd-random-seed.8*
%{_mandir}/man8/systemd-remount-fs.8*
%{_mandir}/man8/systemd-rfkill.8*
%{_mandir}/man8/systemd-rfkill.service.8*
%{_mandir}/man8/systemd-run-generator.8*
%{_mandir}/man8/systemd-shutdown.8*
%{_mandir}/man8/systemd-sleep.8*
%{_mandir}/man8/systemd-socket-proxyd.8*
%{_mandir}/man8/systemd-sysctl.8*
%{_mandir}/man8/systemd-sysext.8*
%{_mandir}/man8/systemd-system-update-generator.8*
%{_mandir}/man8/systemd-sysusers.8*
%{_mandir}/man8/systemd-sysusers.service.8*
%{_mandir}/man8/systemd-sysv-generator.8*
%{_mandir}/man8/systemd-time-wait-sync.8*
%{_mandir}/man8/systemd-timedated.8*
%{_mandir}/man8/systemd-timesyncd.8*
%{_mandir}/man8/systemd-timesyncd.service.8*
%{_mandir}/man8/systemd-udevd.8*
%{_mandir}/man8/systemd-update-done.8*
%{_mandir}/man8/systemd-update-done.service.8*
%{_mandir}/man8/systemd-update-utmp.8*
%{_mandir}/man8/systemd-user-sessions.8*
%{_mandir}/man8/systemd-userdbd.8*
%{_mandir}/man8/systemd-vconsole-setup.8*
%{_mandir}/man8/systemd-veritysetup.8*
%{_mandir}/man8/systemd-veritysetup-generator.8*
%{_mandir}/man8/systemd-veritysetup@.service.8*
%{_mandir}/man8/systemd-volatile-root.8*
%{_mandir}/man8/systemd-volatile-root.service.8*
%{_mandir}/man8/systemd-xdg-autostart-generator.8*
%attr(700,root,root) %dir /var/lib/machines
%dir /var/lib/%{name}
%dir /var/lib/%{name}/coredump
%dir /var/lib/%{name}/catalog
%attr(640,root,root) %ghost /var/lib/%{name}/random-seed
%attr(600,root,utmp) %ghost /var/log/btmp
%attr(664,root,utmp) %ghost /var/log/wtmp
%attr(2755,root,systemd-journal) %dir /var/log/journal
%attr(2755,root,systemd-journal) %dir /var/log/journal/remote

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
%{_mandir}/man1/init.1*
%if %{with cryptsetup}
%{_mandir}/man5/crypttab.5*
%{_mandir}/man5/integritytab.5*
%{_mandir}/man5/veritytab.5*
%endif
%{_mandir}/man8/halt.8*
%{_mandir}/man8/poweroff.8*
%{_mandir}/man8/reboot.8*
%{_mandir}/man8/runlevel.8*
%{_mandir}/man8/shutdown.8*
%{_mandir}/man8/telinit.8*

%files sysv-compat
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/systemd-sysv-convert

%files units
%defattr(644,root,root,755)
%dir %{_sysconfdir}/binfmt.d
%dir %{_sysconfdir}/modules-load.d
%config(noreplace,missingok) %verify(not md5 mtime size) %{_sysconfdir}/modules-load.d/modules.conf
%dir %{_sysconfdir}/sysctl.d
%{_sysconfdir}/sysctl.d/99-sysctl.conf
%dir %{_sysconfdir}/systemd
%dir %{_sysconfdir}/systemd/system
%dir %{_sysconfdir}/systemd/system-preset
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/systemd/system-preset/default.preset
%dir %{_sysconfdir}/systemd/user-preset
%dir %{_sysconfdir}/tmpfiles.d
%dir %{_prefix}/lib/binfmt.d
%dir %{_prefix}/lib/environment.d
%dir %{_prefix}/lib/modules-load.d
%dir %{_prefix}/lib/sysctl.d
%{_prefix}/lib/sysctl.d/50-default.conf
%dir %{_prefix}/lib/systemd
%dir %{_prefix}/lib/systemd/catalog
%dir %{_prefix}/lib/systemd/system-shutdown
%dir %{_prefix}/lib/systemd/system-sleep
%dir %{_prefix}/lib/systemd/user
%{_prefix}/lib/systemd/user/app.slice
%{_prefix}/lib/systemd/user/background.slice
%{_prefix}/lib/systemd/user/basic.target
%{_prefix}/lib/systemd/user/bluetooth.target
%{_prefix}/lib/systemd/user/default.target
%{_prefix}/lib/systemd/user/exit.target
%{_prefix}/lib/systemd/user/paths.target
%{_prefix}/lib/systemd/user/printer.target
%{_prefix}/lib/systemd/user/session.slice
%{_prefix}/lib/systemd/user/shutdown.target
%{_prefix}/lib/systemd/user/smartcard.target
%{_prefix}/lib/systemd/user/sockets.target
%{_prefix}/lib/systemd/user/sound.target
%{_prefix}/lib/systemd/user/systemd-tmpfiles-clean.service
%{_prefix}/lib/systemd/user/systemd-tmpfiles-clean.timer
%{_prefix}/lib/systemd/user/systemd-tmpfiles-setup.service
%{_prefix}/lib/systemd/user/timers.target
%{_prefix}/lib/systemd/user/systemd-exit.service
%{_prefix}/lib/systemd/user/xdg-desktop-autostart.target
%dir %{_prefix}/lib/systemd/user-generators
%attr(755,root,root) %{_prefix}/lib/systemd/user-generators/systemd-xdg-autostart-generator
%dir %{_prefix}/lib/systemd/user-environment-generators
%attr(755,root,root) %{_prefix}/lib/systemd/user-environment-generators/30-systemd-environment-d-generator
%dir %{_prefix}/lib/systemd/user-preset
%{_prefix}/lib/systemd/user-preset/90-systemd.preset
%dir %{_prefix}/lib/systemd/system-environment-generators
%dir /lib/systemd/ntp-units.d
/lib/systemd/ntp-units.d/80-systemd-timesync.list
%dir /lib/systemd/pld-helpers.d
%dir /lib/systemd/system-generators
%dir /lib/systemd/system-preset
/lib/systemd/system-preset/90-systemd.preset
%dir /lib/systemd/system-sleep
%dir /lib/systemd/system-shutdown
%attr(755,root,root) /lib/systemd/systemd-update-helper
%attr(755,root,root) /bin/systemctl
%attr(755,root,root) /bin/systemd-tmpfiles
%attr(755,root,root) /bin/systemd_booted
%{_mandir}/man1/systemctl.1*
%{_mandir}/man5/tmpfiles.d.5*
%{_mandir}/man5/environment.d.5*
%{_mandir}/man8/systemd-tmpfiles.8*

%{systemdunitdir}/dev-hugepages.mount
%{systemdunitdir}/dev-mqueue.mount
%{systemdunitdir}/initrd-root-device.target
%{systemdunitdir}/proc-sys-fs-binfmt_misc.automount
%{systemdunitdir}/proc-sys-fs-binfmt_misc.mount
%{systemdunitdir}/sockets.target.wants/systemd-coredump.socket
%{systemdunitdir}/sys-fs-fuse-connections.mount
%{systemdunitdir}/sys-kernel-config.mount
%{systemdunitdir}/sys-kernel-debug.mount
%{systemdunitdir}/sys-kernel-tracing.mount
%{systemdunitdir}/systemd-coredump@.service
%{systemdunitdir}/systemd-coredump.socket
%{systemdunitdir}/systemd-exit.service
%{systemdunitdir}/systemd-pstore.service
%{systemdunitdir}/systemd-rfkill.socket
%{systemdunitdir}/tmp.mount
%{systemdunitdir}/var-lock.mount
%{systemdunitdir}/var-run.mount
%{systemdunitdir}/systemd-ask-password-console.path
%{systemdunitdir}/systemd-ask-password-wall.path
%{systemdunitdir}/allowlogin.service
%{systemdunitdir}/autovt@.service
%{systemdunitdir}/console-getty.service
%{systemdunitdir}/console.service
%{systemdunitdir}/container-getty@.service
%{systemdunitdir}/cpusets.service
%{systemdunitdir}/dbus-org.freedesktop.hostname1.service
%{systemdunitdir}/dbus-org.freedesktop.locale1.service
%{systemdunitdir}/dbus-org.freedesktop.login1.service
%{systemdunitdir}/dbus-org.freedesktop.timedate1.service
%{systemdunitdir}/debug-shell.service
%{systemdunitdir}/display-manager.service
%{systemdunitdir}/emergency.service
%{systemdunitdir}/getty@.service
%{systemdunitdir}/initrd-cleanup.service
%{systemdunitdir}/initrd-parse-etc.service
%{systemdunitdir}/initrd-switch-root.service
%{systemdunitdir}/initrd-udevadm-cleanup-db.service
%{systemdunitdir}/killall.service
%{systemdunitdir}/kmod-static-nodes.service
%{systemdunitdir}/ldconfig.service
%{systemdunitdir}/modprobe@.service
%{systemdunitdir}/netfs.service
%{systemdunitdir}/network.service
%{systemdunitdir}/pld-clean-tmp.service
%{systemdunitdir}/prefdm.service
%{systemdunitdir}/quotaon.service
%{systemdunitdir}/random.service
%{systemdunitdir}/rescue.service
%{systemdunitdir}/serial-getty@.service
%{systemdunitdir}/single.service
%{systemdunitdir}/sigpwr-container-shutdown.service
%{systemdunitdir}/suspend-then-hibernate.target
%{systemdunitdir}/sys-kernel-config.service
%{systemdunitdir}/system-update-cleanup.service
%{systemdunitdir}/system-update-pre.target
%{systemdunitdir}/systemd-ask-password-console.service
%{systemdunitdir}/systemd-ask-password-wall.service
%{systemdunitdir}/systemd-backlight@.service
%{systemdunitdir}/systemd-binfmt.service
%if %{with efi}
%{systemdunitdir}/systemd-bless-boot.service
%{systemdunitdir}/systemd-boot-random-seed.service
%{systemdunitdir}/systemd-boot-update.service
%endif
%{systemdunitdir}/systemd-boot-check-no-failures.service
%{systemdunitdir}/systemd-firstboot.service
%{systemdunitdir}/systemd-fsck-root.service
%{systemdunitdir}/systemd-fsck@.service
%{systemdunitdir}/systemd-growfs-root.service
%{systemdunitdir}/systemd-growfs@.service
%{systemdunitdir}/systemd-halt.service
%{systemdunitdir}/systemd-hibernate-resume@.service
%{systemdunitdir}/systemd-hibernate.service
%{systemdunitdir}/systemd-hostnamed.service
%{systemdunitdir}/systemd-hwdb-update.service
%{systemdunitdir}/systemd-hybrid-sleep.service
%{systemdunitdir}/systemd-initctl.service
%{systemdunitdir}/systemd-journal-catalog-update.service
%{systemdunitdir}/systemd-journal-flush.service
%{systemdunitdir}/systemd-journald.service
%{systemdunitdir}/systemd-journald@.service
%{systemdunitdir}/systemd-kexec.service
%{systemdunitdir}/systemd-localed.service
%{systemdunitdir}/systemd-logind.service
%{systemdunitdir}/systemd-machine-id-commit.service
%{systemdunitdir}/systemd-modules-load.service
%{systemdunitdir}/systemd-nspawn@.service
%if %{with efi} && %{with tpm2}
%{systemdunitdir}/systemd-pcrfs-root.service
%{systemdunitdir}/systemd-pcrfs@.service
%{systemdunitdir}/systemd-pcrmachine.service
%{systemdunitdir}/systemd-pcrphase-initrd.service
%{systemdunitdir}/systemd-pcrphase-sysinit.service
%{systemdunitdir}/systemd-pcrphase.service
%endif
%{systemdunitdir}/systemd-poweroff.service
%{systemdunitdir}/systemd-quotacheck.service
%{systemdunitdir}/systemd-random-seed.service
%{systemdunitdir}/systemd-reboot.service
%{systemdunitdir}/systemd-remount-fs.service
%{systemdunitdir}/systemd-rfkill.service
%{systemdunitdir}/systemd-suspend.service
%{systemdunitdir}/systemd-suspend-then-hibernate.service
%{systemdunitdir}/systemd-sysctl.service
%{systemdunitdir}/systemd-sysext.service
%{systemdunitdir}/systemd-sysusers.service
%{systemdunitdir}/systemd-time-wait-sync.service
%{systemdunitdir}/systemd-timedated.service
%{systemdunitdir}/systemd-timesyncd.service
%{systemdunitdir}/systemd-tmpfiles-clean.service
%{systemdunitdir}/systemd-tmpfiles-setup-dev.service
%{systemdunitdir}/systemd-tmpfiles-setup.service
%{systemdunitdir}/systemd-udev-settle.service
%{systemdunitdir}/systemd-udev-trigger.service
%{systemdunitdir}/systemd-udevd.service
%dir %{systemdunitdir}/systemd-udevd.service.d
%{systemdunitdir}/systemd-update-done.service
%{systemdunitdir}/systemd-update-utmp-runlevel.service
%{systemdunitdir}/systemd-update-utmp.service
%{systemdunitdir}/systemd-user-sessions.service
%{systemdunitdir}/systemd-userdbd.service
%{systemdunitdir}/systemd-userdbd.socket
%{systemdunitdir}/systemd-vconsole-setup.service
%{systemdunitdir}/systemd-volatile-root.service
%{systemdunitdir}/user@.service
%dir %{systemdunitdir}/user@.service.d
%{systemdunitdir}/user@.service.d/10-login-barrier.conf
%dir %{systemdunitdir}/user@0.service.d
%{systemdunitdir}/user@0.service.d/10-login-barrier.conf
%{systemdunitdir}/machine.slice
#%{systemdunitdir}/system.slice
%{?with_cryptsetup:%{systemdunitdir}/system-systemd\x2dcryptsetup.slice}
%dir %{systemdunitdir}/user-.slice.d
%{systemdunitdir}/user-.slice.d/10-defaults.conf
%{systemdunitdir}/user-runtime-dir@.service
%{systemdunitdir}/user.slice
%exclude %{systemdunitdir}/rc-inetd.service
%{systemdunitdir}/syslog.socket
%{systemdunitdir}/systemd-initctl.socket
%{systemdunitdir}/systemd-journald-audit.socket
%{systemdunitdir}/systemd-journald-dev-log.socket
%{systemdunitdir}/systemd-journald-varlink@.socket
%{systemdunitdir}/systemd-journald.socket
%{systemdunitdir}/systemd-journald@.socket
%{systemdunitdir}/systemd-udevd-control.socket
%{systemdunitdir}/systemd-udevd-kernel.socket
%{systemdunitdir}/basic.target
%{systemdunitdir}/blockdev@.target
%{systemdunitdir}/bluetooth.target
%{systemdunitdir}/boot-complete.target
%if %{with cryptsetup}
%{systemdunitdir}/cryptsetup-pre.target
%{systemdunitdir}/cryptsetup.target
%{systemdunitdir}/integritysetup-pre.target
%{systemdunitdir}/integritysetup.target
%{systemdunitdir}/veritysetup-pre.target
%{systemdunitdir}/veritysetup.target
%endif
%{systemdunitdir}/ctrl-alt-del.target
%{systemdunitdir}/default.target
%{systemdunitdir}/emergency.target
%{systemdunitdir}/exit.target
%{systemdunitdir}/factory-reset.target
%{systemdunitdir}/final.target
%{systemdunitdir}/first-boot-complete.target
%{systemdunitdir}/getty.target
%{systemdunitdir}/getty-pre.target
%{systemdunitdir}/graphical.target
%{systemdunitdir}/halt.target
%{systemdunitdir}/hibernate.target
%{systemdunitdir}/hybrid-sleep.target
%{systemdunitdir}/initrd-fs.target
%{systemdunitdir}/initrd-root-fs.target
%{systemdunitdir}/initrd-switch-root.target
%{systemdunitdir}/initrd-usr-fs.target
%{systemdunitdir}/initrd.target
%{systemdunitdir}/kexec.target
%{systemdunitdir}/local-fs-pre.target
%{systemdunitdir}/local-fs.target
%{systemdunitdir}/multi-user.target
%{systemdunitdir}/network-online.target
%{systemdunitdir}/network-pre.target
%{systemdunitdir}/network.target
%{systemdunitdir}/nss-lookup.target
%{systemdunitdir}/nss-user-lookup.target
%{systemdunitdir}/paths.target
%{systemdunitdir}/poweroff.target
%{systemdunitdir}/printer.target
%{systemdunitdir}/reboot.target
%{systemdunitdir}/remote-fs-pre.target
%{systemdunitdir}/remote-fs.target
%if %{with cryptsetup}
%{systemdunitdir}/remote-cryptsetup.target
%{systemdunitdir}/remote-veritysetup.target
%endif
%{systemdunitdir}/rescue.target
%{systemdunitdir}/rpcbind.target
%{systemdunitdir}/runlevel0.target
%{systemdunitdir}/runlevel1.target
%{systemdunitdir}/runlevel2.target
%{systemdunitdir}/runlevel3.target
%{systemdunitdir}/runlevel4.target
%{systemdunitdir}/runlevel5.target
%{systemdunitdir}/runlevel6.target
%{systemdunitdir}/shutdown.target
%{systemdunitdir}/sigpwr.target
%{systemdunitdir}/sleep.target
%{systemdunitdir}/slices.target
%{systemdunitdir}/smartcard.target
%{systemdunitdir}/sockets.target
%{systemdunitdir}/sound.target
%{systemdunitdir}/suspend.target
%{systemdunitdir}/swap.target
%{systemdunitdir}/sysinit.target
%{systemdunitdir}/system-update.target
%{systemdunitdir}/time-set.target
%{systemdunitdir}/time-sync.target
%{systemdunitdir}/timers.target
%{systemdunitdir}/umount.target
%{systemdunitdir}/usb-gadget.target
%{systemdunitdir}/systemd-tmpfiles-clean.timer
%dir %{systemdunitdir}/basic.target.wants
%dir %{systemdunitdir}/dbus.target.wants
%dir %{systemdunitdir}/final.target.wants
%dir %{systemdunitdir}/graphical.target.wants
%dir %{systemdunitdir}/halt.target.wants
%dir %{systemdunitdir}/initrd.target.wants
%dir %{systemdunitdir}/initrd-root-device.target.wants
%dir %{systemdunitdir}/initrd-root-fs.target.wants
%dir %{systemdunitdir}/kexec.target.wants
%dir %{systemdunitdir}/local-fs.target.wants
%dir %{systemdunitdir}/multi-user.target.wants
%dir %{systemdunitdir}/poweroff.target.wants
%dir %{systemdunitdir}/reboot.target.wants
%dir %{systemdunitdir}/remote-fs.target.wants
%dir %{systemdunitdir}/rescue.target.wants
%dir %{systemdunitdir}/runlevel[12345].target.wants
%dir %{systemdunitdir}/shutdown.target.wants
%dir %{systemdunitdir}/sigpwr.target.wants
%dir %{systemdunitdir}/sockets.target.wants
%dir %{systemdunitdir}/sound.target.wants
%dir %{systemdunitdir}/sysinit.target.wants
%dir %{systemdunitdir}/syslog.target.wants
%dir %{systemdunitdir}/system-update.target.wants
%dir %{systemdunitdir}/timers.target.wants
%if %{with cryptsetup}
%{systemdunitdir}/initrd-root-device.target.wants/remote-cryptsetup.target
%{systemdunitdir}/initrd-root-device.target.wants/remote-veritysetup.target
%endif
%{systemdunitdir}/graphical.target.wants/display-manager.service
%{systemdunitdir}/graphical.target.wants/systemd-update-utmp-runlevel.service
%if %{with efi} && %{with tpm2}
%{systemdunitdir}/initrd.target.wants/systemd-pcrphase-initrd.service
%endif
%{systemdunitdir}/local-fs.target.wants/pld-clean-tmp.service
%{systemdunitdir}/local-fs.target.wants/var-lock.mount
%{systemdunitdir}/local-fs.target.wants/var-run.mount
%{systemdunitdir}/multi-user.target.wants/getty.target
%{systemdunitdir}/multi-user.target.wants/rc-local.service
%{systemdunitdir}/multi-user.target.wants/systemd-ask-password-wall.path
%{systemdunitdir}/multi-user.target.wants/systemd-logind.service
%{systemdunitdir}/multi-user.target.wants/systemd-update-utmp-runlevel.service
%{systemdunitdir}/multi-user.target.wants/systemd-user-sessions.service
%{systemdunitdir}/rescue.target.wants/systemd-update-utmp-runlevel.service
%{systemdunitdir}/sigpwr.target.wants/sigpwr-container-shutdown.service
%{systemdunitdir}/sockets.target.wants/systemd-initctl.socket
%{systemdunitdir}/sockets.target.wants/systemd-journald-dev-log.socket
%{systemdunitdir}/sockets.target.wants/systemd-journald.socket
%{systemdunitdir}/sockets.target.wants/systemd-udevd-control.socket
%{systemdunitdir}/sockets.target.wants/systemd-udevd-kernel.socket
%if %{with cryptsetup}
%{systemdunitdir}/sysinit.target.wants/cryptsetup.target
%{systemdunitdir}/sysinit.target.wants/integritysetup.target
%{systemdunitdir}/sysinit.target.wants/veritysetup.target
%endif
%{systemdunitdir}/sysinit.target.wants/dev-hugepages.mount
%{systemdunitdir}/sysinit.target.wants/dev-mqueue.mount
%{systemdunitdir}/sysinit.target.wants/kmod-static-nodes.service
%{systemdunitdir}/sysinit.target.wants/ldconfig.service
%{systemdunitdir}/sysinit.target.wants/proc-sys-fs-binfmt_misc.automount
%{systemdunitdir}/sysinit.target.wants/sys-fs-fuse-connections.mount
%{systemdunitdir}/sysinit.target.wants/sys-kernel-debug.mount
%{systemdunitdir}/sysinit.target.wants/sys-kernel-tracing.mount
%{systemdunitdir}/sysinit.target.wants/systemd-ask-password-console.path
%{systemdunitdir}/sysinit.target.wants/systemd-binfmt.service
%{?with_efi:%{systemdunitdir}/sysinit.target.wants/systemd-boot-random-seed.service}
%{systemdunitdir}/sysinit.target.wants/systemd-firstboot.service
%{systemdunitdir}/sysinit.target.wants/systemd-hwdb-update.service
%{systemdunitdir}/sysinit.target.wants/systemd-journal-catalog-update.service
%{systemdunitdir}/sysinit.target.wants/systemd-journald.service
%{systemdunitdir}/sysinit.target.wants/systemd-journal-flush.service
%{systemdunitdir}/sysinit.target.wants/systemd-machine-id-commit.service
%{systemdunitdir}/sysinit.target.wants/systemd-modules-load.service
%if %{with efi} && %{with tpm2}
%{systemdunitdir}/sysinit.target.wants/systemd-pcrmachine.service
%{systemdunitdir}/sysinit.target.wants/systemd-pcrphase-sysinit.service
%{systemdunitdir}/sysinit.target.wants/systemd-pcrphase.service
%endif
%{systemdunitdir}/sysinit.target.wants/systemd-random-seed.service
%{systemdunitdir}/sysinit.target.wants/systemd-sysctl.service
%{systemdunitdir}/sysinit.target.wants/systemd-sysusers.service
%{systemdunitdir}/sysinit.target.wants/systemd-tmpfiles-setup-dev.service
%{systemdunitdir}/sysinit.target.wants/systemd-tmpfiles-setup.service
%{systemdunitdir}/sysinit.target.wants/systemd-udevd.service
%{systemdunitdir}/sysinit.target.wants/systemd-udev-trigger.service
%{systemdunitdir}/sysinit.target.wants/systemd-update-done.service
%{systemdunitdir}/sysinit.target.wants/systemd-update-utmp.service
%{systemdunitdir}/timers.target.wants/systemd-tmpfiles-clean.timer
%dir %{systemduserunitdir}/sockets.target.wants
%{systemduserunitdir}/graphical-session-pre.target
%{systemduserunitdir}/graphical-session.target
%{_mandir}/man5/user@.service.5*
%{_mandir}/man5/user-runtime-dir@.service.5*
%{_mandir}/man8/30-systemd-environment-d-generator.8*
%{_mandir}/man8/systemd-environment-d-generator.8*
%{_mandir}/man8/systemd-ask-password-console.path.8*
%{_mandir}/man8/systemd-ask-password-console.service.8*
%{_mandir}/man8/systemd-ask-password-wall.path.8*
%{_mandir}/man8/systemd-ask-password-wall.service.8*
%{_mandir}/man8/systemd-backlight@.service.8*
%{_mandir}/man8/systemd-binfmt.service.8*
%{?with_efi:%{_mandir}/man8/systemd-bless-boot.service.8*}
%{_mandir}/man8/systemd-boot-check-no-failures.service.8*
%{?with_efi:%{_mandir}/man8/systemd-boot-random-seed.service.8*}
%{_mandir}/man8/systemd-coredump.socket.8*
%{_mandir}/man8/systemd-coredump@.service.8*
%if %{with cryptsetup}
%{_mandir}/man8/systemd-cryptsetup.8*
%{_mandir}/man8/systemd-cryptsetup@.service.8*
%{_mandir}/man8/systemd-integritysetup.8*
%{_mandir}/man8/systemd-integritysetup@.service.8*
%endif
%{_mandir}/man8/systemd-fsck-root.service.8*
%{_mandir}/man8/systemd-fsck@.service.8*
%{_mandir}/man8/systemd-halt.service.8*
%{_mandir}/man8/systemd-hibernate.service.8*
%{_mandir}/man8/systemd-hostnamed.service.8*
%{_mandir}/man8/systemd-hybrid-sleep.service.8*
%{_mandir}/man8/systemd-initctl.service.8*
%{_mandir}/man8/systemd-initctl.socket.8*
%{_mandir}/man8/systemd-journald.service.8*
%{_mandir}/man8/systemd-journald.socket.8*
%{_mandir}/man8/systemd-journald-audit.socket.8*
%{_mandir}/man8/systemd-kexec.service.8*
%{_mandir}/man8/systemd-localed.service.8*
%{_mandir}/man8/systemd-logind.service.8*
%{_mandir}/man8/systemd-modules-load.service.8*
%if %{with efi} && %{with tpm2}
%{_mandir}/man8/systemd-pcrfs-root.service.8*
%{_mandir}/man8/systemd-pcrfs@.service.8*
%{_mandir}/man8/systemd-pcrmachine.service.8*
%{_mandir}/man8/systemd-pcrphase-initrd.service.8*
%{_mandir}/man8/systemd-pcrphase-sysinit.service.8*
%{_mandir}/man8/systemd-pcrphase.8*
%{_mandir}/man8/systemd-pcrphase.service.8*
%endif
%{_mandir}/man8/systemd-poweroff.service.8*
%{_mandir}/man8/systemd-quotacheck.service.8*
%{_mandir}/man8/systemd-random-seed.service.8*
%{_mandir}/man8/systemd-reboot.service.8*
%{_mandir}/man8/systemd-remount-fs.service.8*
%{_mandir}/man8/systemd-rfkill.socket.8*
%{_mandir}/man8/systemd-suspend.service.8*
%{_mandir}/man8/systemd-suspend-then-hibernate.service.8*
%{_mandir}/man8/systemd-sysctl.service.8*
%{_mandir}/man8/systemd-sysext.service.8*
%{_mandir}/man8/systemd-time-wait-sync.service.8*
%{_mandir}/man8/systemd-timedated.service.8*
%{_mandir}/man8/systemd-tmpfiles-clean.service.8*
%{_mandir}/man8/systemd-tmpfiles-clean.timer.8*
%{_mandir}/man8/systemd-tmpfiles-setup.service.8*
%{_mandir}/man8/systemd-tmpfiles-setup-dev.service.8*
%{_mandir}/man8/systemd-udev-settle.service.8*
%{_mandir}/man8/systemd-udevd.service.8*
%{_mandir}/man8/systemd-udevd-control.socket.8*
%{_mandir}/man8/systemd-udevd-kernel.socket.8*
%{_mandir}/man8/systemd-update-utmp-runlevel.service.8*
%{_mandir}/man8/systemd-update-utmp.service.8*
%{_mandir}/man8/systemd-user-sessions.service.8*
%{_mandir}/man8/systemd-userdbd.service.8*
%{_mandir}/man8/systemd-vconsole-setup.service.8*

%files tools
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/systemd-cgls
%attr(755,root,root) %{_bindir}/systemd-cgtop
%{_mandir}/man1/systemd-cgls.1*
%{_mandir}/man1/systemd-cgtop.1*

%files container
%defattr(644,root,root,755)
%attr(755,root,root) /bin/machinectl
/lib/systemd/import-pubring.gpg
%attr(755,root,root) /lib/systemd/systemd-export
%attr(755,root,root) /lib/systemd/systemd-import
%attr(755,root,root) /lib/systemd/systemd-import-fs
%attr(755,root,root) /lib/systemd/systemd-machined
%attr(755,root,root) /lib/systemd/systemd-pull
%attr(755,root,root) /lib/systemd/systemd-importd
%attr(755,root,root) %{_bindir}/systemd-dissect
%{_datadir}/dbus-1/system-services/org.freedesktop.import1.service
%{_datadir}/dbus-1/system-services/org.freedesktop.machine1.service
%{_datadir}/dbus-1/interfaces/org.freedesktop.import1.*.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.machine1.*.xml
%{_datadir}/dbus-1/system.d/org.freedesktop.import1.conf
%{_datadir}/dbus-1/system.d/org.freedesktop.machine1.conf
%{_datadir}/polkit-1/actions/org.freedesktop.import1.policy
%{_datadir}/polkit-1/actions/org.freedesktop.machine1.policy
%{_mandir}/man1/machinectl.1*
%{_mandir}/man5/org.freedesktop.import1.5*
%{_mandir}/man5/org.freedesktop.machine1.5*
%{_mandir}/man8/systemd-importd.8*
%{_mandir}/man8/systemd-importd.service.8*
%{_mandir}/man8/systemd-machined.8*
%{_mandir}/man8/systemd-machined.service.8*
%{systemdunitdir}/dbus-org.freedesktop.import1.service
%{systemdunitdir}/dbus-org.freedesktop.machine1.service
%{systemdunitdir}/machines.target
%dir %{systemdunitdir}/machines.target.wants
%{systemdunitdir}/machines.target.wants/var-lib-machines.mount
%{systemdunitdir}/remote-fs.target.wants/var-lib-machines.mount
%{systemdunitdir}/var-lib-machines.mount
%{systemdunitdir}/systemd-importd.service
%{systemdunitdir}/systemd-machined.service

%if %{with microhttpd}
%files journal-remote
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/systemd/journal-remote.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/systemd/journal-upload.conf
%{_prefix}/lib/sysusers.d/systemd-remote.conf
%{systemdunitdir}/systemd-journal-gatewayd.service
%{systemdunitdir}/systemd-journal-gatewayd.socket
%{systemdunitdir}/systemd-journal-remote.service
%{systemdunitdir}/systemd-journal-upload.service
%{systemdunitdir}/systemd-journal-remote.socket
%attr(755,root,root) /lib/systemd/systemd-journal-gatewayd
%attr(755,root,root) /lib/systemd/systemd-journal-remote
%attr(755,root,root) /lib/systemd/systemd-journal-upload
%{_datadir}/systemd/gatewayd
%{_mandir}/man5/journal-remote.conf.5*
%{_mandir}/man5/journal-remote.conf.d.5*
%{_mandir}/man5/journal-upload.conf.5.*
%{_mandir}/man5/journal-upload.conf.d.5*
%{_mandir}/man8/systemd-journal-gatewayd.8*
%{_mandir}/man8/systemd-journal-gatewayd.service.8*
%{_mandir}/man8/systemd-journal-gatewayd.socket.8*
%{_mandir}/man8/systemd-journal-remote.8*
%{_mandir}/man8/systemd-journal-upload.8*
%{_mandir}/man8/systemd-journal-remote.service.8*
%{_mandir}/man8/systemd-journal-remote.socket.8*
%{_mandir}/man8/systemd-journal-upload.service.8*
%endif

%files homed
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/homectl
%attr(755,root,root) /lib/systemd/systemd-homed
%attr(755,root,root) /lib/systemd/systemd-homework
%attr(755,root,root) /%{_lib}/security/pam_systemd_home.so
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/systemd/homed.conf
%{systemdunitdir}/systemd-homed.service
%{systemdunitdir}/systemd-homed-activate.service
%{_datadir}/dbus-1/interfaces/org.freedesktop.home1.*.xml
%{_datadir}/dbus-1/system-services/org.freedesktop.home1.service
%{_datadir}/dbus-1/system.d/org.freedesktop.home1.conf
%{_datadir}/polkit-1/actions/org.freedesktop.home1.policy
%{_mandir}/man1/homectl.1*
%{_mandir}/man5/homed.conf.5*
%{_mandir}/man5/homed.conf.d.5*
%{_mandir}/man5/org.freedesktop.home1.5*
%{_mandir}/man8/pam_systemd_home.8*
%{_mandir}/man8/systemd-homed.8*
%{_mandir}/man8/systemd-homed.service.8*

%files networkd
%defattr(644,root,root,755)
%{_datadir}/dbus-1/interfaces/org.freedesktop.network1.*.xml
%{_datadir}/dbus-1/system.d/org.freedesktop.network1.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/systemd/networkd.conf
%dir %{_sysconfdir}/systemd/network
%{_prefix}/lib/tmpfiles.d/systemd-network.conf
/lib/systemd/network/80-6rd-tunnel.network
/lib/systemd/network/80-container-host0.network
/lib/systemd/network/80-container-vb.network
/lib/systemd/network/80-container-ve.network
/lib/systemd/network/80-container-vz.network
/lib/systemd/network/80-vm-vt.network
/lib/systemd/network/80-wifi-adhoc.network
%{_prefix}/lib/sysusers.d/systemd-network.conf
%{systemdunitdir}/systemd-network-generator.service
%{systemdunitdir}/systemd-networkd-wait-online.service
%{systemdunitdir}/systemd-networkd-wait-online@.service
%{systemdunitdir}/systemd-networkd.service
%{systemdunitdir}/systemd-networkd.socket
%{_datadir}/dbus-1/system-services/org.freedesktop.network1.service
%{_datadir}/polkit-1/actions/org.freedesktop.network1.policy
%attr(755,root,root) /bin/networkctl
%attr(755,root,root) /lib/systemd/systemd-network-generator
%attr(755,root,root) /lib/systemd/systemd-networkd
%attr(755,root,root) /lib/systemd/systemd-networkd-wait-online
%{_mandir}/man1/networkctl.1*
%{_mandir}/man5/networkd.conf.5*
%{_mandir}/man5/networkd.conf.d.5*
%{_mandir}/man5/org.freedesktop.network1.5*
%{_mandir}/man7/systemd.net-naming-scheme.7*
%{_mandir}/man8/systemd-network-generator.8*
%{_mandir}/man8/systemd-network-generator.service.8*
%{_mandir}/man8/systemd-networkd-wait-online.8*
%{_mandir}/man8/systemd-networkd-wait-online.service.8*
%{_mandir}/man8/systemd-networkd-wait-online@.service.8*
%{_mandir}/man8/systemd-networkd.8*
%{_mandir}/man8/systemd-networkd.service.8*

%files oomd
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/oomctl
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/systemd/oomd.conf
%attr(755,root,root) /lib/systemd/systemd-oomd
%{_prefix}/lib/sysusers.d/systemd-oom.conf
%{systemdunitdir}/systemd-oomd.service
%{systemdunitdir}/systemd-oomd.socket
%{_datadir}/dbus-1/interfaces/org.freedesktop.oom1.*.xml
%{_datadir}/dbus-1/system-services/org.freedesktop.oom1.service
%{_datadir}/dbus-1/system.d/org.freedesktop.oom1.conf
%{_mandir}/man1/oomctl.1*
%{_mandir}/man5/oomd.conf.5*
%{_mandir}/man5/oomd.conf.d.5*
%{_mandir}/man5/org.freedesktop.oom1.5*
%{_mandir}/man8/systemd-oomd.8*
%{_mandir}/man8/systemd-oomd.service.8*

%files portabled
%defattr(644,root,root,755)
%doc docs/PORTABLE_SERVICES.md
%attr(755,root,root) /bin/portablectl
%attr(755,root,root) /lib/systemd/systemd-portabled
%{systemdunitdir}/dbus-org.freedesktop.portable1.service
%{systemdunitdir}/systemd-portabled.service
%dir /lib/systemd/portable
%dir /lib/systemd/portable/profile
%dir /lib/systemd/portable/profile/default
/lib/systemd/portable/profile/default/service.conf
%dir /lib/systemd/portable/profile/nonetwork
/lib/systemd/portable/profile/nonetwork/service.conf
%dir /lib/systemd/portable/profile/strict
/lib/systemd/portable/profile/strict/service.conf
%dir /lib/systemd/portable/profile/trusted
/lib/systemd/portable/profile/trusted/service.conf
%{systemdtmpfilesdir}/portables.conf
%{_datadir}/dbus-1/interfaces/org.freedesktop.portable1.*.xml
%{_datadir}/dbus-1/system-services/org.freedesktop.portable1.service
%{_datadir}/dbus-1/system.d/org.freedesktop.portable1.conf
%{_datadir}/polkit-1/actions/org.freedesktop.portable1.policy
%{_mandir}/man1/portablectl.1*
%{_mandir}/man5/org.freedesktop.portable1.5*
%{_mandir}/man8/systemd-portabled.8*
%{_mandir}/man8/systemd-portabled.service.8*

%files repart
%defattr(644,root,root,755)
%dir %{_sysconfdir}/repart.d
%attr(755,root,root) /bin/systemd-repart
%{systemdunitdir}/systemd-repart.service
%{systemdunitdir}/initrd-root-fs.target.wants/systemd-repart.service
%{systemdunitdir}/sysinit.target.wants/systemd-repart.service
%dir %{_prefix}/lib/repart.d
%{_mandir}/man5/repart.d.5*
%{_mandir}/man8/systemd-repart.8*
%{_mandir}/man8/systemd-repart.service.8*

%files resolved
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/systemd/resolved.conf
%{_prefix}/lib/sysusers.d/systemd-resolve.conf
%{_prefix}/lib/tmpfiles.d/systemd-resolve.conf
%{_datadir}/dbus-1/interfaces/org.freedesktop.resolve1.*.xml
%{_datadir}/dbus-1/system.d/org.freedesktop.resolve1.conf
%{_datadir}/dbus-1/system-services/org.freedesktop.resolve1.service
%{_datadir}/polkit-1/actions/org.freedesktop.resolve1.policy
%{systemdunitdir}/systemd-resolved.service
%attr(755,root,root) /sbin/resolvconf
%attr(755,root,root) %{_bindir}/resolvectl
%attr(755,root,root) /lib/systemd/systemd-resolved
%{_mandir}/man1/resolvconf.1*
%{_mandir}/man1/resolvectl.1*
%{_mandir}/man5/org.freedesktop.resolve1.5*
%{_mandir}/man5/resolved.conf.5*
%{_mandir}/man5/resolved.conf.d.5*
%{_mandir}/man8/systemd-resolved.8*
%{_mandir}/man8/systemd-resolved.service.8*

%files sysupdate
%defattr(644,root,root,755)
%dir %{_sysconfdir}/sysupdate.d
%{systemdunitdir}/systemd-sysupdate.service
%{systemdunitdir}/systemd-sysupdate.timer
%{systemdunitdir}/systemd-sysupdate-reboot.service
%{systemdunitdir}/systemd-sysupdate-reboot.timer
%attr(755,root,root) /lib/systemd/systemd-sysupdate
%dir %{_prefix}/lib/sysupdate.d
%{_mandir}/man5/sysupdate.d.5*
%{_mandir}/man8/systemd-sysupdate.8*
%{_mandir}/man8/systemd-sysupdate.service.8*
%{_mandir}/man8/systemd-sysupdate.timer.8*
%{_mandir}/man8/systemd-sysupdate-reboot.service.8*
%{_mandir}/man8/systemd-sysupdate-reboot.timer.8*

%files inetd
%defattr(644,root,root,755)
%attr(755,root,root) %{systemdunitdir}-generators/pld-rc-inetd-generator
%{systemdunitdir}/rc-inetd.service

%files analyze
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/systemd-analyze
%{_mandir}/man1/systemd-analyze.1*

%if %{with efi}
%files ukify
%defattr(644,root,root,755)
%attr(755,root,root) /lib/systemd/ukify
%{_mandir}/man1/ukify.1*
%endif

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) /%{_lib}/libnss_myhostname.so.2
%attr(755,root,root) /%{_lib}/libnss_mymachines.so.2
%attr(755,root,root) /%{_lib}/libnss_resolve.so.2
%attr(755,root,root) /%{_lib}/libnss_systemd.so.2
%attr(755,root,root) /%{_lib}/libsystemd.so.*.*.*
%attr(755,root,root) %ghost /%{_lib}/libsystemd.so.0
%if "%{_lib}" != "lib"
%dir /%{_lib}/systemd
%endif
%attr(755,root,root) /%{_lib}/systemd/libsystemd-core*.so
%attr(755,root,root) /%{_lib}/systemd/libsystemd-shared*.so
%{_mandir}/man8/libnss_resolve.so.2.8*
%{_mandir}/man8/libnss_systemd.so.2.8*
%{_mandir}/man8/nss-resolve.8*
%{_mandir}/man8/nss-systemd.8*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) /%{_lib}/libsystemd.so
%{_includedir}/%{name}
%{_pkgconfigdir}/libsystemd.pc
%{_npkgconfigdir}/systemd.pc
%{_mandir}/man3/SD_*.3*
%{_mandir}/man3/sd*.3*

%files -n bash-completion-systemd
%defattr(644,root,root,755)
%{bash_compdir}/bootctl
%{bash_compdir}/busctl
%{bash_compdir}/coredumpctl
%{bash_compdir}/homectl
%{bash_compdir}/hostnamectl
%{bash_compdir}/journalctl
%{bash_compdir}/kernel-install
%{bash_compdir}/localectl
%{bash_compdir}/loginctl
%{bash_compdir}/machinectl
%{bash_compdir}/networkctl
%{bash_compdir}/oomctl
%{bash_compdir}/portablectl
%{bash_compdir}/resolvectl
%{bash_compdir}/systemctl
%{bash_compdir}/systemd-analyze
%{bash_compdir}/systemd-cat
%{bash_compdir}/systemd-cgls
%{bash_compdir}/systemd-cgtop
%{bash_compdir}/systemd-cryptenroll
%{bash_compdir}/systemd-delta
%{bash_compdir}/systemd-detect-virt
%{bash_compdir}/systemd-dissect
%{bash_compdir}/systemd-id128
%{bash_compdir}/systemd-nspawn
%{bash_compdir}/systemd-path
%{bash_compdir}/systemd-resolve
%{bash_compdir}/systemd-run
%{bash_compdir}/systemd-sysext
%{bash_compdir}/timedatectl

%files -n zsh-completion-systemd
%defattr(644,root,root,755)
%{zsh_compdir}/_bootctl
%{zsh_compdir}/_busctl
%{zsh_compdir}/_coredumpctl
%{zsh_compdir}/_hostnamectl
%{zsh_compdir}/_journalctl
%{zsh_compdir}/_kernel-install
%{zsh_compdir}/_localectl
%{zsh_compdir}/_loginctl
%{zsh_compdir}/_machinectl
%{zsh_compdir}/_networkctl
%{zsh_compdir}/_oomctl
%{zsh_compdir}/_resolvectl
%{zsh_compdir}/_sd_hosts_or_user_at_host
%{zsh_compdir}/_sd_machines
%{zsh_compdir}/_sd_outputmodes
%{zsh_compdir}/_sd_unit_files
%{zsh_compdir}/_systemctl
%{zsh_compdir}/_systemd
%{zsh_compdir}/_systemd-analyze
%{zsh_compdir}/_systemd-delta
%{zsh_compdir}/_systemd-inhibit
%{zsh_compdir}/_systemd-nspawn
%{zsh_compdir}/_systemd-path
%{zsh_compdir}/_systemd-run
%{zsh_compdir}/_systemd-tmpfiles
%{zsh_compdir}/_timedatectl

%files -n udev
%defattr(644,root,root,755)
%dev(c,1,3) %attr(666,root,root) /dev/null
%dev(c,5,1) %attr(660,root,console) /dev/console
%dev(c,1,5) %attr(666,root,root) /dev/zero

%files -n udev-core
%defattr(644,root,root,755)

%{_prefix}/lib/udev

%attr(755,root,root) /lib/udev/net_helper

%attr(755,root,root) /lib/udev/ata_id
%attr(755,root,root) /lib/udev/cdrom_id
%attr(755,root,root) /lib/udev/dmi_memory_id
%attr(755,root,root) /lib/udev/fido_id
%attr(755,root,root) /lib/udev/mtd_probe
%attr(755,root,root) /lib/udev/scsi_id
%attr(755,root,root) /lib/udev/v4l_id

%attr(755,root,root) /lib/udev/udevd

/lib/udev/hwdb.d/20-acpi-vendor.hwdb
/lib/udev/hwdb.d/20-bluetooth-vendor-product.hwdb
/lib/udev/hwdb.d/20-dmi-id.hwdb
/lib/udev/hwdb.d/20-net-ifname.hwdb
/lib/udev/hwdb.d/20-OUI.hwdb
/lib/udev/hwdb.d/20-pci-classes.hwdb
/lib/udev/hwdb.d/20-pci-vendor-model.hwdb
/lib/udev/hwdb.d/20-sdio-classes.hwdb
/lib/udev/hwdb.d/20-sdio-vendor-model.hwdb
/lib/udev/hwdb.d/20-usb-classes.hwdb
/lib/udev/hwdb.d/20-usb-vendor-model.hwdb
/lib/udev/hwdb.d/20-vmbus-class.hwdb
/lib/udev/hwdb.d/60-autosuspend-chromiumos.hwdb
/lib/udev/hwdb.d/60-autosuspend-fingerprint-reader.hwdb
/lib/udev/hwdb.d/60-autosuspend.hwdb
/lib/udev/hwdb.d/60-evdev.hwdb
/lib/udev/hwdb.d/60-input-id.hwdb
/lib/udev/hwdb.d/60-keyboard.hwdb
/lib/udev/hwdb.d/60-seat.hwdb
/lib/udev/hwdb.d/60-sensor.hwdb
/lib/udev/hwdb.d/70-analyzers.hwdb
/lib/udev/hwdb.d/70-av-production.hwdb
/lib/udev/hwdb.d/70-cameras.hwdb
/lib/udev/hwdb.d/70-joystick.hwdb
/lib/udev/hwdb.d/70-mouse.hwdb
/lib/udev/hwdb.d/70-pda.hwdb
/lib/udev/hwdb.d/70-pointingstick.hwdb
/lib/udev/hwdb.d/70-sound-card.hwdb
/lib/udev/hwdb.d/70-touchpad.hwdb
/lib/udev/hwdb.d/80-ieee1394-unit-function.hwdb

%attr(755,root,root) %{_rootsbindir}/start_udev
%attr(755,root,root) %{_rootsbindir}/udevd
%attr(755,root,root) %{_rootsbindir}/udevadm
%attr(755,root,root) /bin/systemd-hwdb
%attr(755,root,root) /bin/udevadm

%dir %{_sysconfdir}/udev
%dir %{_sysconfdir}/udev/rules.d
%dir %{_sysconfdir}/udev/hwdb.d
%ghost %{_sysconfdir}/udev/hwdb.bin

%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/modprobe.d/fbdev-blacklist.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/modprobe.d/udev_blacklist.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/udev/links.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/udev/rules.d/40-alsa-restore.rules
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/udev/rules.d/70-udev-pld.rules
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/udev/rules.d/70-uinput.rules
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/udev/rules.d/70-steam_controller.rules
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/udev/rules.d/70-i2c.rules
%ifarch %{arm} aarch64
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/udev/rules.d/70-raspberrypi.rules
%endif
%config(noreplace,missingok) %verify(not md5 mtime size) %{_sysconfdir}/udev/rules.d/80-net-setup-link.rules

%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/udev/udev.conf

# rules below are NOT supposed to be changed by users
/lib/udev/rules.d/50-udev-default.rules
/lib/udev/rules.d/60-autosuspend.rules
/lib/udev/rules.d/60-block.rules
/lib/udev/rules.d/60-cdrom_id.rules
/lib/udev/rules.d/60-drm.rules
/lib/udev/rules.d/60-evdev.rules
/lib/udev/rules.d/60-fido-id.rules
/lib/udev/rules.d/60-infiniband.rules
/lib/udev/rules.d/60-input-id.rules
/lib/udev/rules.d/60-persistent-alsa.rules
/lib/udev/rules.d/60-persistent-input.rules
/lib/udev/rules.d/60-persistent-storage.rules
/lib/udev/rules.d/60-persistent-storage-tape.rules
/lib/udev/rules.d/60-persistent-v4l.rules
/lib/udev/rules.d/60-sensor.rules
/lib/udev/rules.d/60-serial.rules
/lib/udev/rules.d/64-btrfs.rules
/lib/udev/rules.d/70-camera.rules
/lib/udev/rules.d/70-joystick.rules
/lib/udev/rules.d/70-memory.rules
/lib/udev/rules.d/70-mouse.rules
/lib/udev/rules.d/70-power-switch.rules
/lib/udev/rules.d/70-touchpad.rules
/lib/udev/rules.d/70-uaccess.rules
/lib/udev/rules.d/71-seat.rules
/lib/udev/rules.d/73-seat-late.rules
/lib/udev/rules.d/75-net-description.rules
/lib/udev/rules.d/75-probe_mtd.rules
/lib/udev/rules.d/78-sound-card.rules
/lib/udev/rules.d/80-drivers.rules
/lib/udev/rules.d/80-net-setup-link.rules
/lib/udev/rules.d/81-net-dhcp.rules
/lib/udev/rules.d/90-vconsole.rules

%{_mandir}/man5/udev.conf.5*
%{_mandir}/man7/udev.7*
%{_mandir}/man7/hwdb.7*
%{_mandir}/man8/systemd-hwdb.8*
%{_mandir}/man8/udevadm.8*
%{_mandir}/man8/udevd.8*

%files -n udev-libs
%defattr(644,root,root,755)
%attr(755,root,root) /%{_lib}/libudev.so.*.*.*
%attr(755,root,root) %ghost /%{_lib}/libudev.so.1

%files -n udev-devel
%defattr(644,root,root,755)
%attr(755,root,root) /%{_lib}/libudev.so
%{_includedir}/libudev.h
%{_pkgconfigdir}/libudev.pc
%{_npkgconfigdir}/udev.pc
%{_mandir}/man3/libudev.3*
%{_mandir}/man3/udev_*.3*

%files -n bash-completion-udev
%defattr(644,root,root,755)
%{bash_compdir}/udevadm

%files -n zsh-completion-udev
%defattr(644,root,root,755)
%{zsh_compdir}/_udevadm

%files -n rpm-macros-systemd
%defattr(644,root,root,755)
/usr/lib/rpm/macros.d/macros.systemd
