/**
 * @file sender.c
 * @brief Raw TCP sender example.
 *
 * This program constructs and sends a raw TCP packet to a specified host and port.
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netinet/ip.h>
#include <netinet/tcp.h>
#include <arpa/inet.h>
#include <errno.h>

/**
 * @struct pseudo_header
 * @brief Pseudo-header for TCP checksum calculation.
 */
struct pseudo_header {
    u_int32_t source_address;
    u_int32_t dest_address;
    u_int8_t placeholder;
    u_int8_t protocol;
    u_int16_t tcp_length;
};

/**
 * @brief Sends a raw TCP packet.
 *
 * Constructs a custom IP and TCP header and sends the packet.
 * Note: Checksum calculation is simplified or offloaded to kernel/placeholder in this example context,
 * though typically raw sockets might require manual checksumming if not handled by OS.
 * For this assignment's context, we follow the existing pattern but clean it up.
 *
 * @param buffer The data to send.
 * @param size The size of the data.
 * @param src_ip Source IP address.
 * @param dest_ip Destination IP address.
 * @param src_port Source port.
 * @param dest_port Destination port.
 */
void send_data(const char *buffer, size_t size, char *src_ip, char *dest_ip, int src_port, int dest_port)
{
    int sockfd;
    struct sockaddr_in dest_addr;
    char packet[sizeof(struct ip) + sizeof(struct tcphdr) + size];
    struct ip *ip_header;
    struct tcphdr *tcp_header;
    int optval;

    /* Create a raw socket */
    sockfd = socket(AF_INET, SOCK_RAW, IPPROTO_RAW);
    if (sockfd < 0) {
        perror("socket");
        return;
    }

    /* IP_HDRINCL to tell the kernel that headers are included in the packet */
    optval = 1;
    if (setsockopt(sockfd, IPPROTO_IP, IP_HDRINCL, &optval, sizeof(optval)) < 0) {
        perror("setsockopt");
        close(sockfd);
        return;
    }

    /* Fill in the IP header */
    ip_header = (struct ip *)packet;
    ip_header->ip_hl = 5;
    ip_header->ip_v = 4;
    ip_header->ip_tos = 0;
    ip_header->ip_len = sizeof(struct ip) + sizeof(struct tcphdr) + size; /* Kernel will fix if needed but good practice */
    ip_header->ip_id = htons(12345); /* ID of this packet */
    ip_header->ip_off = 0;
    ip_header->ip_ttl = 64;
    ip_header->ip_p = IPPROTO_TCP;
    ip_header->ip_sum = 0; /* Let the kernel compute the checksum */
    ip_header->ip_src.s_addr = inet_addr(src_ip);
    ip_header->ip_dst.s_addr = inet_addr(dest_ip);

    /* Fill in the TCP header */
    tcp_header = (struct tcphdr *)(packet + sizeof(struct ip));
    tcp_header->th_sport = htons(src_port);
    tcp_header->th_dport = htons(dest_port);
    tcp_header->th_seq = 0;
    tcp_header->th_ack = 0;
    tcp_header->th_off = sizeof(struct tcphdr) / 4;
    tcp_header->th_flags = TH_SYN;
    tcp_header->th_win = htons(65535);
    tcp_header->th_sum = 0;
    tcp_header->th_urp = 0;

    /* Set the destination address */
    dest_addr.sin_family = AF_INET;
    dest_addr.sin_port = htons(dest_port);
    if (inet_pton(AF_INET, dest_ip, &(dest_addr.sin_addr)) <= 0) {
        perror("inet_pton");
        close(sockfd);
        return;
    }

    /* Copy data to the packet buffer */
    memcpy(packet + sizeof(struct ip) + sizeof(struct tcphdr), buffer, size);

    /* Send the packet */
    if (sendto(sockfd, packet, sizeof(struct ip) + sizeof(struct tcphdr) + size, 0, (struct sockaddr *)&dest_addr, sizeof(dest_addr)) < 0) {
        perror("sendto");
        close(sockfd);
        return;
    }

    close(sockfd);
}

int main(int argc, char *argv[])
{
    char *src_ip;
    char *dest_ip;
    int src_port;
    int dest_port;
    char *send_data_buffer;

    if (argc != 6) {
        fprintf(stderr, "Usage: %s <src_ip> <src_port> <dest_ip> <dest_port> <message>\n", argv[0]);
        exit(1);
    }

    src_ip = argv[1];
    src_port = atoi(argv[2]);
    dest_ip = argv[3];
    dest_port = atoi(argv[4]);
    send_data_buffer = argv[5];

    /* Send data */
    send_data(send_data_buffer, strlen(send_data_buffer), src_ip, dest_ip, src_port, dest_port);

    return 0;
}