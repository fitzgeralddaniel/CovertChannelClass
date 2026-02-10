import sys
from scapy.all import *

def analyze_exercise3(pcap_file):
    print(f"Analyzing {pcap_file} for IP TOS Covert Channel...")
    
    try:
        packets = rdpcap(pcap_file)
    except Exception as e:
        print(f"Error reading pcap: {e}")
        return

    extracted_chars = []
    
    print("Debug: Extracted characters:")
    for i, pkt in enumerate(packets):
        if pkt.haslayer(IP) and pkt.haslayer(TCP):
            if pkt[IP].src == "192.168.1.3" and pkt[IP].dst == "192.168.1.9":
                 tos = pkt[IP].tos
                 if 32 <= tos <= 126:
                     char = chr(tos)
                     extracted_chars.append(char)
                     sys.stdout.write(char)
                     sys.stdout.flush()
    print("\n")

    message = "".join(extracted_chars)
    if message:
        print(f"\nFinal Message: {message}")
    else:
        print("\nFAILURE: Maybe no matching packets?")

if __name__ == "__main__":
    analyze_exercise3(sys.argv[1])
