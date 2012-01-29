#
# TODO:
#	- remove compat-pld-var-run.tmpfiles and maybe tmpfiles-not-fatal.patch
#	  after enough packages provide their own tmpfiles.d configs for
#	  /var/run directories
#
# Conditional build:
%bcond_without	audit		# without audit support
%bcond_without	cryptsetup	# without cryptsetup support
%bcond_without	gtk		# build gtk tools
%bcond_without	pam		# PAM authentication support
%bcond_without	selinux		# without SELinux support
%bcond_without	tcpd		# libwrap (tcp_wrappers) support

Summary:	A System and Service Manager
Summary(pl.UTF-8):	systemd - zarządca systemu i usług dla Linuksa
Name:		systemd
Version:	39
Release:	0.1
License:	GPL v2+
Group:		Base
Source0:	http://www.freedesktop.org/software/systemd/%{name}-%{version}.tar.xz
# Source0-md5:	7179b34f6f6553d2a36551ac1dec5f0d
Source1:	%{name}-sysv-convert
Source2:	systemd_booted.c
Source3:	ifup@.service
Source4:	network-post.service
Source5:	network.service
Source6:	compat-pld-media.tmpfiles
Source7:	compat-pld-var-run.tmpfiles
Patch0:		target-pld.patch
Patch1:		config-pld.patch
Patch2:		shut-sysv-up.patch
Patch3:		pld-sysv-network.patch
Patch4:		tmpfiles-not-fatal.patch
URL:		http://www.freedesktop.org/wiki/Software/systemd
BuildRequires:	acl-devel
%{?with_audit:BuildRequires:	audit-libs-devel}
BuildRequires:	autoconf >= 2.63
BuildRequires:	automake >= 1:1.11
%{?with_cryptsetup:BuildRequires:	cryptsetup-luks-devel}
BuildRequires:	dbus-devel >= 1.3.2
BuildRequires:	docbook-style-xsl
%if %{with gtk}
BuildRequires:	glib2-devel >= 1:2.26.1
BuildRequires:	gtk+2-devel >= 2:2.24.0
BuildRequires:	libgee-devel
BuildRequires:	libnotify-devel >= 0.7.0
%endif
BuildRequires:	gperf
BuildRequires:	intltool >= 0.40.0
BuildRequires:	libcap-devel
%{?with_selinux:BuildRequires:	libselinux-devel}
BuildRequires:	libtool >= 2:2.2
%{?with_tcpd:BuildRequires:	libwrap-devel}
BuildRequires:	libxslt-progs
BuildRequires:	m4
%{?with_pam:BuildRequires:	pam-devel}
BuildRequires:	pkgconfig >= 0.9.0
BuildRequires:	rpmbuild(macros) >= 1.527
BuildRequires:	udev-devel >= 172
# not required for building from release (which contains *.c for *.vala)
#BuildRequires:	vala >= 0.10.0
Requires:	%{name}-libs = %{version}-%{release}
Requires:	%{name}-units = %{version}-%{release}
Requires:	SysVinit-tools
Requires:	agetty
Requires:	dbus >= 1.3.2
Requires:	dbus-systemd
Requires:	filesystem >= 4.0
Requires:	rc-scripts >= 0.4.5.1-7
Requires:	setup >= 2.8.0-2
Requires:	udev-core >= 1:172
Requires:	udev-systemd >= 1:172
Requires:	udev-libs >= 1:172
Suggests:	ConsoleKit-systemd
Suggests:	fsck >= 2.20
Suggests:	nss_myhostname
# python modules required by systemd-analyze
Suggests:	python-dbus
Suggests:	python-modules
Suggests:	service(syslog)
Provides:	udev-acl
Conflicts:	upstart
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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
Requires(post):	gawk
Requires:	pkgconfig

%description units
Basic configuration files, directories and installation tool for the
systemd system and service manager.

This is common config, use %{_sysconfdir}/systemd/system to override.

%description units -l pl.UTF-8
Podstawowe pliki konfiguracyjne, katalogi i narzędzie instalacyjne dla
zarządcy systemu i usług systemd.

Ten pakiet zawiera ogólną konfigurację, ustawienia można nadpisać
poprzez katalog %{_sysconfdir}/systemd/system.

