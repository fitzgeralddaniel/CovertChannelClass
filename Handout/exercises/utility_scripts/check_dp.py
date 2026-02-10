from scapy.all import *

def check_doublepulsar(pcap):
    pkts = rdpcap(pcap)
    for pkt in pkts:
        if pkt.haslayer(TCP) and (pkt[TCP].sport == 445 or pkt[TCP].dport == 445):
            # SMB header is usually after NetBIOS Session Service (4 bytes)
            # if payload exists
            if pkt.haslayer(Raw):
                payload = pkt[Raw].load
                # SMB 1.0 specific check
                # \xffSMB is the start of SMB header (0xff, 'S', 'M', 'B')
                if b'\xffSMB' in payload:
                    smb_offset = payload.find(b'\xffSMB')
                    # Mid is at offset 32 from start of SMB header (header is 32 bytes: 4 flag + 4 status + ... Mid is 2 bytes at offset 30?)
                    # Let's double check SMB header structure:
                    # 4 bytes: Protocol (\xffSMB)
                    # 1 byte: Command
                    # 4 bytes: Status
                    # 1 byte: Flags
                    # 2 bytes: Flags2
                    # 2 bytes: PID High
                    # 8 bytes: Signature
                    # 2 bytes: Reserved
                    # 2 bytes: TID
                    # 2 bytes: PID Low
                    # 2 bytes: UID
                    # 2 bytes: MID
                    
                    # Offset calc:
                    # 0: \xffSMB
                    # 4: Command
                    # 5: Status
                    # 9: Flags
                    # 10: Flags2
                    # 12: PID High
                    # 14: Signature
                    # 22: Reserved
                    # 24: TID
                    # 26: PID Low
                    # 28: UID
                    # 30: MID
                    
                    mid_bytes = payload[smb_offset+30:smb_offset+32]
                    mid = int.from_bytes(mid_bytes, byteorder='little')
                    
                    if mid == 81: # 0x51
                        print(f"FOUND DoublePulsar Response! Packet Mid={mid}")
                        return True
    print("DoublePulsar signature not found.")
    return False

check_doublepulsar('Handout/exercises/Exercise0.pcap')
