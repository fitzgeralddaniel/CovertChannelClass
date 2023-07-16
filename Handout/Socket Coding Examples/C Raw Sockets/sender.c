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

#define SRC_IP "127.0.0.1"  // Source IP address
#define DEST_IP "127.0.0.1" // Destination IP address
#define SRC_PORT 12345      // Source port
#define DEST_PORT 54321     // Destination port

// Function to send data over TCP
void sendData(const char *buffer, size_t size)
{
    int sockfd;
    struct sockaddr_in dest_addr;
    char packet[sizeof(struct ip) + sizeof(struct tcphdr) + size];

    // Create a raw socket
    sockfd = socket(AF_INET, SOCK_RAW, IPPROTO_RAW);
    if (sockfd < 0)
    {
        perror("socket");
        return;
    }

    // Fill in the IP header
    struct ip *ip_header = (struct ip *)packet;
    ip_header->ip_hl = 5;
    ip_header->ip_v = 4;
    ip_header->ip_tos = 0;
    ip_header->ip_len = htons(sizeof(struct ip) + sizeof(struct tcphdr) + size);
    ip_header->ip_id = htons(12345); // ID of this packet
    ip_header->ip_off = 0;
    ip_header->ip_ttl = 64;
    ip_header->ip_p = IPPROTO_TCP;
    ip_header->ip_sum = 0; // Let the kernel compute the checksum
    ip_header->ip_src.s_addr = inet_addr(SRC_IP);
    ip_header->ip_dst.s_addr = inet_addr(DEST_IP);

    // Fill in the TCP header
    struct tcphdr *tcp_header = (struct tcphdr *)(packet + sizeof(struct ip));
    tcp_header->th_sport = htons(SRC_PORT);
    tcp_header->th_dport = htons(DEST_PORT);
    tcp_header->th_seq = 0;
    tcp_header->th_ack = 0;
    tcp_header->th_off = sizeof(struct tcphdr) / 4;
    tcp_header->th_flags = TH_SYN;
    tcp_header->th_win = htons(65535);
    tcp_header->th_sum = 0;
    tcp_header->th_urp = 0;

    // Set the destination address
    dest_addr.sin_family = AF_INET;
    dest_addr.sin_port = htons(DEST_PORT);
    if (inet_pton(AF_INET, DEST_IP, &(dest_addr.sin_addr)) <= 0)
    {
        perror("inet_pton");
        close(sockfd);
        return;
    }

    // Copy data to the packet buffer
    memcpy(packet + sizeof(struct ip) + sizeof(struct tcphdr), buffer, size);

    // Send the packet
    if (sendto(sockfd, packet, sizeof(struct ip) + sizeof(struct tcphdr) + size, 0, (struct sockaddr *)&dest_addr, sizeof(dest_addr)) < 0)
    {
        perror("sendto");
        close(sockfd);
        return;
    }

    close(sockfd);
}

int main()
{
    const char *sendDataBuffer = "Hello World!";

    // Send data
    sendData(sendDataBuffer, strlen(sendDataBuffer));

    return 0;
}