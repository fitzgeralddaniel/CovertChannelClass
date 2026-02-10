from scapy.all import *
import sys

def find_hidden_strings(pcap_file):
    packets = rdpcap(pcap_file)
    for i, pkt in enumerate(packets):
        payload = b""
        if pkt.haslayer(Raw):
            payload = pkt[Raw].load
        elif pkt.haslayer(ICMP):
             # sometimes load is part of ICMP but scapy handles it nicely
             pass 

        if not payload and pkt.haslayer(ICMP) and pkt[ICMP].type == 8: # Echo Request
             # Extract payload from ICMP if raw layer wasn't found (scapy usually puts it in Raw)
             pass

        if payload:
            try:
                # filter for printable ascii
                s = payload.decode('utf-8', errors='ignore')
                # basic heuristic: if it looks like a sentence or flag
                if len(s) > 5:
                    print(f"Packet {i+1}: " + s.replace('\n', ' '))
            except:
                pass

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 scanner.py <pcap>")
        sys.exit(1)
    find_hidden_strings(sys.argv[1])
