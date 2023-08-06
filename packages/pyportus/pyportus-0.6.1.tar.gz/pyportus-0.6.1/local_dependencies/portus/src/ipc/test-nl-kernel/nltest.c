#include <linux/module.h>
#include <linux/netlink.h>
#include <linux/skbuff.h>
#include <linux/gfp.h>
#include <linux/kprobes.h>
#include <linux/ptrace.h>
#include <linux/time.h>
#include <net/sock.h>

#define MYMGRP 22

struct sock *nl_sk = NULL;
int nl_send_msg(unsigned long data, char *payload, size_t msg_size);
/* (type, len, socket_id) header
 * -----------------------------------
 * | Msg Type | Len (B)  | Uint32    |
 * | (2 B)    | (2 B)    | (32 bits) |
 * -----------------------------------
 * total: 8 Bytes
 */
struct __attribute__((packed, aligned(4))) CcpMsgHeader {
    uint16_t Type;
    uint16_t Len;
    uint32_t SocketId;
};

char * serialize_time_msg(struct timespec recv_time, struct timespec send_time){
	long recv_cut_nsec = (long)recv_time.tv_nsec;
	long send_cut_nsec = (long)send_time.tv_nsec;
	char * msg = kmalloc(sizeof(struct CcpMsgHeader) + 2*sizeof(struct timespec), GFP_USER);
	struct CcpMsgHeader hdr;

	hdr.Type = 0xFF - 1;
	hdr.Len = 8 + 2*(8 + 4);
	hdr.SocketId = 0;

	memcpy(msg, &hdr, sizeof(struct CcpMsgHeader));
	memcpy(msg + sizeof(struct CcpMsgHeader), &(recv_time.tv_sec), 8);
	memcpy(msg + sizeof(struct CcpMsgHeader) + 8, &recv_cut_nsec, 4);
	memcpy(msg + sizeof(struct CcpMsgHeader) + 12, &(send_time.tv_sec), 8);
	memcpy(msg + sizeof(struct CcpMsgHeader) + 20, &send_cut_nsec, 4);

	return msg;
}
/* Receive echo message from userspace 
 * Respond echo it back for checking
 */
void nl_recv_msg(struct sk_buff *skb) {
    int res;
	struct timespec recv_time;
	struct timespec send_time;

	getnstimeofday(&recv_time);
	getnstimeofday(&send_time);
    res = nl_send_msg(0, serialize_time_msg(recv_time, send_time), 8+2*(8+4));
    if (res < 0) {
        pr_info("nltest: echo send failed: %d\n", res);
    }
    printk(KERN_INFO "nltest: Got past send extra messages\n");
}


/* Send message to userspace
 */
int nl_send_msg(unsigned long data, char *payload, size_t msg_size) {
    struct sk_buff *skb_out;
    struct nlmsghdr *nlh;
    int res;


    skb_out = nlmsg_new(
        NLMSG_ALIGN(msg_size), // @payload: size of the message payload
        GFP_NOWAIT             // @flags: the type of memory to allocate.
    );
    if (!skb_out) {
        printk(KERN_ERR "nltest: Failed to allocate new skb\n");
        return -20;
    }

    nlh = nlmsg_put(
        skb_out,    // @skb: socket buffer to store message in
        0,          // @portid: netlink PORTID of requesting application
        0,          // @seq: sequence number of message
        NLMSG_DONE, // @type: message type
        msg_size,   // @payload: length of message payload
        0           // @flags: message flags
    );

    memcpy(nlmsg_data(nlh), payload, msg_size);
    res = nlmsg_multicast(
            nl_sk,     // @sk: netlink socket to spread messages to
            skb_out,   // @skb: netlink message as socket buffer
            0,         // @portid: own netlink portid to avoid sending to yourself
            MYMGRP,    // @group: multicast group id
            GFP_NOWAIT // @flags: allocation flags
    );

    return res;
}

static int nl_send_init_msg(void) {
    char *msg = "hello, netlink";
    struct CcpMsgHeader hdr = {
        .Type = 0xff,
        .Len = 24,
        .SocketId = 0,
    };
    char buf[23];

    memcpy(&buf, &hdr, sizeof(struct CcpMsgHeader));
    memcpy(&buf[8], msg, 15);

    return nl_send_msg(0, (char*)&buf, 23);
}

static int __init nl_init(void) {
    int res;
    struct netlink_kernel_cfg cfg = {
           .input = nl_recv_msg,
    };
    
    nl_sk = netlink_kernel_create(&init_net, NETLINK_USERSOCK, &cfg);
    if (!nl_sk) {
        printk(KERN_ALERT "nltest: Error creating socket.\n");
        return -10;
    }

    printk(KERN_INFO "nltest: Sending initial message");
    res = nl_send_init_msg();
    if (res < 0) {
        pr_info("send err: %d\n", res);
    }

    return 0;
}

static void __exit nl_exit(void) {
    netlink_kernel_release(nl_sk);
}

module_init(nl_init);
module_exit(nl_exit);

MODULE_LICENSE("GPL");
