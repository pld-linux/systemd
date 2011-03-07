#
# Conditional build:
%bcond_with		gtk	# build gtk tools (needs devel libnotify>=0.7 and gtk+3)
%bcond_without	selinux		# without SELinux support
%bcond_without	tcpd		# libwrap (tcp_wrappers) support
%bcond_without	pam			# PAM authentication support
%bcond_without	audit		# without audit support
%bcond_without	cryptsetup	# without cryptsetup support

Summary:	A System and Service Manager
Summary(pl.UTF-8):	systemd - zarządca systemu i usług dla Linuksa
Name:		systemd
Version:	19
Release:	0.1
License:	GPL v2+
Group:		Base
Source0:	http://www.freedesktop.org/software/systemd/%{name}-%{version}.tar.bz2
# Source0-md5:	32de12b132a2f6c270d422d682362a91
Patch0:		target-pld.patch
Patch1:		pld-port.patch
URL:		http://www.freedesktop.org/wiki/Software/systemd
%{?with_audit:BuildRequires:	audit-libs-devel}
BuildRequires:	autoconf
BuildRequires:	automake
%{?with_crypt:BuildRequires:	cryptsetup-luks-devel}
BuildRequires:	dbus-devel
BuildRequires:	docbook-style-xsl
%{?with_gtk:BuildRequires:	gtk+3-devel}
BuildRequires:	libcap-devel
%{?with_gtk:BuildRequires:	libnotify-devel >= 0.7}
%{?with_selinux:BuildRequires:	libselinux-devel}
BuildRequires:	libtool >= 2:2.2
%{?with_tcpd:BuildRequires:	libwrap-devel}
BuildRequires:	libxslt
%{?with_pam:BuildRequires:	pam-devel}
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.527
BuildRequires:	udev-devel >= 160
BuildRequires:	vala >= 0.11
Requires:	%{name}-units = %{version}-%{release}
Requires:	dbus >= 1.3.2
Requires:	rc-scripts
Requires:	udev-core >= 160
Provides:	SysVinit = 2.86-23
Provides:	readahead = 1:1.5.7-3
Provides:	virtual(init-daemon)
Obsoletes:	SysVinit < 2.86-23
Obsoletes:	readahead < 1:1.5.7-3
Obsoletes:	virtual(init-daemon)
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
zależnościach logikę kontroli usług. Może pracować jako zastępca dla
sysvinit.

%package units
Summary:	Configuration files, directories and installation tool for systemd
Group:		Base
Requires:	pkgconfig
Requires(post):	coreutils
Requires(post):	gawk

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

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__aclocal} -I m4
%{__autoconf}
%{__automake}
%configure \
	%{__enable_disable audit} \
	%{__enable_disable cryptsetup libcryptsetup} \
	%{__enable_disable gtk} \
	%{__enable_disable pam} \
	%{__enable_disable selinux} \
	%{__enable_disable tcpd tcpwrap} \
	--disable-silent-rules \
	--with-distro=pld \
	--with-syslog-service=syslog-ng \
	--with-rootdir=

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT '(' -name '*.a' -o -name '*.la' ')' | xargs -r rm -v

%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}

# no -devel (yet)
rm -f $RPM_BUILD_ROOT%{_npkgconfigdir}/systemd.pc

%if %{without gtk}
# to shut up check-files
rm -f $RPM_BUILD_ROOT%{_datadir}/polkit-1/actions/org.freedesktop.systemd1.policy
rm -f $RPM_BUILD_ROOT%{_bindir}/systemadm
rm -f $RPM_BUILD_ROOT%{_bindir}/systemd-gnome-ask-password-agent
rm -f $RPM_BUILD_ROOT%{_datadir}/polkit-1/actions/org.freedesktop.systemd1.policy
rm -f $RPM_BUILD_ROOT%{_mandir}/man1/systemadm.1*
%endif

# Create SysV compatibility symlinks. systemctl/systemd are smart
# enough to detect in which way they are called.
install -d $RPM_BUILD_ROOT/sbin
ln -s ../bin/systemd $RPM_BUILD_ROOT/sbin/init
ln -s ../bin/systemctl $RPM_BUILD_ROOT/sbin/reboot
ln -s ../bin/systemctl $RPM_BUILD_ROOT/sbin/halt
ln -s ../bin/systemctl $RPM_BUILD_ROOT/sbin/poweroff
ln -s ../bin/systemctl $RPM_BUILD_ROOT/sbin/shutdown
ln -s ../bin/systemctl $RPM_BUILD_ROOT/sbin/telinit
ln -s ../bin/systemctl $RPM_BUILD_ROOT/sbin/runlevel

