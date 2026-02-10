/**
 * @file receiver.c
 * @brief TCP receiver example.
 *
 * This program listens on a specified port and prints received data.
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <unistd.h>

/**
 * @brief Receives data from a TCP connection.
 *
 * Binds to a port, listens for a connection, receiving data into a buffer.
 *
 * @param host The host IP to bind to (not strictly used with INADDR_ANY, but passed for consistency).
 * @param port The port to listen on.
 * @param buffer_size The size of the receive buffer.
 * @param buffer The buffer to store received data.
 */
void receive_data(char *host, int port, int buffer_size, char *buffer)
{
    int sock;
    struct sockaddr_in server_address;
    struct sockaddr_in client_address;
    socklen_t client_address_len;
    int connection;
    ssize_t bytes_received;

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
    server_address.sin_addr.s_addr = htonl(INADDR_ANY);

    /* Bind the socket to the host and port */
    if (bind(sock, (struct sockaddr *)&server_address, sizeof(server_address)) == -1) {
        perror("bind");
        exit(1);
    }

    /* Listen for incoming connections */
    if (listen(sock, 1) == -1) {
        perror("listen");
        exit(1);
    }

    /* Wait for a connection */
    client_address_len = sizeof(client_address);
    connection = accept(sock, (struct sockaddr *)&client_address, &client_address_len);
    if (connection == -1) {
        perror("accept");
        exit(1);
    }

    /* Receive data */
    bytes_received = recv(connection, buffer, buffer_size - 1, 0);
    if (bytes_received == -1) {
        perror("recv");
        exit(1);
    }

    /* Null terminate the received data safely */
    if (bytes_received < buffer_size) {
        buffer[bytes_received] = '\0';
    } else {
        buffer[buffer_size - 1] = '\0';
    }
}

int main(int argc, char *argv[])
{
    char *host;
    int port;
    int buffer_size;
    char *buffer;

    if (argc != 4) {
        fprintf(stderr, "Usage: %s <host> <port> <buffer_size>\n", argv[0]);
        exit(1);
    }

    host = argv[1];
    port = atoi(argv[2]);
    buffer_size = atoi(argv[3]);

    /* Allocate memory for the buffer */
    buffer = malloc(sizeof(char) * buffer_size);
    if (buffer == NULL) {
        perror("malloc");
        exit(1);
    }

    receive_data(host, port, buffer_size, buffer);

    /* Print the received data */
    printf("Received data: %s\n", buffer);

    /* Free the buffer */
    free(buffer);

    return 0;
}