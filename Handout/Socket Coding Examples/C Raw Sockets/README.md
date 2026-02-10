# C Raw Socket Programming Example

## What are Raw Sockets?
Raw sockets allow a process to have direct access to the underlying transport provider. Unlike standard sockets (where the kernel handles headers for you), raw sockets let you manipulate the IP and transport layer (TCP/UDP) headers directly. This is powerful for custom packet creation, network monitoring (sniffing), or implementing new protocols, but requires root privileges and careful handling of header fields.

In this example, the `sender` manually constructs IP and TCP headers to send a packet, and the `receiver` captures all packets and manually decodes the headers to find the relevant ones.

## Compilation

You can compile the examples using the provided `Makefile`:

```bash
make
```

Or manually using `gcc`:

To compile `receiver`:
```bash
gcc -o receiver receiver.c
```

To compile `sender`:
```bash
gcc -o sender sender.c
```

## Usage

You will need to run each of these in a separate terminal.

**Note:** You must use `sudo` because raw sockets require root privileges.
*(Unless using the provided Docker container with `--cap-add=NET_RAW`, in which case `sudo` is not needed).*

Make sure to run the receiver first.

**Receiver (Sniffer):**
Listens for packets from a specific source IP destined for a specific port.
```bash
sudo ./receiver <source_ip_filter> <dest_port_filter>
```
*(Or just `./receiver ...` if running in Docker)*

Example:
```bash
sudo ./receiver 127.0.0.1 54321
```

**Sender:**
Sends a custom packet with manually constructed IP/TCP headers.
```bash
sudo ./sender <source_ip> <source_port> <dest_ip> <dest_port> <message>
```
*(Or just `./sender ...` if running in Docker)*

Example:
```bash
sudo ./sender 127.0.0.1 12345 127.0.0.1 54321 "Hello Raw World!"
```

## Troubleshooting

- **`make: command not found`**: If you do not have `make` installed, you can use `gcc` directly as shown in the Compilation section.
- **`gcc: command not found`**: You need a C compiler. On Debian/Ubuntu, run `sudo apt update && sudo apt install build-essential`.
- **`Permission denied`**: Raw sockets require root privileges. Ensure you are using `sudo` when running the executables, or use `--cap-add=NET_RAW` if running in Docker.
- **`Address already in use`**: The port you are trying to bind to is already taken by another process. Try using a different port number (e.g., 54322) or wait a few moments.
- **Not knowing what IP/Port to use**:
    - For local testing, use the loopback address `127.0.0.1`.
    - For ports, use high numbers (1024-65535) to avoid conflict with system services.
    - Consistency is key: Ensure the `receiver` listens for the same IP/Port that the `sender` is configured to send to/from.

## Notes & Assumptions

- **Raw IP Access**: This code assumes the operating system allows raw socket access. Some containerized environments or restrictive security policies may block this.
- **Hardcoded Fields**:
    - **IP ID**: The IP header Identification field (`ip_id`) is hardcoded to `12345`. In typical traffic, this value is unique per packet (often incrementing or randomized) to aid in reassembly of fragmented packets. A constant ID could be a signature of this specific tool.
    - **TTL**: Time To Live is set to `64`.
    - **Window Size**: TCP Window size is fixed.
- **Checksums**:
    - **IP Checksum**: Set to `0` to let the kernel compute it (`ip_sum = 0`).
    - **TCP Checksum**: Set to `0`. In a real-world scenario, you would typically need to calculate the TCP pseudo-header checksum manually for the packet to be accepted by a strict network stack, though loopback interfaces often ignore checksum offloading or errors.
- **Security**: The receiver indiscriminately prints payloads of packets matching the filter. In a production environment, rigorous input validation and bound checking (beyond what is shown) would be necessary to prevent vulnerabilities.
