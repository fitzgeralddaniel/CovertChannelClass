
import scapy.all as scapy
import base64
import sys
import collections
import urllib.parse
import os

def analyze_pcap(pcap_file):
    packets = scapy.rdpcap(pcap_file)
    messages = []
    
    print(f"Analyzing {pcap_file}...")
    
    binary_payloads = []

    for pkt in packets:
        if pkt.haslayer(scapy.TCP) and pkt.haslayer(scapy.Raw):
            load = pkt[scapy.Raw].load.decode('utf-8', errors='ignore')
            if "POST /gate.php" in load:
                # Extract body
                try:
                    headers, body = load.split('\r\n\r\n', 1)
                    decoded_body = urllib.parse.unquote(body)
                    parts = decoded_body.split('&')
                    
                    for part in parts:
                        if '=' in part:
                            key_b64, val_b64 = part.split('=', 1)
                            
                            try:
                                key = base64.b64decode(key_b64).decode('utf-8', errors='ignore')
                            except:
                                key = repr(key_b64)
                                
                            try:
                                val_bytes = base64.b64decode(val_b64)
                            except:
                                print(f"Key: {key} (Invalid Base64)")
                                continue

                            is_text = False
                            try:
                                val_str = val_bytes.decode('utf-8')
                                if val_str.isprintable():
                                    print(f"Key: {key} (Text - Likely Encrypted)")
                                    print(f"Value: {val_str}")
                                    is_text = True
                                else:
                                    print(f"Key: {key} (Binary, len={len(val_bytes)})")
                            except UnicodeDecodeError:
                                print(f"Key: {key} (Binary, len={len(val_bytes)})")
                            
                            if not is_text:
                                binary_payloads.append(val_bytes)

                            messages.append((key, val_bytes))
                            
                except Exception as e:
                    print(f"Error parsing packet: {e}")

    # Reconstruct binary
    if binary_payloads:
        filename = "extracted_secret.gpg"
        with open(filename, "wb") as f:
            for payload in binary_payloads:
                f.write(payload)
        print(f"\n[+] Extracted binary data to '{filename}' -> Identified as OpenPGP Secret Key")

    return messages

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 exercise6-solver.py <pcap_file>")
        sys.exit(1)
        
    pcap_file = sys.argv[1]
    analyze_pcap(pcap_file)
