#!/bin/sh
# Read functions
. /lib/rc-scripts/functions

# Clean /tmp
if is_yes "$CLEAN_TMP" && ! is_fsmounted tmpfs /tmp; then
	LC_ALL=C rm -rf /tmp/* /tmp/.[a-zA-Z0-9]*
fi
