#!/usr/bin/env python3
"""
Exercise 10 Solver – Multi-Port Backdoor Shell Detection

Covert Channel: TCP backdoor shells hidden behind well-known service ports
(DNS/53, Telnet/23, HTTP/80). All three ports serve identical Windows XP
command prompts instead of their expected protocols.

Usage:
    python3 exercise10-solver.py [pcap_file]
"""

import sys
from scapy.all import rdpcap, TCP, IP


def extract_sessions(packets):
    """Extract and reconstruct TCP sessions by well-known port."""
    # Ports of interest (well-known ports used as backdoors)
    target_ports = {53: "DNS", 21: "FTP", 23: "Telnet", 80: "HTTP"}

    sessions = {}
    for port in target_ports:
        sessions[port] = {
            "label": target_ports[port],
            "syn_count": 0,
            "rst_count": 0,
            "established": False,
            "commands": [],
            "responses": [],
            "payloads_client": [],
            "payloads_server": [],
        }

    for pkt in packets:
        # Skip non-standard Ethernet frames (0x2452 Prism/802.11 duplicates)
        if hasattr(pkt, "type") and pkt.type != 0x0800:
            continue

        if TCP not in pkt or IP not in pkt:
            continue

        tcp = pkt[TCP]
        ip = pkt[IP]
        flags = str(tcp.flags)
        payload = bytes(tcp.payload) if tcp.payload else b""

        # Determine which well-known port this belongs to
        port = None
        if tcp.dport in target_ports:
            port = tcp.dport
            direction = "client"
        elif tcp.sport in target_ports:
            port = tcp.sport
            direction = "server"
        else:
            continue

        sess = sessions[port]

        # Track SYN / RST
        if "S" in flags and "A" not in flags:
            sess["syn_count"] += 1
        if "R" in flags:
            sess["rst_count"] += 1
        if "S" in flags and "A" in flags:
            sess["established"] = True

        # Collect payloads
        if payload:
            text = payload.decode("ascii", errors="replace").rstrip("\x00")
            if direction == "client":
                sess["payloads_client"].append(text)
                # Commands are short client payloads
                clean = text.strip().strip("\x00")
                if clean and len(clean) < 50:
                    sess["commands"].append(clean)
            else:
                sess["payloads_server"].append(text)

    return sessions


def detect_backdoor(sessions):
    """Identify which ports are being used as covert backdoor shells."""
    backdoors = []
    scanned = []

    for port, sess in sorted(sessions.items()):
        if sess["established"] and sess["payloads_server"]:
            # Check if server responses contain shell indicators
            all_responses = " ".join(sess["payloads_server"])
            if "Windows" in all_responses or "C:\\" in all_responses or "$ " in all_responses:
                backdoors.append(port)
        elif sess["syn_count"] > 0 and not sess["established"]:
            scanned.append(port)

    return backdoors, scanned


def main():
    pcap_file = sys.argv[1] if len(sys.argv) > 1 else "Handout/exercises/Exercise10.pcap"

    print(f"[*] Reading {pcap_file}...")
    packets = rdpcap(pcap_file)
    print(f"[*] Loaded {len(packets)} packets\n")

    sessions = extract_sessions(packets)
    backdoors, scanned = detect_backdoor(sessions)

    # --- Report ---
    print("=" * 60)
    print("  COVERT CHANNEL ANALYSIS: Multi-Port Backdoor")
    print("=" * 60)

    bd_str = ', '.join(f"{p}/{sessions[p]['label']}" for p in backdoors)
    print(f"\n[!] Backdoor shells detected on {len(backdoors)} port(s): {bd_str}")
    if scanned:
        sc_str = ', '.join(f"{p}/{sessions[p]['label']}" for p in scanned)
        print(f"[!] Port scanning detected on {len(scanned)} port(s): {sc_str}")

    for port in sorted(sessions.keys()):
        sess = sessions[port]
        print(f"\n{'─' * 60}")
        print(f"  Port {port}/{sess['label']}")
        print(f"{'─' * 60}")
        print(f"  SYN packets:  {sess['syn_count']}")
        print(f"  RST packets:  {sess['rst_count']}")
        print(f"  Established:  {sess['established']}")

        if port in backdoors:
            print(f"  ⚠  STATUS: BACKDOOR SHELL")
            print(f"  Commands sent:")
            for cmd in sess["commands"]:
                print(f"    → {cmd}")
            print(f"  Server response (first 200 chars):")
            first_resp = sess["payloads_server"][0] if sess["payloads_server"] else "(none)"
            print(f"    {first_resp[:200]}")
        elif port in scanned:
            print(f"  ⚠  STATUS: PORT SCAN (SYN → RST)")
        else:
            print(f"  ✓  STATUS: Normal")

    # Summary
    print(f"\n{'=' * 60}")
    print("  FINDINGS SUMMARY")
    print(f"{'=' * 60}")
    print(f"""
  Mechanism: The attacker runs a backdoor that listens on multiple
  well-known TCP ports (53, 23, 80). Each port serves an identical
  Windows XP command shell, mimicking legitimate services to evade
  firewall rules and IDS detection.

  The attacker also performs SYN scans on port 21 (FTP), which
  responds with RST (service not running or blocked).

  All three active backdoor sessions execute the same commands:
    • 'dir'  — directory listing of C:\\
    • 'exit' — close session

  Additionally, the telnet session runs 'ls -la' (which fails on
  Windows, confirming the attacker expected a Linux target).

  Covert Channel Type: Protocol Manipulation / Port Misuse
  Wetzel Pattern:      Protocol Manipulation (Backdoor)
  Bandwidth:           Full interactive shell (unlimited)
  Stealth:             Low-Medium (shell banners on wrong ports
                       are detectable by deep packet inspection)
""")


if __name__ == "__main__":
    main()
