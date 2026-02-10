# C Socket Programming Example

## Compilation

To compile the `receiver`:
```bash
gcc -o receiver receiver.c
```

To compile the `sender`:
```bash
gcc -o sender sender.c
```

## Usage

You will need to run each of these in a separate terminal.

Make sure to run the receiver first. It should hang when it is running correctly and wait for you to run the sender.

**Receiver:**
```bash
./receiver <host_ip> <port> <buffer_size>
```
- `<host_ip>`: The IP address to listen on (e.g., `127.0.0.1` for localhost, or `0.0.0.0` for all interfaces).
- `<port>`: The port number to listen on (e.g., `8080`).
- `<buffer_size>`: The size of the buffer to allocate for incoming messages (e.g., `1024`). Larger buffers can handle larger messages but use more memory.

Example:
```bash
./receiver 127.0.0.1 8080 1024
```

**Sender:**
```bash
./sender <host_ip> <port> <message>
```
- `<host_ip>`: The IP address of the receiver.
- `<port>`: The port the receiver is listening on.
- `<message>`: The string of text to send.

Example:
```bash
./sender 127.0.0.1 8080 "Hello from C!"
```

## Troubleshooting

- **`gcc: command not found`**: You need a C compiler. On Debian/Ubuntu, run `sudo apt update && sudo apt install build-essential`.
- **`Address already in use`**: The port you are trying to bind to is already taken by another process. Try using a different port number (e.g., 8081) or wait a few moments.
- **`Connection refused`**: The sender cannot connect to the receiver.
  - Ensure the receiver is running *before* you run the sender.
  - Check that you are using the correct IP and port.
  - If running on different machines, check firewall settings.

## Notes

- **Buffer Size**: The `buffer_size` argument for the receiver determines the maximum amount of data it can read at once. If the sender sends more data than this, the message will be truncated in this simple example.
- **Blocking**: The `recv()` call in the receiver is blocking. It will wait indefinitely until data arrives.
