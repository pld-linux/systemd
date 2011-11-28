# UNPACKAGED files:
#   /etc/hostname
#   /etc/locale.conf
#   /etc/machine-info
#   /etc/os-release
#   /etc/timezone
#   /etc/vconsole.conf
#
# TODO:	- move %_libexecdir/tmpfiles.d/* to /etc/tmpfiles.d?
#	- shouldn't ../bin/systemctl symlinks be absolute? -no they shouldn't (think browsing mounted as chroot and seeing all blink due invalid link targets when doing ls)
#	- separate init subpackage (with symlink), one can switch to
#	  systemd using init=/bin/systemd with other one installed
#	- verify %_sysconfdir usage vs literal '/etc'
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
Version:	37
Release:	0.5
License:	GPL v2+
Group:		Base
Source0:	http://www.freedesktop.org/software/systemd/%{name}-%{version}.tar.bz2
# Source0-md5:	1435f23be79c8c38d1121c6b150510f3
Patch0:		target-pld.patch
URL:		http://www.freedesktop.org/wiki/Software/systemd
%{?with_audit:BuildRequires:	audit-libs-devel}
BuildRequires:	autoconf >= 2.63
BuildRequires:	automake >= 1:1.11
%{?with_cryptsetup:BuildRequires:	cryptsetup-luks-devel}
BuildRequires:	dbus-devel >= 1.3.2
BuildRequires:	docbook-style-xsl
%if %{with gtk}
BuildRequires:	glib2-devel >= 1:2.26.1
BuildRequires:	gtk+2-devel >= 2:2.24.0
BuildRequires:	libnotify-devel >= 0.7.0
%endif
BuildRequires:	gperf
BuildRequires:	libcap-devel
%{?with_selinux:BuildRequires:	libselinux-devel}
BuildRequires:	libtool >= 2:2.2
%{?with_tcpd:BuildRequires:	libwrap-devel}
BuildRequires:	libxslt-progs
BuildRequires:	m4
%{?with_pam:BuildRequires:	pam-devel}
BuildRequires:	pkgconfig >= 0.9.0
BuildRequires:	rpmbuild(macros) >= 1.527
BuildRequires:	udev-devel >= 160
BuildRequires:	vala >= 0.10.0
Requires:	%{name}-libs = %{version}-%{release}
Requires:	%{name}-units = %{version}-%{release}
Requires:	SysVinit-tools
Requires:	agetty
Requires:	dbus >= 1.3.2
Requires:	dbus-systemd
# python modules required by systemd-analyze
Requires:	filesystem >= 3.0-43
Requires:	python-dbus
Requires:	python-modules
Requires:	rc-scripts
Requires:	setup >= 2.8.0-2
Requires:	udev-core >= 160
Requires:	udev-systemd
Suggests:	ConsoleKit-systemd
Suggests:	rsyslog-systemd
Suggests:	udev-systemd
Provides:	SysVinit = 2.86-26
Provides:	readahead = 1:1.5.7-3
Provides:	virtual(init-daemon)
Obsoletes:	SysVinit < 2.86-26
Obsoletes:	readahead < 1:1.5.7-3
Obsoletes:	virtual(init-daemon)
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

%package units
Summary:	Configuration files, directories and installation tool for systemd
Group:		Base
Requires(post):	coreutils
Requires(post):	gawk
Requires:	pkgconfig

%description units
Basic configuration files, directories and installation tool for the
systemd system and service manager.

%package gtk
Summary:	Graphical frontend for systemd
Group:		Base
Requires:	%{name} = %{version}-%{release}
Requires:	polkit

%description gtk
Graphical front-end for systemd.

%package -n bash-completion-systemd
Summary:	bash-completion for systemd
Group:		Applications/Shells
Requires:	%{name}
Requires:	bash-completion

%description -n bash-completion-systemd
bash-completion for systemd.

%package libs
Summary:	Shared systemd library
Group:		Libraries

%description libs
Shared systemd library.

%package devel
Summary:	Header files for systemd libraries
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotek systemd
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header files for systemd libraries.

%description devel -l pl.UTF-8
Pliki nagłówkowe bibliotek systemd.

