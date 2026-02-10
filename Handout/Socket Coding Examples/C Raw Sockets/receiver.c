/**
 * @file receiver.c
 * @brief Raw socket packet sniffer.
 *
 * Captures raw TCP packets and filters based on source IP and destination port.
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
 * @brief Handles captured packets.
 *
 * Decodes IP and TCP headers, checks against filter criteria, and prints payload.
 *
 * @param packet_data Pointer to the captured packet data.
 * @param packet_size Total size of the captured packet.
 * @param filter_src_ip Source IP to filter by.
 * @param filter_dest_port Destination port to filter by.
 */
void packet_handler(unsigned char *packet_data, int packet_size, char *filter_src_ip, int filter_dest_port)
{
    struct ip *ip_header;
    struct tcphdr *tcp_header;
    unsigned int ip_header_length;
    unsigned int tcp_header_length;
    unsigned char *payload;
    int payload_length;
    int i;

    /* Decode the IP header */
    ip_header = (struct ip *)packet_data;
    ip_header_length = ip_header->ip_hl * 4; /* Length of IP header in bytes */

    /* Decode the TCP header */
    tcp_header = (struct tcphdr *)(packet_data + ip_header_length);
    tcp_header_length = tcp_header->th_off * 4; /* Length of TCP header in bytes */

    /* Check the source IP address and destination port */
    if (strcmp(inet_ntoa(ip_header->ip_src), filter_src_ip) == 0 && ntohs(tcp_header->th_dport) == filter_dest_port) {
        printf("Packet captured\n");
        /* You can access the raw packet data using the 'packet_data' pointer here */
        /* You can print or process the packet data as needed */

        /* Decode the payload (data after the TCP header) */
        payload = packet_data + ip_header_length + tcp_header_length;
        payload_length = packet_size - ip_header_length - tcp_header_length;

        /* Print the source and destination IP addresses and ports */
        printf("Source IP: %s\n", inet_ntoa(ip_header->ip_src));
        printf("Destination IP: %s\n", inet_ntoa(ip_header->ip_dst));
        printf("Source Port: %d\n", ntohs(tcp_header->th_sport));
        printf("Destination Port: %d\n", ntohs(tcp_header->th_dport));

        /* Print the payload data as UTF-8 text */
        printf("Payload: ");
        for (i = 0; i < payload_length; i++) {
            printf("%c", payload[i]);
        }
        printf("\n");
    }
}

int main(int argc, char *argv[])
{
    int sockfd;
    unsigned char packet_buffer[65536];
    int option_value;
    char *filter_src_ip;
    int filter_dest_port;
    int packet_size;

    if (argc != 3) {
        fprintf(stderr, "Usage: %s <source_ip_filter> <dest_port_filter>\n", argv[0]);
        exit(1);
    }

    filter_src_ip = argv[1];
    filter_dest_port = atoi(argv[2]);

    /* Create a raw socket */
    sockfd = socket(AF_INET, SOCK_RAW, IPPROTO_TCP);
    if (sockfd < 0) {
        perror("socket");
        return 1;
    }

    /* Set socket options to receive all packets */
    option_value = 1;
    if (setsockopt(sockfd, IPPROTO_IP, IP_HDRINCL, &option_value, sizeof(option_value)) < 0) {
        perror("setsockopt");
        close(sockfd);
        return 1;
    }

    /* Receive and process packets */
    while (1) {
        packet_size = recv(sockfd, packet_buffer, sizeof(packet_buffer), 0);
        if (packet_size < 0) {
            perror("recv");
            close(sockfd);
            return 1;
        }

        /* Process the captured packet */
        packet_handler(packet_buffer, packet_size, filter_src_ip, filter_dest_port);
    }

    /* Close the socket */
    close(sockfd);

    return 0;
}