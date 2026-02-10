import socket
import argparse

def receive_data(host, port, buffer_size):
    """
    Receives data from TCP and returns it.

    Args:
        host (str): The host to bind to.
        port (int): The port to listen on.
        buffer_size (int): The size of the buffer to receive data into.

    Returns:
        bytes: The received data.
    """
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Allow address reuse to avoid "Address already in use" errors during testing
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind the socket to the host and port
    server_address = (host, port)
    sock.bind(server_address)

    # Listen for incoming connections
    sock.listen(1)
    print(f"Listening on {host}:{port}...")

    # Wait for a connection
    connection, client_address = sock.accept()
    print(f"Connection from {client_address}")

    try:
        # Receive data
        data = connection.recv(buffer_size)
        return data
    finally:
        # Clean up the connection
        connection.close()
        sock.close()

def main():
    parser = argparse.ArgumentParser(description="TCP Receiver Example")
    parser.add_argument("host", help="The host IP to bind to (e.g., 127.0.0.1)")
    parser.add_argument("port", type=int, help="The port to listen on")
    parser.add_argument("buffer_size", type=int, help="The receive buffer size")

    args = parser.parse_args()

    data = receive_data(args.host, args.port, args.buffer_size)
    print(f"Data received: {data.decode('utf-8')}")

if __name__ == "__main__":
    main()