%prep
%setup -q
%patch0 -p1

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
	--with-rootdir=

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

for lib in libsystemd-daemon libsystemd-login; do
	%{__mv} $RPM_BUILD_ROOT{%{_libdir}/$lib.so.*,/%{_lib}}
	ln -sf /%{_lib}/$(basename $RPM_BUILD_ROOT/%{_lib}/$lib.so.*) $RPM_BUILD_ROOT%{_libdir}/$lib.so
done

# Create SysV compatibility symlinks. systemctl/systemd are smart
# enough to detect in which way they are called.
install -d $RPM_BUILD_ROOT/sbin
ln -s ../bin/systemd $RPM_BUILD_ROOT/sbin/init
ln -s ../bin/systemctl $RPM_BUILD_ROOT/sbin/halt
ln -s ../bin/systemctl $RPM_BUILD_ROOT/sbin/poweroff
ln -s ../bin/systemctl $RPM_BUILD_ROOT/sbin/reboot
ln -s ../bin/systemctl $RPM_BUILD_ROOT/sbin/runlevel
ln -s ../bin/systemctl $RPM_BUILD_ROOT/sbin/shutdown
ln -s ../bin/systemctl $RPM_BUILD_ROOT/sbin/telinit

ln -s ../modules $RPM_BUILD_ROOT%{_sysconfdir}/modules-load.d/modules.conf

