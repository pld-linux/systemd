#!/bin/sh

# Read functions
. /lib/rc-scripts/functions

if ! is_no "$DM_MULTIPATH" && [ -x /sbin/multipath ]; then
	modprobe -s dm-mod >/dev/null 2>&1
	modprobe -s dm-multipath >/dev/null 2>&1
	/sbin/multipath -v 0
	[ -x /sbin/kpartx ] && /sbin/dmsetup ls --target multipath --exec '/sbin/kpartx -u -a -p p'
fi

if [ -x /sbin/dmraid ]; then
	modprobe -s dm-mod >/dev/null 2>&1
	modprobe -s dm-mirror >/dev/null 2>&1
	dmraidsets=$(LC_ALL=C /sbin/dmraid -s -c -i)
	if [ "$?" = "0" ]; then
		oldIFS=$IFS
		IFS=$(echo -en "\n\b")
		for dmname in $dmraidsets ; do
			[[ "$dmname" = isw_* ]] && continue
			/sbin/dmraid -ay -i --rm_partitions -p "$dmname"
			[ -x /sbin/kpartx ] && /sbin/kpartx -u -a -p p "/dev/mapper/$dmname"
		done
		IFS=$oldIFS
	fi
fi

# Start any MD RAID arrays that haven't been started yet
[ -r /proc/mdstat ] && /sbin/mdadm -As --auto=yes --run 2>&1

if ! is_no "$LVM2" && [ -x /sbin/lvm ]; then
	modprobe -s dm-mod >/dev/null 2>&1
	run_cmd "Scanning for LVM volume groups" /sbin/lvm vgscan --ignorelockingfailure
	run_cmd "Activating LVM volume groups" /sbin/lvm vgchange -a y --sysinit
	/sbin/lvm vgmknodes --ignorelockingfailure
fi

exit 0
