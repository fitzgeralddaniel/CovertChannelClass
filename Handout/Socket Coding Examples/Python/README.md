# Python Socket Programming Example

## Usage

You will need to run each of these in a separate terminal.

Make sure to run the receiver first. It will hang and wait for a connection.

**Receiver:**
```bash
python3 receiver.py <host_ip> <port> <buffer_size>
```
- `<host_ip>`: The IP address to listen on (e.g., `127.0.0.1` for localhost).
- `<port>`: The port number to listen on (e.g., `8080`).
- `<buffer_size>`: The size of the buffer for incoming data (e.g., `1024`).

Example:
```bash
python3 receiver.py 127.0.0.1 8080 1024
```

**Sender:**
```bash
python3 sender.py <host_ip> <port> <message>
```
- `<host_ip>`: The IP address of the receiver.
- `<port>`: The port the receiver is listening on.
- `<message>`: The string of text to send.

Example:
```bash
python3 sender.py 127.0.0.1 8080 "Hello from Python!"
```

## Troubleshooting

- **`python3: command not found`**: Ensure Python 3 is installed. On Debian/Ubuntu: `sudo apt update && sudo apt install python3`.
- **`Address already in use`**: The port is occupied. Try a different port or wait for it to clear.
- **`ConnectionRefusedError`**: The sender failed to connect. Ensure the receiver is running and listening on the correct IP/Port.

## Notes

- **Buffer Size**: Similar to the C example, `buffer_size` limits how much data is read at once. Python's `socket.recv(size)` reads *up to* `size` bytes.
- **Encoding**: The sender encodes strings to UTF-8 bytes (`data.encode('utf-8')`) before sending, and the receiver decodes them back (`data.decode('utf-8')`).
