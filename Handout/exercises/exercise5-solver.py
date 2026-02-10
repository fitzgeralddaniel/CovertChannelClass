from scapy.all import *

def solve():
    pcap = "Handout/exercises/Exercise5.pcap"
    packets = rdpcap(pcap)
    
    hidden_data = ""
    
    for p in packets:
        if p.haslayer(TCP):
            tcp = p[TCP]
            # Check for flags: SYN (S), ECE (E), CWR (C)
            # Scapy flags are stored as a 'Flag' object, can be checked with string representation
            # or bitwise operations. 'S' = 0x02, 'E' = 0x40, 'C' = 0x80.
            # 0x02 | 0x40 | 0x80 = 0xC2 (194)
            
            # Scapy's Flags object handles string comparison well.
            # We look for EXACTLY SEC flags based on analysis.
            if tcp.flags == "SEC":
                ip_id = p[IP].id
                # The high byte of the IP ID is the hidden character
                # IP ID is 16 bits. High byte is (id >> 8) & 0xFF.
                char_code = (ip_id >> 8) & 0xFF
                hidden_data += chr(char_code)
                
    print(f"Recovered Message: {hidden_data}")

if __name__ == "__main__":
    solve()
