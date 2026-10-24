#!/bin/sh
# runlevel(8) for systemd as PID 1: derived from the active targets, the previous runlevel is
# not known ("N"); systemd >= 258 no longer records runlevels in utmp
for t in poweroff:0 reboot:6 graphical:5 multi-user:3 rescue:1; do
	if /bin/systemctl --quiet is-active "${t%:*}.target"; then
		echo "N ${t#*:}"
		exit 0
	fi
done
echo unknown
exit 1
