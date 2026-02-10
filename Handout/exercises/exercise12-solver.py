#!/usr/bin/env python3
"""
Exercise 12 Solver - Iodine DNS Tunnel Extraction

This pcap contains an iodine DNS tunnel to hillary.clinton.io.
Downstream data is carried in DNS NULL record responses.
Payloads are zlib-compressed TUN/TAP frames wrapping IPv4 packets.

The tunneled traffic reveals a brute-force password attack against
a custom login service on port 9999 at 45.55.178.79.
"""

import subprocess
import sys
import zlib
import struct
import os
import re
from collections import Counter

def get_pcap_path():
    if len(sys.argv) > 1:
        return sys.argv[1]
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "Exercise12.pcap")

def extract_dns_null_rdata(pcap_path):
    """Use tshark to extract DNS NULL record rdata from responses."""
    cmd = [
        "tshark", "-r", pcap_path,
        "-Y", "dns.resp.type == 10 && dns.flags.response == 1",
        "-T", "fields", "-e", "dns.null"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    records = []
    for line in result.stdout.strip().split('\n'):
        line = line.strip()
        if line:
            try:
                records.append(bytes.fromhex(line))
            except ValueError:
                pass
    return records

def decode_iodine_downstream(rdata_list):
    """
    Decode iodine downstream data packets.

    Frame format: 2-byte header + zlib-compressed TUN/TAP frame.
    TUN frame: 4-byte header (00 00 08 00) + IPv4 packet.
    """
    inner_packets = []
    for rdata in rdata_list:
        if len(rdata) < 10:
            continue
        # Find zlib header (0x78 0xda = best compression, 0x78 0x9c = default, etc.)
        for off in range(min(4, len(rdata))):
            if off < len(rdata) - 1 and rdata[off] == 0x78 and rdata[off+1] in (0x01, 0x5e, 0x9c, 0xda):
                try:
                    decompressed = zlib.decompress(rdata[off:])
                    # TUN header (00 00 08 00) + IPv4 (0x45)
                    if decompressed[:4] == b'\x00\x00\x08\x00' and len(decompressed) > 4 and decompressed[4] == 0x45:
                        inner_packets.append(decompressed[4:])
                    elif decompressed[0] == 0x45:
                        inner_packets.append(decompressed)
                except zlib.error:
                    pass
                break
    return inner_packets

def write_pcap(packets, output_path):
    """Write raw IPv4 packets to a pcap file (DLT_RAW)."""
    with open(output_path, 'wb') as f:
        f.write(struct.pack('<IHHiIII', 0xa1b2c3d4, 2, 4, 0, 0, 65535, 228))
        for i, pkt in enumerate(packets):
            f.write(struct.pack('<IIII', i, 0, len(pkt), len(pkt)))
            f.write(pkt)

def extract_text_from_packets(packets):
    """Extract readable text from TCP payloads."""
    text_chunks = []
    for pkt_data in packets:
        if len(pkt_data) < 40 or pkt_data[0] != 0x45:
            continue
        ihl = (pkt_data[0] & 0x0f) * 4
        protocol = pkt_data[9]
        if protocol == 6:  # TCP
            tcp_offset = (pkt_data[ihl + 12] >> 4) * 4
            payload = pkt_data[ihl + tcp_offset:]
            if payload:
                text_chunks.append(payload)
    return b''.join(text_chunks)

def main():
    pcap_path = get_pcap_path()
    print(f"[*] Analyzing: {pcap_path}")
    print(f"[*] This is an iodine DNS tunnel to hillary.clinton.io")
    print()

    # Step 1: Extract DNS NULL rdata
    print(f"[*] Extracting DNS NULL response data (downstream)...")
    rdata_list = extract_dns_null_rdata(pcap_path)
    print(f"    Found {len(rdata_list)} DNS NULL response records")

    # Step 2: Decode iodine frames
    print(f"[*] Decoding iodine downstream frames (zlib + TUN/TAP)...")
    inner_packets = decode_iodine_downstream(rdata_list)
    print(f"    Extracted {len(inner_packets)} inner IPv4 packets")

    # Step 3: Write tunnel pcap
    output_pcap = pcap_path.replace('.pcap', '_tunnel.pcap')
    write_pcap(inner_packets, output_pcap)
    print(f"[*] Wrote tunnel traffic to: {output_pcap}")

    # Step 4: Extract and analyze text content
    print()
    print(f"[*] Extracting text from tunneled TCP traffic...")
    raw_text = extract_text_from_packets(inner_packets)
    text = raw_text.decode('utf-8', errors='replace')

    # Find login results
    welcome_matches = re.findall(r'Welcome, (\w+)', text)
    denied_count = text.count('ACCESS DENIED!')

    print()
    print("=" * 60)
    print("COVERT CHANNEL: Iodine DNS Tunnel")
    print("=" * 60)
    print(f"  Domain:    hillary.clinton.io")
    print(f"  Protocol:  DNS NULL records (type 10)")
    print(f"  Encoding:  Base128 + zlib compression")
    print(f"  Tunnel IP: 10.0.0.1 <-> 10.0.0.2")
    print()
    print("TUNNELED ACTIVITY: Password Brute-Force Attack")
    print("-" * 60)
    print(f"  Target:    45.55.178.79:9999 (custom login service)")
    print(f"  Total login attempts: {denied_count + len(welcome_matches)}")
    print(f"  Failed (ACCESS DENIED): {denied_count}")
    print(f"  Successful (Welcome):   {len(welcome_matches)}")
    print()
    print("  Successful logins by username:")
    for name, count in Counter(welcome_matches).most_common():
        print(f"    - {name}: {count} times")
    print()
    print("=" * 60)

if __name__ == "__main__":
    main()
