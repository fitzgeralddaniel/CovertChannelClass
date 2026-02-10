import sys
from scapy.all import *

def analyze_exercise3(pcap_file):
    print(f"Analyzing {pcap_file}...")
    
    try:
        packets = rdpcap(pcap_file)
    except Exception as e:
        print(f"Error reading pcap: {e}")
        return

    print("Packet Analysis (192.168.1.3 -> 192.168.1.9):")
    for i, pkt in enumerate(packets):
        if pkt.haslayer(IP) and pkt[IP].src == "192.168.1.3" and pkt[IP].dst == "192.168.1.9":
            # Print TOS, ID, Seq
            tos = pkt[IP].tos
            ip_id = pkt[IP].id
            seq = 0
            if pkt.haslayer(TCP):
                seq = pkt[TCP].seq
            
            print(f"Pkt {i+1}: TOS={tos} ({chr(tos) if 32<=tos<=126 else '?'}) ID={ip_id} SEQ={seq}")

if __name__ == "__main__":
    analyze_exercise3(sys.argv[1])
