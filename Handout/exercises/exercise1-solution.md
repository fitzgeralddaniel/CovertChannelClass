# Exercise 1 Solution: IP Identification Field

## Analysis
To find the covert channel in this pcap, a student should:
1.  Open `Exercise1.pcap` in Wireshark.
2.  Observe the ICMP Echo Request/Reply traffic between `172.16.255.1` and `67.215.65.132`.
3.  Inspect the **IP Header** of these packets.
4.  Notice that the **Identification** (IP ID) field values are unusual. In standard traffic, these increment sequentially. In this capture, they appear random or specific.
5.  If converted to ASCII, the IP IDs in the Echo Requests (`172.16.255.1` -> `67.215.65.132`) spell out a sentence.

## Covert Channel
**Mechanism**: Storage Covered Channel / Header Manipulation
**Location**: IP Protocol, **Identification** (ID) field (16-bit).
**Encoding**: Direct ASCII encoding (one character per packet ID).

## Message
The decoded message is:
`The password is 'goodjob'`

## Wetzel Pattern
This fits the **Header Manipulation** pattern (specifically identifying unused or malleable header fields like IP ID in ICMP traffic where fragmentation is not occurring).

## Metrics
*   **Bandwidth**: Low (16 bits per packet, or 8 bits if only using lower byte for ASCII).
*   **Stealth**: Moderate. While IP IDs can be random, a sequence of printable ASCII values is statistically anomalous and easily detected by heuristics properly tuned for distribution analysis.
