import socket

def receive_data(host, port, buffer_size):
    """
    This function receives data from TCP and writes it into a buffer.
    :param host: The host to receive data from.
    :param port: The port to receive data from.
    :param buffer_size: The size of the buffer to receive data into.
    :return: The received data.
    """
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the host and port
    server_address = (host, int(port))
    sock.bind(server_address)

    # Listen for incoming connections
    sock.listen(1)

    # Wait for a connection
    connection, client_address = sock.accept()

    try:
        # Receive data
        data = connection.recv(buffer_size)
        return data
    finally:
        # Clean up the connection
        connection.close()

def main():
    # host variable is hardcoded to localhost (127.0.0.1), port is hardcoded to 8080, and buffer_size of 50
    # Try changing these values or even allowing the user to input them at runtime or on the command line
    print("Data received: " + receive_data("127.0.0.1", "8080", 50).decode("utf-8"))

main()