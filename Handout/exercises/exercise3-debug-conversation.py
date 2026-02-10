import sys
from scapy.all import *

def analyze_exercise3(pcap_file):
    print(f"Analyzing {pcap_file}...")
    
    try:
        packets = rdpcap(pcap_file)
    except Exception as e:
        print(f"Error reading pcap: {e}")
        return

    print("Packet Analysis (Full Conversation 192.168.1.3 <-> 192.168.1.9):")
    for i, pkt in enumerate(packets):
        if pkt.haslayer(IP) and (pkt[IP].src == "192.168.1.3" or pkt[IP].src == "192.168.1.9"):
            src = pkt[IP].src
            dst = pkt[IP].dst
            tos = pkt[IP].tos
            ip_id = pkt[IP].id
            info = ""
            if pkt.haslayer(TCP):
                info = f"TCP Flags={pkt[TCP].flags} Seq={pkt[TCP].seq} Ack={pkt[TCP].ack}"
            
            # ASCII helpers
            tos_char = chr(tos) if 32<=tos<=126 else '.'
            id_char = chr(ip_id % 256) if 32<=(ip_id % 256)<=126 else '.'
            
            print(f"Pkt {i+1}: {src}->{dst} TOS={tos}({tos_char}) ID={ip_id} {info}")

if __name__ == "__main__":
    analyze_exercise3(sys.argv[1])
