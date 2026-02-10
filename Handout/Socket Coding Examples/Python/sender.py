import socket
import argparse

def send_data(data, host, port):
    """
    Sends data from a buffer over TCP to the specified host and port.

    Args:
        data (str): The data to be sent.
        host (str): The host to send the data to.
        port (int): The port to send the data to.
    """
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the host and port
    server_address = (host, port)
    try:
        sock.connect(server_address)
    except ConnectionRefusedError:
        print(f"Error: Could not connect to {host}:{port}. Is the receiver running?")
        return

    try:
        # Send data
        # encode() converts string to bytes to send over the wire
        sock.sendall(data.encode('utf-8'))
        print(f"Data sent: {data}")
    finally:
        # Close the socket
        sock.close()

def main():
    parser = argparse.ArgumentParser(description="TCP Sender Example")
    parser.add_argument("host", help="The host to connect to (e.g., 127.0.0.1)")
    parser.add_argument("port", type=int, help="The port to connect to")
    parser.add_argument("data", help="The data string to send")
    
    args = parser.parse_args()

    send_data(args.data, args.host, args.port)

if __name__ == "__main__":
    main()

