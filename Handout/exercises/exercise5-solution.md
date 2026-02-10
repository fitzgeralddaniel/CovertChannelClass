# Exercise 5 Solution

## Analysis
The analysis began by examining the pcap file for unusual traffic patterns. A quick scan using `tcpdump` revealed a series of TCP packets with an unusual combination of flags: `SYN`, `ECE`, and `CWR` (shown as `SEW` or `SEC` in different tools).

```bash
tcpdump -r Handout/exercises/Exercise5.pcap -n -c 20
```

Output highlights:
```
17:26:30.962129 IP 127.0.0.1.1021 > 127.0.0.1.1020: Flags [SEW], seq 3474784256, win 512, length 0
```

These flags are typically negotiated during the TCP handshake for ECN (Explicit Congestion Notification) support, but seeing them repeatedly in this pattern is suspicious. Further inspection of the IP headers for these specific packets revealed that the `Identification` (IP ID) field contained varying values, while other fields like the Window size and Sequence numbers were either constant or less structured. Note that the sequence numbers do change, but the IP ID showed a more direct correlation to ASCII values in its high byte.

## Covert Channel
- **Mechanism**: Storage Channel in the IP Identification (ID) field.
- **Location**: The high byte of the 16-bit IP ID field in TCP packets with flags `SYN`, `ECE`, `CWR`.
- **Encoding**: The high byte corresponds to the ASCII value of the hidden character.

## Message
The hidden message extracted from the packets is:
`securitynik`

## Wetzel Pattern
- **Header Manipulation**: The channel actively manipulates the IP Identification field to store data. It also uses specific TCP flags to mark the covert packets, which is another form of header manipulation/signaling.

## Metrics
- **Bandwidth**: 8 bits per covert packet (1 character per packet).
- **Stealth**: 
    - **Medium**: While the traffic volume is low, the use of the `SYN+ECE+CWR` flag combination is highly anomalous and would likely be flagged by intrusion detection systems (IDS) as potential scanning or evasion attempts. The modification of the IP ID field itself is less obvious without deep packet inspection, but the flagging mechanism makes it vulnerable to detection.