%package gtk
Summary:	Graphical frontend for systemd
Summary(pl.UTF-8):	Graficzny interfejs do systemd
Group:		Base
Requires:	%{name} = %{version}-%{release}
Requires:	polkit

%description gtk
Graphical front-end for systemd.

%description gtk -l pl.UTF-8
Graficzny interfejs do systemd.

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
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header files for systemd libraries.

%description devel -l pl.UTF-8
Pliki nagłówkowe bibliotek systemd.

%package -n bash-completion-systemd
Summary:	bash-completion for systemd
Summary(pl.UTF-8):	Bashowe dopełnianie składni dla systemd
Group:		Applications/Shells
Requires:	%{name}
Requires:	bash-completion

%description -n bash-completion-systemd
bash-completion for systemd.

%description -n bash-completion-systemd -l pl.UTF-8
Bashowe dopełnianie składni dla systemd

%prep
%setup -q
%patch0 -p1
%patch1 -p1
#%patch2 -p1
%patch3 -p1
%patch4 -p1
cp -p %{SOURCE2} src/systemd_booted.c

%build
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{__enable_disable audit} \
	%{__enable_disable cryptsetup libcryptsetup} \
	%{__enable_disable gtk} \
	%{__enable_disable pam} \
	%{__enable_disable selinux} \
	%{__enable_disable tcpd tcpwrap} \
	--disable-silent-rules \
	--disable-static \
	--with-distro=pld \
	--with-rootprefix= \
	--with-rootlibdir=/%{_lib}

%{__make}
./libtool --mode=link --tag=CC %{__cc} %{rpmcppflags} %{rpmcflags} -o systemd_booted %{rpmldflags} src/systemd_booted.c -L. -lsystemd-daemon

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

./libtool --mode=install install -m755 systemd_booted $RPM_BUILD_ROOT/bin/systemd_booted

# Create SysV compatibility symlinks. systemctl/systemd are smart
# enough to detect the way they were called
install -d $RPM_BUILD_ROOT/sbin
ln -s ../bin/systemd $RPM_BUILD_ROOT/sbin/init
ln -s ../bin/systemctl $RPM_BUILD_ROOT/sbin/halt
ln -s ../bin/systemctl $RPM_BUILD_ROOT/sbin/poweroff
ln -s ../bin/systemctl $RPM_BUILD_ROOT/sbin/reboot
ln -s ../bin/systemctl $RPM_BUILD_ROOT/sbin/runlevel
ln -s ../bin/systemctl $RPM_BUILD_ROOT/sbin/shutdown
ln -s ../bin/systemctl $RPM_BUILD_ROOT/sbin/telinit

ln -s ../modules $RPM_BUILD_ROOT%{_sysconfdir}/modules-load.d/modules.conf
# disable random and console SYSV service 
ln -s /dev/null $RPM_BUILD_ROOT/lib/systemd/system/random.service
ln -s /dev/null $RPM_BUILD_ROOT/lib/systemd/system/console.service

# add static (non-NetworkManager) networking
install %{SOURCE3} $RPM_BUILD_ROOT/lib/systemd/system/ifup@.service
install %{SOURCE4} $RPM_BUILD_ROOT/lib/systemd/system/network-post.service
install %{SOURCE5} $RPM_BUILD_ROOT/lib/systemd/system/network.service

# install compatibility tmpfiles configs
install %{SOURCE6} $RPM_BUILD_ROOT%{_sysconfdir}/tmpfiles.d/compat-pld-media.conf
install %{SOURCE7} $RPM_BUILD_ROOT%{_sysconfdir}/tmpfiles.d/compat-pld-var-run.conf

