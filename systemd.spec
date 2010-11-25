#
# TODO:
# - gtk BRs: libnotify 0.7 and gtk+3
# - subpackages: bash-autocompletion, dbus(?), gtk, others?
# - more BRs
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
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	dbus-devel
%if %{with gtk}
BuildRequires:	libnotify-devel >= 0.7.0
%endif
BuildRequires:	libtool
BuildRequires:	udev-devel >= 160
BuildRequires:	vala >= 0.11
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
%{__autoconf}
%{__automake}
%configure \
	--with-distro=other \
	--%{?with_gtk:en}%{!?with_gtk:dis}able-gtk \
	--with-syslog-service=syslog-ng \
	--with-sysvinit-path=/etc/rc.d/init.d \
	--with-sysvrcd-path=/etc/rc.d \
	--with-rootdir=/usr

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc DISTRO_PORTING README TODO
%attr(755,root,root) %{_bindir}/systemctl
%attr(755,root,root) %{_bindir}/systemd
%attr(755,root,root) %{_bindir}/systemd-ask-password
%attr(755,root,root) %{_bindir}/systemd-cgls
%attr(755,root,root) %{_bindir}/systemd-notify
%attr(755,root,root) %{_bindir}/systemd-tty-ask-password-agent
%{_prefix}/lib/systemd/
/etc/dbus-1/system.d/org.freedesktop.systemd1.conf
%{_sysconfdir}/systemd/system.conf
%{_sysconfdir}/systemd/system/getty.target.wants/getty@tty1.service
%{_sysconfdir}/systemd/system/getty.target.wants/getty@tty2.service
%{_sysconfdir}/systemd/system/getty.target.wants/getty@tty3.service
%{_sysconfdir}/systemd/system/getty.target.wants/getty@tty4.service
%{_sysconfdir}/systemd/system/getty.target.wants/getty@tty5.service
%{_sysconfdir}/systemd/system/getty.target.wants/getty@tty6.service
%{_sysconfdir}/systemd/system/local-fs.target.wants/quotacheck.service
%{_sysconfdir}/systemd/system/local-fs.target.wants/quotaon.service
%{_sysconfdir}/systemd/system/multi-user.target.wants/remote-fs.target
%{_sysconfdir}/systemd/system/sysinit.target.wants/hwclock-load.service
%{_sysconfdir}/tmpfiles.d/systemd.conf
%{_sysconfdir}/tmpfiles.d/x11.conf
%{_sysconfdir}/xdg/systemd/user
/lib/udev/rules.d/99-systemd.rules
%{_lib}/security/pam_systemd.la
%attr(755,root,root) %{_lib}/security/pam_systemd.so
%{_datadir}/dbus-1/interfaces/org.freedesktop.systemd1.Automount.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.systemd1.Device.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.systemd1.Job.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.systemd1.Manager.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.systemd1.Mount.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.systemd1.Path.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.systemd1.Service.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.systemd1.Snapshot.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.systemd1.Socket.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.systemd1.Swap.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.systemd1.Target.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.systemd1.Timer.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.systemd1.Unit.xml
%{_datadir}/dbus-1/services/org.freedesktop.systemd1.service
%{_datadir}/dbus-1/system-services/org.freedesktop.systemd1.service
%{_mandir}/man1/init.1
%{_mandir}/man1/systemadm.1*
%{_mandir}/man1/systemctl.1*
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
%{_mandir}/man5/tmpfiles.d.5*
%{_mandir}/man5/vconsole.conf.5*
%{_mandir}/man7/daemon.7*
%{_mandir}/man7/sd-daemon.7*
%{_mandir}/man7/sd-readahead.7*
%{_mandir}/man7/systemd.special.7*
%{_mandir}/man8/halt.8*
%{_mandir}/man8/pam_systemd.8*
%{_mandir}/man8/poweroff.8
%{_mandir}/man8/reboot.8
%{_mandir}/man8/runlevel.8*
%{_mandir}/man8/shutdown.8*
%{_mandir}/man8/telinit.8*
%{_datadir}/polkit-1/actions/org.freedesktop.systemd1.policy
%{_datadir}/systemd
