import sys
from scapy.all import *

def analyze_exercise1(pcap_file):
    print(f"Analyzing {pcap_file} for IP ID Covert Channel...")
    
    try:
        packets = rdpcap(pcap_file)
    except Exception as e:
        print(f"Error reading pcap: {e}")
        return

    extracted_chars = []
    
    # Based on initial analysis, the covert channel is in the IP ID field
    # of packets from 172.16.255.1 to 67.215.65.132.
    # The IDs are directly ASCII values.
    
    for pkt in packets:
        if pkt.haslayer(IP) and pkt.haslayer(ICMP):
            if pkt[IP].src == "172.16.255.1" and pkt[IP].dst == "67.215.65.132":
                 ip_id = pkt[IP].id
                 # Filter for printable ASCII just to be clean, 
                 # though we could print everything.
                 if 32 <= ip_id <= 126:
                     extracted_chars.append(chr(ip_id))

    message = "".join(extracted_chars)
    if message:
        print(f"\nSUCCESS: Extracted message from IP ID fields.")
        print(f"Message: {message}")
        print("Covert Channel: Data embedded in the 16-bit IP Identification field.")
    else:
        print("\nFAILURE: Could not extract message.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 exercise1-solver.py <pcap_file>")
        sys.exit(1)
    analyze_exercise1(sys.argv[1])
