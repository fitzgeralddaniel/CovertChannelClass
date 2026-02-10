/**
 * @file sender.c
 * @brief TCP sender example.
 *
 * This program connects to a specified host and port and sends a message string.
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>

/**
 * @brief Sends data over a TCP connection.
 *
 * Establishes a connection to the server and sends the provided data buffer.
 *
 * @param data The null-terminated string to send.
 * @param host The target host IP address.
 * @param port The target port number.
 */
void send_data(char *data, char *host, int port)
{
    int sock;
    struct sockaddr_in server_address;

    /* Create a TCP/IP socket */
    sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock == -1) {
        perror("socket");
        exit(1);
    }

    /* Set up the server address structure */
    memset(&server_address, 0, sizeof(server_address));
    server_address.sin_family = AF_INET;
    server_address.sin_port = htons(port);
    server_address.sin_addr.s_addr = inet_addr(host);

    /* Connect the socket to the host and port */
    if (connect(sock, (struct sockaddr *)&server_address, sizeof(server_address)) == -1) {
        perror("connect");
        exit(1);
    }

    /* Send data */
    if (send(sock, data, strlen(data), 0) == -1) {
        perror("send");
        exit(1);
    }

    /* Close the socket */
    close(sock);
}

int main(int argc, char *argv[])
{
    char *host;
    int port;
    char *data;

    if (argc != 4) {
        fprintf(stderr, "Usage: %s <host> <port> <data>\n", argv[0]);
        exit(1);
    }

    host = argv[1];
    port = atoi(argv[2]);
    data = argv[3];

    send_data(data, host, port);

    return 0;
}