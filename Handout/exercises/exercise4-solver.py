import sys
from scapy.all import *

def solve_exercise4(pcap_file):
    """
    Reads a pcap file and extracts a covert message hidden in the 
    high byte of the TCP Initial Sequence Number (ISN) of SYN packets.
    """
    print(f"[*] Analyzing {pcap_file}...")
    
    try:
        packets = rdpcap(pcap_file)
    except FileNotFoundError:
        print(f"[!] Error: File {pcap_file} not found.")
        return
    except Exception as e:
        print(f"[!] Error reading pcap: {e}")
        return

    hidden_data = []

    for pkt in packets:
        # Check for TCP layer and SYN flag (0x02)
        if pkt.haslayer(TCP) and pkt[TCP].flags == 0x02:
            seq_num = pkt[TCP].seq
            # Extract high byte: (Seq >> 24) & 0xFF
            char_code = (seq_num >> 24) & 0xFF
            
            if char_code != 0: # Avoid null bytes if they aren't part of the msg
                 hidden_data.append(chr(char_code))

    message = "".join(hidden_data)
    print(f"[*] Decoded Message:\n{message}")

if __name__ == "__main__":
    pcap_path = "Handout/exercises/Exercise4.pcap"
    if len(sys.argv) > 1:
        pcap_path = sys.argv[1]
    
    solve_exercise4(pcap_path)
