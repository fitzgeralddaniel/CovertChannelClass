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
    
    # Filter: 192.168.1.3:1234 -> 192.168.1.9:80
    # The covert channel is in the IP TOS field.
    
    for pkt in packets:
        if pkt.haslayer(IP) and pkt.haslayer(TCP):
            if pkt[IP].src == "192.168.1.3" and pkt[IP].dst == "192.168.1.9":
                 # Check TOS
                 tos = pkt[IP].tos
                 # Sometimes ECN bits (last 2 bits) might be involved or not. 
                 # 0x65 = 0110 0101. 
                 # 0x6e = 0110 1110.
                 # It seems the whole byte is used for ASCII?
                 
                 # Let's try to just decode TOS as char directly
                 if 32 <= tos <= 126:
                     extracted_chars.append(chr(tos))

    message = "".join(extracted_chars)
    if message:
        print(f"\nSUCCESS: Extracted message from IP TOS fields.")
        print(f"Message: {message}")
        print("Covert Channel: Data embedded in the 8-bit IP TOS/DSCP field.")
    else:
        print("\nFAILURE: Could not extract message.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 exercise3-solver.py <pcap_file>")
        sys.exit(1)
    analyze_exercise3(sys.argv[1])
