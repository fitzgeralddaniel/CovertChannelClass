import sys
from scapy.all import *

def analyze_exercise3(pcap_file):
    print(f"Analyzing {pcap_file}...")
    try:
        packets = rdpcap(pcap_file)
    except Exception as e:
        print(f"Error reading pcap: {e}")
        return

    for i, pkt in enumerate(packets):
        if pkt.haslayer(IP) and pkt[IP].src == "192.168.1.3" and pkt[IP].dst == "192.168.1.9":
            # Check payload
            if pkt.haslayer(Raw):
                load = pkt[Raw].load
                print(f"Pkt {i+1}: Payload len={len(load)}")
                print(f"Payload: {load}")
            else:
                 # Check if TCP data offset implies data?
                 pass

if __name__ == "__main__":
    analyze_exercise3(sys.argv[1])
