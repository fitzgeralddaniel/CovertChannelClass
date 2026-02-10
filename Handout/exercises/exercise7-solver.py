#!/usr/bin/env python3
"""
Exercise 7 Solver: UDP Checksum Covert Channel

The covert channel hides data in the UDP checksum field of DNS query packets.
Each checksum encodes 2 ASCII characters (high byte + low byte).
"""
from scapy.all import *
import sys


def solve(pcap_file):
    """Extract the hidden message from UDP checksums in DNS queries."""
    packets = rdpcap(pcap_file)
    message = ""

    for pkt in packets:
        if DNS in pkt and pkt[DNS].qr == 0:  # DNS query only
            checksum = pkt[UDP].chksum
            high_byte = (checksum >> 8) & 0xFF
            low_byte = checksum & 0xFF

            if high_byte > 0:
                message += chr(high_byte)
            if low_byte > 0:
                message += chr(low_byte)

    return message


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <pcap_file>")
        sys.exit(1)

    result = solve(sys.argv[1])
    print("=== Decoded Message ===")
    print(result)
