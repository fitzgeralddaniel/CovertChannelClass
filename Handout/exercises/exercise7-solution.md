# Exercise 7 Solution: UDP Checksum Covert Channel

## Analysis
To find the covert channel in this pcap, a student should:
1.  Open `Exercise7.pcap` in Wireshark or use `tcpdump -r Exercise7.pcap -n`.
2.  Observe that the traffic is entirely DNS: query/response pairs to well-known security domains (iana.org, isc.sans.org, tools.ietf.org, etc.).
3.  Note that all standard fields appear normal: IP ID is constant (`0x0001`), TOS is `0x00`, TTL is `64`, query class is `IN`, type is `A`. Response IPs and TTLs are consistent per domain.
4.  Perform a **hex dump** of the DNS query packets (`tshark -r Exercise7.pcap -x -c 2`).
5.  Notice the **UDP checksum** field at offset `0x28-0x29` contains values like `0x5361` ("Sa"), `0x7665` ("ve"), `0x2074` (" t")—these are ASCII character pairs!
6.  Extract the UDP checksum from each DNS query packet and decode both bytes as ASCII.

## Covert Channel
**Mechanism**: Storage Covert Channel / Header Manipulation
**Location**: UDP **Checksum** field (16-bit).
**Encoding**: Each checksum's high byte and low byte correspond to two ASCII characters. With 147 query packets, this yields a ~294 character message.

## Message
```
Save the date, SANS Boston starts August 1, 2016. Another notable event
occurred August 1, but in 1981.  The rock music video channel MTV made
its debut. The first person to decode this and show up and send the
message to stephen@sans.edu will receive a prize. Best of luck to you,
Judy Novak.
```

## Wetzel Pattern
This fits the **Header Manipulation** pattern. The UDP checksum field is repurposed to carry hidden data instead of an actual integrity check value.

## Metrics
*   **Bandwidth**: 16 bits (2 characters) per packet.
*   **Stealth**: **High**. The DNS queries and responses themselves look completely legitimate—real security-related domains with valid responses. The only anomaly is that the UDP checksums do not match the actual computed checksum, which would only be detected by a system explicitly validating UDP checksums (UDP checksum validation is often disabled or optional in IPv4). Most IDS/IPS systems ignore UDP checksum correctness.
