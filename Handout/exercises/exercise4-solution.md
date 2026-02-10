# Exercise 4 Solution: TCP Initial Sequence Number (ISN) Steganography

## Analysis
To find the covert channel in this pcap, a student should:
1.  Open `Exercise4.pcap` in Wireshark.
2.  Filter for TCP SYN packets (`tcp.flags.syn == 1`).
3.  Inspect the **Sequence Number** field.
4.  Notice that the Sequence Numbers are not random.
5.  If one looks at the Hexadecimal representation of the Sequence Number, the first byte (high byte) falls within the printable ASCII range.
6.  Extracting the high byte from each SYN packet reveals the message.

## Covert Channel
**Mechanism**: Storage Covered Channel / Header Manipulation
**Location**: TCP Protocol, **Sequence Number** field (32-bit). Specifically the most significant byte (MSB).
**Encoding**: The data is directly encoded into the top 8 bits of the 32-bit ISN. The process works by taking a character, shifting it left by 24 bits, and potentially adding random noise or a valid-looking sequence to the lower 24 bits (though in this specific case, the lower bits appear to be 0 or irrelevant).

## Message
The decoded message is the contents of a Linux `/etc/shadow` file, containing password hashes for users like `root`, `securitynik`, and `sansforensics`.

Partial content:
```
root:!16652:0:99999:7:::
daemon:*:16652:0:99999:7:::
...
securitynik:$6$NJW2GsFv$...
sansforensics:$6$Bz8.BXYs$...
```

## Wetzel Pattern
This fits the **Header Manipulation** pattern. The TCP Sequence Number is a required field, but the Initial Sequence Number (ISN) is supposed to be random to prevent TCP prediction attacks. Replacing bits of the ISN with data is a classic example of hiding data in protocol headers.

## Metrics
*   **Bandwidth**: Moderate/High for a covert channel. TCP headers are 20 bytes, and we are using 4 bytes (or just 1 byte in this specific encoding) per packet. Since SYN packets initiates connections, high volume of SYN packets might look suspicious (SYN Flood), but if interspersed with normal traffic, it can be effective.
*   **Stealth**: Moderate. Modern operating systems use specific algorithms to generate random ISNs (e.g., RFC 6528). A statistical analysis of ISNs would reveal that the distribution is not uniform (due to the ASCII bias in the MSB), making it detectable by sophisticated anomaly detection systems.
