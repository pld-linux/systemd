#define _GNU_SOURCE
#include <libudev.h>
#include <linux/netlink.h>
#include <netinet/in.h>

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#ifndef SOCK_CLOEXEC
#define SOCK_CLOEXEC 0
#endif

#define	MONITOR_BUF_SIZE	4096
#define UDEV_MONITOR_MAGIC	0xfeedcafe
struct udev_monitor_netlink_header {
	/* "libudev" prefix to distinguish libudev and kernel messages */
	char prefix[8];
	/*
	 * magic to protect against daemon <-> library message format mismatch
	 * used in the kernel from socket filter rules; needs to be stored in network order
	 */
	unsigned int magic;
	/* total length of header structure known to the sender */
	unsigned int header_size;
	/* properties string buffer */
	unsigned int properties_off;
	unsigned int properties_len;
	/*
	 * hashes of primary device properties strings, to let libudev subscribers
	 * use in-kernel socket filters; values need to be stored in network order
	 */
	unsigned int filter_subsystem_hash;
	unsigned int filter_devtype_hash;
	unsigned int filter_tag_bloom_hi;
	unsigned int filter_tag_bloom_lo;
};

int main() {
	int sock=socket(PF_NETLINK, SOCK_RAW|SOCK_CLOEXEC|SOCK_NONBLOCK, NETLINK_KOBJECT_UEVENT);
	struct msghdr msg;
	struct iovec iov[2];
	char val[MONITOR_BUF_SIZE];
	ssize_t i;
	struct udev_monitor_netlink_header nlh;
	struct udev *udev;
	struct udev_enumerate *enumerate;
	struct udev_list_entry *devices, *dev_list_entry;
	struct udev_device *dev;
	struct sockaddr_nl dst;

	memset(&dst, 0 ,sizeof(dst));
	dst.nl_family= AF_NETLINK;
	dst.nl_pad=0;
	dst.nl_pid=1;
	dst.nl_groups=2;

	memset(&msg,0,sizeof(msg));
	msg.msg_iov = iov;
	msg.msg_iovlen = 2;
	msg.msg_name = &dst;
	msg.msg_namelen = sizeof(dst);

	memset(&nlh, 0, sizeof(nlh));
	memcpy(nlh.prefix, "libudev", 8);
	nlh.magic = htonl(UDEV_MONITOR_MAGIC);
	nlh.header_size = sizeof(nlh);
	iov[0].iov_base = &nlh;
	iov[0].iov_len = sizeof(nlh);
	nlh.properties_off = iov[0].iov_len;
	nlh.filter_tag_bloom_hi = htonl(0xffffffff);
	nlh.filter_tag_bloom_lo = htonl(0xffffffff);
	
	udev = udev_new();
	enumerate = udev_enumerate_new(udev);
//	udev_enumerate_add_match_subsystem(enumerate, "block");
	udev_enumerate_scan_devices(enumerate);
	devices = udev_enumerate_get_list_entry(enumerate);
	udev_list_entry_foreach(dev_list_entry, devices) {
		const char *path;
		path = udev_list_entry_get_name(dev_list_entry);
		dev = udev_device_new_from_syspath(udev, path);
		if(udev_device_get_devnum(dev)==0) continue;
		char *tmp;
		int l;
		i=0;
		l=asprintf(&tmp,"ACTION=add");					strcpy(val+i,tmp); i+=l+1; free(tmp);
		l=asprintf(&tmp,"DEVNAME=%s",udev_device_get_devnode(dev));	strcpy(val+i,tmp); i+=l+1; free(tmp);
		l=asprintf(&tmp,"DEVPATH=%s",udev_device_get_devpath(dev));	strcpy(val+i,tmp); i+=l+1; free(tmp);
		l=asprintf(&tmp,"DEVTYPE=%s",udev_device_get_devtype(dev));	strcpy(val+i,tmp); i+=l+1; free(tmp);
		l=asprintf(&tmp,"MAJOR=%u",major(udev_device_get_devnum(dev)));	strcpy(val+i,tmp); i+=l+1; free(tmp);
		l=asprintf(&tmp,"MINOR=%u",minor(udev_device_get_devnum(dev)));	strcpy(val+i,tmp); i+=l+1; free(tmp);
		l=asprintf(&tmp,"SEQNUM=%lld",udev_device_get_seqnum(dev));	strcpy(val+i,tmp); i+=l+1; free(tmp);
		l=asprintf(&tmp,"SUBSYSTEM=%s",udev_device_get_subsystem(dev));	strcpy(val+i,tmp); i+=l+1; free(tmp);
		l=asprintf(&tmp,"TAGS=:systemd:");				strcpy(val+i,tmp); i+=l+1; free(tmp);
		l=asprintf(&tmp,"UDEV_LOG=%u",udev_get_log_priority(udev));	strcpy(val+i,tmp); i+=l+1; free(tmp);
		l=asprintf(&tmp,"USEC_INITIALIZED=%lld",udev_device_get_usec_since_initialized(dev)); strcpy(val+i,tmp); i+=l+1; free(tmp);
		udev_device_unref(dev);
		iov[1].iov_base = val;
		iov[1].iov_len = i;
		nlh.properties_len = i;
		sendmsg(sock, &msg, 0);
	}
	udev_enumerate_unref(enumerate);
	udev_unref(udev);

	close(sock);
	return EXIT_SUCCESS;
}
