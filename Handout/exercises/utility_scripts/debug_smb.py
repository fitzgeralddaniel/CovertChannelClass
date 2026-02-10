from scapy.all import *
import sys

def debug_print(pcap_file):
    pkts = rdpcap(pcap_file)
    for i, pkt in enumerate(pkts):
        if pkt.haslayer(TCP) and (pkt[TCP].sport == 445 or pkt[TCP].dport == 445):
            if pkt.haslayer(Raw):
                payload = pkt[Raw].load
                print(f"Packet {i}: {payload[:50]}")
                if b'\xffSMB' in payload:
                    offset = payload.find(b'\xffSMB')
                    print(f"  SMB Header found at offset {offset}")
                    if len(payload) >= offset + 32:
                         mid = int.from_bytes(payload[offset+30:offset+32], byteorder='little')
                         print(f"  Mid: {mid}")

if __name__ == "__main__":
    debug_print(sys.argv[1])
