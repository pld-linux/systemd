/*
 * /run/initctl for SysVinit's shutdown, halt, reboot, poweroff and telinit running under
 * systemd as PID 1 (systemd >= 258 dropped its systemd-initctl). Socket-activated through
 * systemd-initctl.socket (ListenFIFO), maps runlevel requests to systemd targets.
 */
#include <errno.h>
#include <poll.h>
#include <signal.h>
#include <stdbool.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>

#include "systemd/sd-bus.h"
#include "systemd/sd-daemon.h"

/* struct init_request from sysvinit's initreq.h, 384 bytes */
#define INIT_MAGIC		0x03091969
#define INIT_CMD_RUNLVL		1
#define INIT_CMD_POWERFAIL	2
#define INIT_CMD_POWERFAILNOW	3
#define INIT_CMD_POWEROK	4
struct init_request {
	int magic;
	int cmd;
	int runlevel;
	int sleeptime;
	char data[368];
};
_Static_assert(sizeof(struct init_request) == 384, "init_request size");

/* exit when idle, the socket starts us again on the next request */
#define IDLE_TIMEOUT_MSEC	(30 * 1000)

static bool kexec_loaded(void) {
	char c = '0';
	FILE *f = fopen("/sys/kernel/kexec_loaded", "re");

	if (f) {
		if (fread(&c, 1, 1, f) != 1)
			c = '0';
		fclose(f);
	}
	return c == '1';
}

static int start_unit(const char *target, const char *mode) {
	sd_bus_error error = SD_BUS_ERROR_NULL;
	sd_bus *bus = NULL;
	int r;

	/* PID 1's private socket, works without dbus-daemon (early boot, rescue) */
	r = sd_bus_new(&bus);
	if (r >= 0)
		r = sd_bus_set_address(bus, "unix:path=/run/systemd/private");
	if (r >= 0)
		r = sd_bus_start(bus);
	if (r < 0) {
		fprintf(stderr, SD_ERR "Failed to connect to systemd: %s\n", strerror(-r));
		sd_bus_unref(bus);
		return r;
	}
	r = sd_bus_call_method(bus, "org.freedesktop.systemd1", "/org/freedesktop/systemd1",
			       "org.freedesktop.systemd1.Manager", "StartUnit", &error, NULL,
			       "ss", target, mode);
	if (r < 0)
		fprintf(stderr, SD_ERR "Failed to start %s: %s\n", target,
			error.message ? error.message : strerror(-r));
	sd_bus_error_free(&error);
	sd_bus_flush_close_unref(bus);
	return r;
}

/* returns true when we should exit (PID 1 is being reexecuted) */
static bool runlevel_request(int runlevel) {
	switch (runlevel) {
	case '0':
		start_unit("poweroff.target", "replace-irreversibly");
		break;
	case '6':
		start_unit(kexec_loaded() ? "kexec.target" : "reboot.target", "replace-irreversibly");
		break;
	case '1': case 's': case 'S':
		start_unit("rescue.target", "isolate");
		break;
	case '2': case '3': case '4':
		start_unit("multi-user.target", "isolate");
		break;
	case '5':
		start_unit("graphical.target", "isolate");
		break;
	case 'q': case 'Q':
		if (kill(1, SIGHUP) < 0)
			fprintf(stderr, SD_ERR "kill(1, SIGHUP): %s\n", strerror(errno));
		break;
	case 'u': case 'U':
		if (kill(1, SIGTERM) < 0)
			fprintf(stderr, SD_ERR "kill(1, SIGTERM): %s\n", strerror(errno));
		return true;
	default:
		fprintf(stderr, SD_WARNING "Unknown runlevel request '%c', ignoring.\n", runlevel);
	}
	return false;
}

int main(void) {
	int n, fd = SD_LISTEN_FDS_START;

	n = sd_listen_fds(1);
	if (n != 1) {
		fprintf(stderr, SD_ERR "Expected exactly one FIFO from socket activation, got %d.\n", n);
		return 1;
	}

	for (;;) {
		struct pollfd p = { .fd = fd, .events = POLLIN };
		struct init_request req;
		ssize_t l;

		n = poll(&p, 1, IDLE_TIMEOUT_MSEC);
		if (n < 0) {
			if (errno == EINTR)
				continue;
			fprintf(stderr, SD_ERR "poll(): %s\n", strerror(errno));
			return 1;
		}
		if (n == 0)
			return 0;

		l = read(fd, &req, sizeof(req));
		if (l < 0) {
			if (errno == EAGAIN || errno == EINTR)
				continue;
			fprintf(stderr, SD_ERR "read(): %s\n", strerror(errno));
			return 1;
		}
		if (l != (ssize_t) sizeof(req) || req.magic != INIT_MAGIC) {
			fprintf(stderr, SD_WARNING "Invalid initctl request, ignoring.\n");
			continue;
		}

		switch (req.cmd) {
		case INIT_CMD_RUNLVL:
			if (runlevel_request(req.runlevel))
				return 0;
			break;
		case INIT_CMD_POWERFAIL:
		case INIT_CMD_POWERFAILNOW:
		case INIT_CMD_POWEROK:
			fprintf(stderr, SD_WARNING "UPS power requests through initctl are not supported by systemd, use systemctl.\n");
			break;
		default:
			/* INIT_CMD_SETENV from shutdown(8) and friends: nothing to do */
			break;
		}
	}
}
