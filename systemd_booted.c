#include "sd-daemon.h"

int main(int argc, char*argv[]) {
	return (sd_booted() > 0) ? 0 : 1;
}