# All wants links are created at %post to make sure they are not owned
# and hence overriden by rpm if the user deletes them (missingok?)
%{__rm} -r $RPM_BUILD_ROOT%{_sysconfdir}/systemd/system/*.target.wants

# it is in rc-scripts pkg
%{__rm} $RPM_BUILD_ROOT/lib/systemd/system/rc-local.service

# Make sure these directories are properly owned:
#	- halt,kexec,poweroff,reboot: generic ones used by ConsoleKit-systemd,
#	- syslog _might_ be used by some syslog implementation (none for now),
#	- isn't dbus populated by dbus-systemd only (so to be moved there)?
install -d $RPM_BUILD_ROOT/lib/systemd/system/{dbus,halt,kexec,poweroff,reboot,syslog}.target.wants

# Create new-style configuration files so that we can ghost-own them
touch $RPM_BUILD_ROOT%{_sysconfdir}/{hostname,locale.conf,machine-id,machine-info,os-release,timezone,vconsole.conf}

# Install SysV conversion tool for systemd
install -p %{SOURCE1} $RPM_BUILD_ROOT%{_bindir}

install -d $RPM_BUILD_ROOT/var/log
:> $RPM_BUILD_ROOT/var/log/btmp
:> $RPM_BUILD_ROOT/var/log/wtmp

%if %{without gtk}
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man1/systemadm.1*
%endif

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
		target="/lib/systemd/system/graphical.target"
	else
		target="/lib/systemd/system/runlevel$runlevel.target"
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
fi
# Enable the services we install by default.
/bin/systemctl enable \
	getty@.service \
	network.service \
	network-post.service \
	remote-fs.target \
	systemd-readahead-replay.service \
	systemd-readahead-collect.service >/dev/null 2>&1 || :

# Find and enable all installed interfaces
mkdir -p %{_sysconfdir}/systemd/system/network.target.wants >/dev/null 2>&1 || :
for f in /etc/sysconfig/interfaces/ifcfg-* ; do
	ff=$(basename $f)
	ff=${ff##ifcfg-}
	case "$ff" in
	*.rpmorig|*.rpmnew|*.rpmsave|*~|*.orig)
		continue
		;;
	*)
		DEVICE="" ; ONBOOT="" ; USERS=""
		. $f 2>/dev/null
		[ ${USERS:-no} != no ] && continue
		if [ "$DEVICE" = "$ff" -a ${ONBOOT:-no} = "yes" ]; then
			ln -s /lib/systemd/system/ifup@.service \
				%{_sysconfdir}/systemd/system/network.target.wants/ifcfg@$ff.service >/dev/null 2>&1 || :
		fi
		;;
	esac
done

%preun units
if [ $1 -eq 0 ] ; then
	/bin/systemctl disable \
		getty@.service \
		network.service \
		network-post.service \
		remote-fs.target \
		systemd-readahead-replay.service \
		systemd-readahead-collect.service >/dev/null 2>&1 || :

	%{__rm} -f %{_sysconfdir}/systemd/system/default.target >/dev/null 2>&1 || :
	%{__rm} -f %{_sysconfdir}/systemd/system/network.target.wants/ifcfg@*.service >/dev/null 2>&1 || :
fi

%postun units
if [ $1 -ge 1 ]; then
	/bin/systemctl daemon-reload > /dev/null 2>&1 || :
fi

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
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/os-release
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/timezone
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/vconsole.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/systemd/*.conf
%dir %{_sysconfdir}/systemd/user
/etc/xdg/systemd
%attr(755,root,root) /bin/systemd
%attr(755,root,root) /bin/systemd-ask-password
%attr(755,root,root) /bin/systemd-journalctl
%attr(755,root,root) /bin/systemd-loginctl
%attr(755,root,root) /bin/systemd-machine-id-setup
%attr(755,root,root) /bin/systemd-notify
%attr(755,root,root) /bin/systemd-tty-ask-password-agent
%attr(755,root,root) %{_bindir}/systemd-analyze
%attr(755,root,root) %{_bindir}/systemd-cat
%attr(755,root,root) %{_bindir}/systemd-cgtop
%attr(755,root,root) %{_bindir}/systemd-cgls
%attr(755,root,root) %{_bindir}/systemd-nspawn
%attr(755,root,root) %{_bindir}/systemd-stdio-bridge
%attr(755,root,root) %{_bindir}/systemd-sysv-convert
%attr(755,root,root) /lib/systemd/systemd-*
%dir /lib/systemd/system-generators
%attr(755,root,root) /lib/systemd/system-generators/systemd-*-generator
%dir /lib/systemd/system-shutdown
/lib/udev/rules.d/99-systemd.rules
/lib/udev/rules.d/70-uaccess.rules
/lib/udev/rules.d/71-seat.rules
/lib/udev/rules.d/73-seat-late.rules
%dir %{_libexecdir}/systemd
%{_libexecdir}/systemd/user
%dir %{_libexecdir}/systemd/user-generators
%config(noreplace,missingok) %{_libexecdir}/tmpfiles.d/*.conf
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
%{_mandir}/man1/systemd.1*
%{_mandir}/man1/systemd-*.1*
%{_mandir}/man3/sd_booted.3*
%{_mandir}/man3/sd_is_fifo.3*
%{_mandir}/man3/sd_is_socket.3
%{_mandir}/man3/sd_is_socket_inet.3
%{_mandir}/man3/sd_is_socket_unix.3
%{_mandir}/man3/sd_listen_fds.3*
%{_mandir}/man3/sd_notify.3*
%{_mandir}/man3/sd_notifyf.3
%{_mandir}/man3/sd_readahead.3*
%{_mandir}/man5/binfmt.d.5*
%{_mandir}/man5/hostname.5*
%{_mandir}/man5/locale.conf.5*
%{_mandir}/man5/machine-id.5*
%{_mandir}/man5/machine-info.5*
%{_mandir}/man5/modules-load.d.5*
%{_mandir}/man5/os-release.5*
%{_mandir}/man5/sysctl.d.5*
%{_mandir}/man5/systemd.*.5*
%{_mandir}/man5/systemd-logind.conf.5*
%{_mandir}/man5/timezone.5*
%{_mandir}/man5/vconsole.conf.5*
%{_mandir}/man7/daemon.7*
%{_mandir}/man7/sd-daemon.7*
%{_mandir}/man7/sd-login.7*
%{_mandir}/man7/sd-readahead.7*
%{_mandir}/man7/systemd.special.7*
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
%config(noreplace,missingok) %{_sysconfdir}/tmpfiles.d/*.conf
%dir %{_libexecdir}/binfmt.d
%dir %{_libexecdir}/modules-load.d
%dir %{_libexecdir}/sysctl.d
%{_libexecdir}/sysctl.d/coredump.conf
%attr(755,root,root) /bin/systemctl
%attr(755,root,root) /bin/systemd-tmpfiles
%attr(755,root,root) /bin/systemd_booted
%{_mandir}/man1/systemctl.1*
%{_mandir}/man5/tmpfiles.d.5*
%{_mandir}/man8/systemd-tmpfiles.8*
%{_npkgconfigdir}/systemd.pc

/lib/systemd/system/*.automount
/lib/systemd/system/*.mount
/lib/systemd/system/*.path
/lib/systemd/system/*.service
/lib/systemd/system/*.socket
/lib/systemd/system/*.target
/lib/systemd/system/*.timer
%dir /lib/systemd/system/*.wants
%config(noreplace,missingok) /lib/systemd/system/*.wants/*

%if %{with gtk}
%files gtk
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/systemadm
%attr(755,root,root) %{_bindir}/systemd-gnome-ask-password-agent
%{_mandir}/man1/systemadm.1*
%endif

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
%{_mandir}/man3/sd_get_seats.3*
%{_mandir}/man3/sd_get_sessions.3*
%{_mandir}/man3/sd_get_uids.3*
%{_mandir}/man3/sd_is_mq.3*
%{_mandir}/man3/sd_login_monitor_flush.3*
%{_mandir}/man3/sd_login_monitor_get_fd.3*
%{_mandir}/man3/sd_login_monitor_new.3*
%{_mandir}/man3/sd_login_monitor_unref.3*
%{_mandir}/man3/sd_pid_get_owner_uid.3*
%{_mandir}/man3/sd_pid_get_session.3*
%{_mandir}/man3/sd_pid_get_unit.3*
%{_mandir}/man3/sd_seat_can_multi_session.3*
%{_mandir}/man3/sd_seat_get_active.3*
%{_mandir}/man3/sd_seat_get_sessions.3*
%{_mandir}/man3/sd_session_get_seat.3*
%{_mandir}/man3/sd_session_get_uid.3*
%{_mandir}/man3/sd_session_is_active.3*
%{_mandir}/man3/sd_uid_get_seats.3*
%{_mandir}/man3/sd_uid_get_sessions.3*
%{_mandir}/man3/sd_uid_get_state.3*
%{_mandir}/man3/sd_uid_is_on_seat.3*

%files -n bash-completion-systemd
%defattr(644,root,root,755)
/etc/bash_completion.d/systemd-bash-completion.sh
