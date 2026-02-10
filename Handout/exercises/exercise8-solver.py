from scapy.all import *
import sys

def solve():
    # Read the pcap file
    packets = rdpcap('Handout/exercises/Exercise8.pcap')
    
    covert_message = ""
    
    for packet in packets:
        # Check if the packet is ICMP
        if ICMP in packet:
            # We are interested in Echo Requests (type 8)
            if packet[ICMP].type == 8:
                # Check for Raw layer (payload)
                if Raw in packet:
                    load = packet[Raw].load
                    # The load seems to be the character itself
                    try:
                        covert_message += load.decode('utf-8')
                    except:
                        pass
                        
    print(f"Recovered Message: {covert_message}")

if __name__ == "__main__":
    solve()
