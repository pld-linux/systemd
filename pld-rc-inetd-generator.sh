#!/bin/sh
#
# TODO:
#	pre_start_service() and pre_stop_service()
#
parse_one_service() {
	SOCKET_FILE="${CURRENT_SERVICE}.socket"
	SERVICE_FILE="${CURRENT_SERVICE}.service"

	case "$FAMILY" in
		ipv4)
			PORT="0.0.0.0:$PORT"
			;;
		ipv6)
			PORT="[::]:$PORT"
			;;
		*)
	esac

	case "$SOCK_TYPE" in
		stream)
			[ "$PROTOCOL" = "tcp" ] || return
			__LISTEN="ListenStream=$PORT"
			;;
		dgram)
			[ "$PROTOCOL" = "udp" ] || return
			__LISTEN="ListenDatagram=$PORT"
			;;
		seqpacket)
			__LISTEN="ListenSequentialPacket=$PORT"
			;;
		*)
			return
	esac
	:>$SOCKET_FILE
	:>$SERVICE_FILE

	echo "[Unit]" >>$SERVICE_FILE
	echo "Description=$SERVICE_NAME" >>$SERVICE_FILE
	echo >>$SERVICE_FILE
	echo "[Service]" >>$SERVICE_FILE

	echo "[Unit]" >>$SOCKET_FILE
	echo "Description=$SERVICE_NAME" >>$SOCKET_FILE
	echo >>$SOCKET_FILE
	echo "[Socket]" >>$SOCKET_FILE
	echo $__LISTEN >>$SOCKET_FILE

	for i in $FLAGS; do
		case "$i" in
			wait)
				echo "Accept=true" >>$SOCKET_FILE
				;;
			nowait)
				[ "${MAX_CONNECTIONS:-n}" = "n" ] || echo "MaxConnections=$MAX_CONNECTIONS" >>$SOCKET_FILE
				;;
			*)
				;;
		esac
	done

	if [ "$SERVER" = "tcpd" ] ; then
		echo "TCPWrapName=$SERVICE_NAME" >>$SOCKET_FILE
	elif [ $SERVER != $DAEMON ]; then
		DAEMON="$SERVER $DAEMON"
	fi
	[ "${INTERFACE:-none}" = "none" ] || echo "BindToDevice=$INTERFACE" >>$SOCKET_FILE

	echo "User=$USER" >>$SERVICE_FILE
	[ "${GROUP:-none}" = "none" ] || echo "Group=$GROUP" >>$SERVICE_FILE
	[ "${NICE:-none}" = "none" ] || echo "Nice=$NICE" >>$SERVICE_FILE
	[ "${CHROOT:-none}" = "none" ] || echo "RootDirectory=$CHROOT" >>$SERVICE_FILE
	[ "${ENV:-none}" = "none" ] || echo "Environment=$ENV" >>$SERVICE_FILE
	echo -n "ExecStart=$DAEMON" >>$SERVICE_FILE
	if [ "${DAEMONARGS:-none}" = "none" ] ; then
		echo >>$SERVICE_FILE
	else
		echo "$DAEMONARGS" >>$SERVICE_FILE
	fi

	echo >>$SERVICE_FILE
	echo "[Install]" >>$SERVICE_FILE
	echo "Also=${CURRENT_SERVICE}.socket" >>$SERVICE_FILE
	echo >>$SERVICE_FILE

	echo >>$SOCKET_FILE
	echo "[Install]" >>$SOCKET_FILE
	echo "WantedBy=sockets.target" >>$SOCKET_FILE
}

SERVICES=$(ls -d /etc/sysconfig/rc-inetd/* 2>/dev/null | egrep -v '.*(\.rpm(save|new|orig)|~|CVS)')
for i in $SERVICES; do
	# unset everything
	unset SERVICE_NAME SOCK_TYPE PROTOCOL PORT USER
	unset DAEMON DAEMONARGS MAX_CONNECTIONS GROUP NICE
	unset FAMILY INTERFACE CHROOT RPCNAME RPCVERSION
	unset INITGROUPS BANNER ECHO FILTER ENV FLAGS
	unset SERVER MAX_CONNECTIONS_PER_SOURCE
	unset CONNECTIONS_PER_SECOND RPCNUMBER
	unset BANNER_SUCCESS BANNER_FAILURE PASSENV
	unset SERVICE_TYPE ACCESS_TIMES LOG_TYPE
	unset LOG_SUCCESS LOG_FAILURE REDIRECT MAX_LOAD
	# Read defaults...
	. /etc/sysconfig/rc-inetd.conf
	# ...and then config of *this* service.
	. $i
	CURRENT_SERVICE=`basename $i`
	DONT_PARSE=0
	# check if service is in deny list ?
	for i in $DENY_SERVICES ; do
		if [ $i = $CURRENT_SERVICE ] ; then
			DONT_PARSE=1
		fi
	done
	[ $DONT_PARSE -eq 0 ] || continue

	parse_one_service
done
