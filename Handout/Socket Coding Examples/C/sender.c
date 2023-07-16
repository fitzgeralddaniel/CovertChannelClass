#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h> // added to use inet_addr()
#include <unistd.h>    // to use close()

void send_data(char *data, char *host, int port)
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
    server_address.sin_addr.s_addr = inet_addr(host);

    // Connect the socket to the host and port
    if (connect(sock, (struct sockaddr *)&server_address, sizeof(server_address)) == -1)
    {
        perror("connect");
        exit(1);
    }

    // Send data
    if (send(sock, data, strlen(data), 0) == -1)
    {
        perror("send");
        exit(1);
    }

    // Close the socket
    close(sock);
}

int main()
{
    // Hard-coded arguments
    char *data = "Hello, World!";
    char *host = "127.0.0.1";
    int port = 8080;

    // Call the send_data function
    send_data(data, host, port);

    return 0;
}