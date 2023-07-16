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

void packetHandler(unsigned char *packetData, int packetSize)
{
    // Decode the IP header
    struct ip *ip_header = (struct ip *)packetData;
    unsigned int ip_header_length = ip_header->ip_hl * 4; // Length of IP header in bytes

    // Decode the TCP header
    struct tcphdr *tcp_header = (struct tcphdr *)(packetData + ip_header_length);
    unsigned int tcp_header_length = tcp_header->th_off * 4; // Length of TCP header in bytes

    // Check the source IP address and destination port
    if (strcmp(inet_ntoa(ip_header->ip_src), "127.0.0.1") == 0 && ntohs(tcp_header->th_dport) == 54321)
    {
        printf("Packet captured\n");
        // You can access the raw packet data using the 'packetData' pointer here
        // You can print or process the packet data as needed

        // Decode the payload (data after the TCP header)
        unsigned char *payload = packetData + ip_header_length + tcp_header_length;
        int payload_length = packetSize - ip_header_length - tcp_header_length;

        // Print the source and destination IP addresses and ports
        printf("Source IP: %s\n", inet_ntoa(ip_header->ip_src));
        printf("Destination IP: %s\n", inet_ntoa(ip_header->ip_dst));
        printf("Source Port: %d\n", ntohs(tcp_header->th_sport));
        printf("Destination Port: %d\n", ntohs(tcp_header->th_dport));

        // Print the payload data as UTF-8 text
        printf("Payload: ");
        for (int i = 0; i < payload_length; i++)
        {
            printf("%c", payload[i]);
        }
        printf("\n");
    }
}
	


int main()
{
    int sockfd;
    struct sockaddr_in server_addr;
    unsigned char packet_buffer[65536];

    // Create a raw socket
    sockfd = socket(AF_INET, SOCK_RAW, IPPROTO_TCP);
    if (sockfd < 0)
    {
        perror("socket");
        return 1;
    }

    // Set socket options to receive all packets
    int option_value = 1;
    if (setsockopt(sockfd, IPPROTO_IP, IP_HDRINCL, &option_value, sizeof(option_value)) < 0)
    {
        perror("setsockopt");
        close(sockfd);
        return 1;
    }

    // Receive and process packets
    while (1)
    {
        int packet_size = recv(sockfd, packet_buffer, sizeof(packet_buffer), 0);
        if (packet_size < 0)
        {
            perror("recv");
            close(sockfd);
            return 1;
        }

        // Process the captured packet
        packetHandler(packet_buffer, packet_size);
    }

    // Close the socket
    close(sockfd);

    return 0;
}