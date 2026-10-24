#!/bin/sh
# telinit(8) for systemd as PID 1, runlevels mapped like systemd-initctl does
case "$1" in
0)	exec /bin/systemctl poweroff ;;
6)	exec /bin/systemctl reboot ;;
1|s|S)	exec /bin/systemctl isolate rescue.target ;;
2|3|4)	exec /bin/systemctl isolate multi-user.target ;;
5)	exec /bin/systemctl isolate graphical.target ;;
q|Q)	exec /bin/systemctl daemon-reload ;;
u|U)	exec /bin/systemctl daemon-reexec ;;
*)
	echo "Usage: telinit {0|1|2|3|4|5|6|s|S|q|Q|u|U}" >&2
	exit 1
	;;
esac
