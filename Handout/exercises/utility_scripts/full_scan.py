from scapy.all import *
import sys

def scan_full(pcap):
    pkts = rdpcap(pcap)
    print(f"Loaded {len(pkts)} packets.")
    found = False
    for i, pkt in enumerate(pkts):
        if pkt.haslayer(TCP) and (pkt[TCP].sport == 445 or pkt[TCP].dport == 445):
            if pkt.haslayer(Raw):
                payload = pkt[Raw].load
                if b'\xffSMB' in payload:
                    idx = payload.find(b'\xffSMB')
                    # Mid is at idx + 30
                    if len(payload) >= idx + 32:
                        mid = int.from_bytes(payload[idx+30:idx+32], byteorder='little')
                        print(f"Packet {i}: SMB Header found. Mid={mid}")
                        if mid == 81:
                            print(f"Possible DoublePulsar found in Packet {i}!")
                            found = True
                
    if not found:
        print("No standard DoublePulsar (Mid=81) found.")

if __name__ == "__main__":
    scan_full(sys.argv[1])
