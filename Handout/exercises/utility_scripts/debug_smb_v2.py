from scapy.all import *
import sys
import binascii

def debug_print(pcap_file):
    pkts = rdpcap(pcap_file)
    for i, pkt in enumerate(pkts):
        if pkt.haslayer(TCP) and (pkt[TCP].sport == 445 or pkt[TCP].dport == 445):
            if pkt.haslayer(Raw):
                payload = pkt[Raw].load
                # Print first 16 bytes in hex
                print(f"Packet {i} Payload: {binascii.hexlify(payload[:16])}")
                
                if b'\xffSMB' in payload:
                    print(f"  [!] SMBv1 Header found")
                    offset = payload.find(b'\xffSMB')
                    if len(payload) >= offset + 32:
                         mid = int.from_bytes(payload[offset+30:offset+32], byteorder='little')
                         print(f"  Mid: {mid}")
                
                if b'\xfeSMB' in payload:
                    print(f"  [!] SMBv2/3 Header found")

if __name__ == "__main__":
    try:
        debug_print(sys.argv[1])
    except BrokenPipeError:
        pass
