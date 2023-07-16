#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <unistd.h> // to use close()

void receive_data(char *host, int port, int buffer_size, char *buffer)
{
    // Create a TCP/IP socket
    int sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock == -1)
    {
        perror("socket");
        exit(1);
    }

    // Set up the server address structure
    struct sockaddr_in server_address;
    memset(&server_address, 0, sizeof(server_address));
    server_address.sin_family = AF_INET;
    server_address.sin_port = htons(port);
    server_address.sin_addr.s_addr = htonl(INADDR_ANY);

    // Bind the socket to the host and port
    if (bind(sock, (struct sockaddr *)&server_address, sizeof(server_address)) == -1)
    {
        perror("bind");
        exit(1);
    }

    // Listen for incoming connections
    if (listen(sock, 1) == -1)
    {
        perror("listen");
        exit(1);
    }

    // Wait for a connection
    struct sockaddr_in client_address;
    socklen_t client_address_len = sizeof(client_address);
    int connection = accept(sock, (struct sockaddr *)&client_address, &client_address_len);
    if (connection == -1)
    {
        perror("accept");
        exit(1);
    }

    // Receive data
    ssize_t bytes_received = recv(connection, buffer, buffer_size - 1, 0);
    if (bytes_received == -1)
    {
        perror("recv");
        exit(1);
    }
}

int main()
{
    // Hard-coded arguments
    char *host = "127.0.0.1";
    int port = 8080;
    int buffer_size = 1024;

    // Allocate memory for the buffer
    char *buffer = malloc(sizeof(char) * buffer_size);
    if (buffer == NULL)
    {
        perror("malloc");
        exit(1);
    }

    // Call the receive_data function
    receive_data(host, port, buffer_size, buffer);

    // Print the received data
    printf("Received data: %s\n", buffer);

    // Free the buffer
    free(buffer);

    return 0;
}