import socket

def send_data(data, host, port):
    """
    This function sends data from a buffer over TCP to the specified host and port.
    :param data: The data to be sent.
    :param host: The host to send the data to.
    :param port: The port to send the data to.
    """
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the host and port
    server_address = (host, int(port))
    sock.connect(server_address)

    try:
        # Send data
        # encode() converts string to bytes to send over the wire
        sock.sendall(data.encode('utf-8'))
        print("Data sent: " + data)
    finally:
        # Close the socket
        sock.close()

def main():
    # host variable is hardcoded to localhost (127.0.0.1), port is hardcoded to 8080
    # data is set to the single character "A"
    # Try changing these values or even allowing the user to input them at runtime or on the command line
    send_data("A", "127.0.0.1", "8080")

main()