# We create all wants links manually at installation time to make sure
# they are not owned and hence overriden by rpm after the used deleted
# them.
rm -r $RPM_BUILD_ROOT%{_sysconfdir}/systemd/system/*.target.wants

%clean
rm -rf $RPM_BUILD_ROOT

%post
/bin/systemctl daemon-reexec > /dev/null 2>&1 || :

%post units
if [ $1 -ne 1 ]; then
	exit 0
fi

# Try to read default runlevel from the old inittab if it exists
runlevel=$(/bin/awk -F ':' '$3 == "initdefault" && $1 !~ "^#" { print $2 }' /etc/inittab 2> /dev/null)
if [ -z "$runlevel" ] ; then
	runlevel=3
fi
target="/lib/systemd/system/runlevel$runlevel.target"

# And symlink what we found to the new-style default.target
ln -sf "$target" %{_sysconfdir}/systemd/system/default.target > /dev/null 2>&1 || :
#/bin/systemctl enable SERVICES > /dev/null 2>&1 || :

%preun units
if [ $1 -ne 0 ]; then
	exit 0
fi
#/bin/systemctl disable SERVICES > /dev/null 2>&1 || :
rm -f %{_sysconfdir}/systemd/system/default.target > /dev/null 2>&1 || :

%postun
if [ $1 -ge 1 ] ; then
	/bin/systemctl daemon-reload > /dev/null 2>&1 || :
fi

%files
%defattr(644,root,root,755)
%doc DISTRO_PORTING README TODO
/etc/dbus-1/system.d/org.freedesktop.systemd1.conf
%dir %{_sysconfdir}/systemd
%{_sysconfdir}/tmpfiles.d/systemd.conf
%{_sysconfdir}/tmpfiles.d/x11.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/systemd/system.conf
%dir /etc/xdg/systemd
/etc/xdg/systemd/user
%attr(755,root,root) /bin/systemd
%attr(755,root,root) /bin/systemd-ask-password
%attr(755,root,root) /bin/systemd-notify
%attr(755,root,root) /bin/systemd-tty-ask-password-agent
%attr(755,root,root) %{_bindir}/systemd-cgls
%attr(755,root,root) /sbin/halt
%attr(755,root,root) /sbin/init
%attr(755,root,root) /sbin/poweroff
%attr(755,root,root) /sbin/reboot
%attr(755,root,root) /sbin/runlevel
%attr(755,root,root) /sbin/shutdown
%attr(755,root,root) /sbin/telinit
%dir /lib/systemd
/lib/systemd/systemd-*
%dir /lib/systemd/system-generators
/lib/udev/rules.d/99-systemd.rules
%{_datadir}/dbus-1/interfaces/org.freedesktop.systemd1.*.xml
%{_datadir}/dbus-1/services/org.freedesktop.systemd1.service
%{_datadir}/dbus-1/system-services/org.freedesktop.systemd1.service
%{_datadir}/systemd
%{_mandir}/man1/init.1
%{_mandir}/man1/systemd-cgls.1*
%{_mandir}/man1/systemd-notify.1*
%{_mandir}/man1/systemd.1*
%{_mandir}/man3/sd_booted.3*
%{_mandir}/man3/sd_is_fifo.3*
%{_mandir}/man3/sd_is_socket.3
%{_mandir}/man3/sd_is_socket_inet.3
%{_mandir}/man3/sd_is_socket_unix.3
%{_mandir}/man3/sd_listen_fds.3*
%{_mandir}/man3/sd_notify.3*
%{_mandir}/man3/sd_notifyf.3
%{_mandir}/man3/sd_readahead.3*
%{_mandir}/man5/hostname.5*
%{_mandir}/man5/locale.conf.5*
%{_mandir}/man5/modules-load.d.5*
%{_mandir}/man5/os-release.5*
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

%if %{with cryptsetup}
/lib/systemd/system-generators/systemd-cryptsetup-generator
%endif

%if %{with pam}
%attr(755,root,root) /%{_lib}/security/pam_systemd.so
%{_mandir}/man8/pam_systemd.8*
%endif

%files units
%defattr(644,root,root,755)
%dir %{_sysconfdir}/systemd
%dir %{_sysconfdir}/systemd/system
%dir %{_sysconfdir}/tmpfiles.d
%dir /lib/systemd
/lib/systemd/system
%attr(755,root,root) /bin/systemctl
%attr(755,root,root) /bin/systemd-tmpfiles
%{_mandir}/man5/tmpfiles.d.5*
%{_mandir}/man1/systemctl.1*
%{_mandir}/man8/systemd-tmpfiles.8*

%if %{with gtk}
%files gtk
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/systemadm
%attr(755,root,root) %{_bindir}/systemd-gnome-ask-password-agent
%{_datadir}/polkit-1/actions/org.freedesktop.systemd1.policy
%{_mandir}/man1/systemadm.1*
%endif

%files -n bash-completion-systemd
%defattr(644,root,root,755)
/etc/bash_completion.d/systemctl-bash-completion.sh
