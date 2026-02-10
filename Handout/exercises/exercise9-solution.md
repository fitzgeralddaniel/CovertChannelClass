# Exercise 9 Solution

## Analysis
Inspection of `Exercise9.pcap` reveals ICMP Echo Requests (Type 8) communicating between `10.0.2.4` and `10.0.2.8`. 
The most notable anomaly is the payload size and content. Each ICMP Echo Request contains exactly 1 byte of data in the payload.
The values of these bytes are small integers (0x02, 0x03, 0x05, 0x06, 0x07, etc.).

> [!NOTE]
> **Correction**: Initial analysis incorrectly filtered out null bytes (`0x00`) from the payload, assuming they were padding or empty. This resulted in a garbled partial message. The user correctly identified that the output should be readable ASCII and that the null bytes were significant (e.g., forming the low nibble `0x0` for characters like 'P'=`0x50` and 'p'=`0x70`). Correcting the script to validly process `0x00` revealed the true message.

By concatenating these bytes and treating every pair as a hexadecimal representation of an ASCII character (High Nibble, Low Nibble), a clear message emerges. For example, `0x05` followed by `0x03` forms `0x53` (ASCII 'S').

## Covert Channel
- **Mechanism**: Storage Channel in ICMP Payload.
- **Encoding**: Hexadecimal Nibbles. Two packets are required to transmit one ASCII character. The payload of the first packet represents the high nibble (4 bits), and the second payload represents the low nibble.

## Message
`SuperSecretPass`

## Wetzel Pattern
- **Pattern**: Storage Channel (specifically using the Data field).

## Metrics
- **Bandwidth**: 4 bits per packet (0.5 bytes per packet).
- **Stealth**: Low/Medium. While the traffic volume is low, the non-standard 1-byte payload size in ICMP is highly anomalous and easily detected by standard IDS signatures or manual inspection.