# We create all wants links manually at installation time to make sure
# they are not owned and hence overriden by rpm after the used deleted
# them.
%{__rm} -r $RPM_BUILD_ROOT%{_sysconfdir}/systemd/system/*.target.wants

# do not cover /media (system-specific removable mountpoints)
%{__rm} -f $RPM_BUILD_ROOT/lib/systemd/local-fs.target.wants/media.mount
# do not cover /var/run (packages need rpm-provided subdirectories)
%{__rm} -f $RPM_BUILD_ROOT/lib/systemd/local-fs.target.wants/var-run.mount

# Make sure these directories are properly owned
install -d $RPM_BUILD_ROOT/lib/systemd/system/{basic,dbus,default,halt,kexec,poweroff,reboot,syslog}.target.wants

# Create new-style configuration files so that we can ghost-own them
touch $RPM_BUILD_ROOT%{_sysconfdir}/{hostname,locale.conf,machine-id,machine-info,os-release,timezone,vconsole.conf}

%if %{without gtk}
# to shut up check-files
rm -f $RPM_BUILD_ROOT%{_bindir}/systemadm
rm -f $RPM_BUILD_ROOT%{_bindir}/systemd-gnome-ask-password-agent
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
	ln -sf "$target" /etc/systemd/system/default.target >/dev/null 2>&1 || :

	# Enable the services we install by default.
	/bin/systemctl enable \
		getty@.service \
		remote-fs.target \
		systemd-readahead-replay.service \
		systemd-readahead-collect.service >/dev/null 2>&1 || :
fi

%preun units
if [ $1 -eq 0 ] ; then
	/bin/systemctl disable \
		getty@.service \
		remote-fs.target \
		systemd-readahead-replay.service \
		systemd-readahead-collect.service >/dev/null 2>&1 || :

	%{__rm} -f /etc/systemd/system/default.target >/dev/null 2>&1 || :
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
%dir %{_sysconfdir}/systemd
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/systemd/*.conf
/etc/xdg/systemd
%attr(755,root,root) /bin/systemd
%attr(755,root,root) /bin/systemd-ask-password
%attr(755,root,root) /bin/systemd-loginctl
%attr(755,root,root) /bin/systemd-machine-id-setup
%attr(755,root,root) /bin/systemd-notify
%attr(755,root,root) /bin/systemd-tty-ask-password-agent
%attr(755,root,root) %{_bindir}/systemd-analyze
%attr(755,root,root) %{_bindir}/systemd-cgls
%attr(755,root,root) %{_bindir}/systemd-nspawn
%attr(755,root,root) %{_bindir}/systemd-stdio-bridge
%attr(755,root,root) /sbin/halt
%attr(755,root,root) /sbin/init
%attr(755,root,root) /sbin/poweroff
%attr(755,root,root) /sbin/reboot
%attr(755,root,root) /sbin/runlevel
%attr(755,root,root) /sbin/shutdown
%attr(755,root,root) /sbin/telinit
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
%config(noreplace,missingok) %verify(not md5 mtime size) %{_libexecdir}/tmpfiles.d/*.conf
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
%{_mandir}/man1/init.1
%{_mandir}/man1/systemd.1*
%{_mandir}/man1/systemd-ask-password.1*
%{_mandir}/man1/systemd-cgls.1*
%{_mandir}/man1/systemd-notify.1*
%{_mandir}/man1/systemd-nspawn.1*
%{_mandir}/man1/systemd-loginctl.1*
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
%{_mandir}/man5/systemd.automount.5*
%{_mandir}/man5/systemd.conf.5*
%{_mandir}/man5/systemd.device.5*
%{_mandir}/man5/systemd.exec.5*
%{_mandir}/man5/systemd.mount.5*
%{_mandir}/man5/systemd.path.5*
%{_mandir}/man5/systemd.service.5*
%{_mandir}/man5/systemd.snapshot.5*
%{_mandir}/man5/systemd.socket.5*
%{_mandir}/man5/systemd.swap.5*
%{_mandir}/man5/systemd.target.5*
%{_mandir}/man5/systemd.timer.5*
%{_mandir}/man5/systemd.unit.5*
%{_mandir}/man5/systemd-logind.conf.5*
%{_mandir}/man5/timezone.5*
%{_mandir}/man5/vconsole.conf.5*
%{_mandir}/man7/daemon.7*
%{_mandir}/man7/sd-daemon.7*
%{_mandir}/man7/sd-readahead.7*
%{_mandir}/man7/systemd.special.7*
%{_mandir}/man8/halt.8*
%{_mandir}/man8/poweroff.8
%{_mandir}/man8/reboot.8
%{_mandir}/man8/runlevel.8*
%{_mandir}/man8/shutdown.8*
%{_mandir}/man8/telinit.8*

%if %{with pam}
%attr(755,root,root) /%{_lib}/security/pam_systemd.so
%{_mandir}/man8/pam_systemd.8*
%endif

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) /%{_lib}/libsystemd-daemon.so.*.*.*
%attr(755,root,root) %ghost /%{_lib}/libsystemd-daemon.so.0
%attr(755,root,root) /%{_lib}/libsystemd-login.so.*.*.*
%attr(755,root,root) %ghost /%{_lib}/libsystemd-login.so.0

%files units
%defattr(644,root,root,755)
%dir %{_sysconfdir}/binfmt.d
%dir %{_sysconfdir}/modules-load.d
%config(noreplace,missingok) %verify(not md5 mtime size) %{_sysconfdir}/modules-load.d/modules.conf
%dir %{_sysconfdir}/sysctl.d
%dir %{_sysconfdir}/systemd
%dir %{_sysconfdir}/systemd/system
%dir %{_sysconfdir}/tmpfiles.d
%dir /lib/systemd
%config(noreplace,missingok) %verify(not md5 mtime size) /lib/systemd/system
%dir %{_libexecdir}/binfmt.d
%dir %{_libexecdir}/modules-load.d
%dir %{_libexecdir}/sysctl.d
%dir %{_libexecdir}/tmpfiles.d
%attr(755,root,root) /bin/systemctl
%attr(755,root,root) /bin/systemd-tmpfiles
%{_mandir}/man5/tmpfiles.d.5*
%{_mandir}/man1/systemctl.1*
%{_mandir}/man8/systemd-tmpfiles.8*
%{_npkgconfigdir}/systemd.pc

%if %{with gtk}
%files gtk
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/systemadm
%attr(755,root,root) %{_bindir}/systemd-gnome-ask-password-agent
%{_mandir}/man1/systemadm.1*
%endif

%files -n bash-completion-systemd
%defattr(644,root,root,755)
/etc/bash_completion.d/systemctl-bash-completion.sh

%files devel
%defattr(644,root,root,755)
%{_includedir}/systemd
%{_libdir}/libsystemd-daemon.so
%{_libdir}/libsystemd-login.so
%{_pkgconfigdir}/libsystemd-daemon.pc
%{_pkgconfigdir}/libsystemd-login.pc
