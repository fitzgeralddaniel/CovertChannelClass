# Exercise 8 Solution

## Analysis
The initial analysis involved inspecting `Exercise8.pcap` with `tcpdump` and `tshark`.
The capture consists of ICMP Echo Request and Reply packets.

Looking closely at the ICMP Echo Requests:
```bash
tshark -r Handout/exercises/Exercise8.pcap -T fields -e frame.number -e ip.src -e icmp.type -e data.data
```

This revealed that each Echo Request (Type 8) contained a single byte of data in the payload, which corresponds to ASCII characters.

Another anomaly observed: The ICMP Sequence Number was always `1` for the requests, which is unusual for a standard ping (where sequence usually increments), but the primary covert channel here is the **Storage Channel in the ICMP Payload**.

## Covert Channel mechanism
- **Type**: Storage Channel
- **Location**: ICMP Echo Request Payload (Data)
- **Method**: Each packet carries one character of the hidden message in the data field.

## Hidden Message
The extracted message is:
`SuperSecretPass`

## Wetzel Pattern
This fits the **Protocol Manipulation** (specifically payload/storage) pattern, as the data field of the ICMP packet is used to carry a message instead of standard ping padding (or random data). It can also be classified under **Header/Storage** if one considers the payload as a field, though typically payload is considered data.

## Metrics
- **Bandwidth**: ~8 bits per packet (1 byte character).
- **Stealth**: Low. The payload is visible in cleartext if inspected. A standard ping usually has a fixed payload (like `abc...` or all zeros), so varying single-byte payloads are highly suspicious.
