import subprocess
import sys

def analyze_exercise0(pcap_file):
    print(f"Analyzing {pcap_file} for DoublePulsar covert channel...")
    
    # We use tshark because it has robust SMB parsing
    # The DoublePulsar signature often involves:
    # 1. Trans2 Response with STATUS_NOT_IMPLEMENTED
    # 2. Multiplex ID (MID) values that are specific (often 81 or others depending on variant)
    # 3. Specific payload calculations
    
    # Based on manual analysis, we look for Trans2 Response + STATUS_NOT_IMPLEMENTED
    cmd = [
        'tshark', '-r', pcap_file,
        '-Y', 'smb.cmd == 0x32 && smb.nt_status == 0xc0000002',
        '-T', 'fields',
        '-e', 'frame.number',
        '-e', 'ip.src',
        '-e', 'ip.dst',
        '-e', 'smb.mid'
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        lines = result.stdout.strip().split('\n')
        
        found_count = 0
        for line in lines:
            if not line: continue
            parts = line.split('\t')
            if len(parts) >= 4:
                frame, src, dst, mid = parts
                print(f"[+] Found DoublePulsar Indicator in Frame {frame}")
                print(f"    Source: {src} -> Dest: {dst}")
                print(f"    Multiplex ID: {mid}")
                print(f"    Signature: Trans2 Response with STATUS_NOT_IMPLEMENTED")
                found_count += 1
                
        if found_count > 0:
            print(f"\nSUCCESS: Detected {found_count} potential DoublePulsar packets.")
            print("Covert Channel: SMB Trans2 Response (0x32) misuse with Error Code 0xC0000002.")
            print("Message: The presence of the DoublePulsar backdoor.")
            
    except subprocess.CalledProcessError as e:
        print(f"Error running tshark: {e}")
    except FileNotFoundError:
        print("Error: tshark not found. Please install wireshark/tshark.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 exercise0-solver.py <pcap_file>")
        sys.exit(1)
    analyze_exercise0(sys.argv[1])
