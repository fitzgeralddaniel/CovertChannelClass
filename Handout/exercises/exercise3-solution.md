# Exercise 3 Solution: IP Type of Service (TOS) Field

## Analysis
To find the covert channel in this pcap, a student should:
1.  Open `Exercise3-client.pcapng` (or server pcap) in Wireshark.
2.  Filter for traffic between `192.168.1.3` and `192.168.1.9`.
3.  Observe the TCP SYN packets sent to port 80 (which are rejected with RST).
4.  Inspect the **IP Header** of these SYN packets.
5.  Notice the **Type of Service (TOS)** or **Differentiated Services Field** (DSCP) varies between packets. In normal traffic, this is usually constant (e.g., 0x00) or consistent for a flow.
6.  The TOS values correspond directly to ASCII characters.

## Covert Channel
**Mechanism**: Storage Covered Channel / Header Manipulation
**Location**: IP Protocol, **Type of Service (TOS)** field (8-bit).
**Encoding**: Direct ASCII encoding (one character per packet).

## Message
The decoded message is:
`sent.txt`

## Wetzel Pattern
This fits the **Header Manipulation** pattern (specifically identifying unused or mutable header fields like TOS).

## Metrics
*   **Bandwidth**: Low (8 bits per packet).
*   **Stealth**: Moderate. Non-zero TOS values are not uncommon, but a sequence of varying values in a short scan might trigger anomaly detection. The use of SYN packets to a closed port (scanning behavior) is also noisy.
