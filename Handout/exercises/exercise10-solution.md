# Exercise 10 – Multi-Port Backdoor Shell

## Analysis

Inspecting the pcap with `tcpdump` or Wireshark reveals **131 packets** containing a mix of:

- **802.11 Prism frames** (Ethertype `0x2452`) – wireless captures that duplicate the wired traffic
- **Standard Ethernet IP/TCP** – the actual network sessions

Filtering for TCP sessions on well-known ports reveals suspicious behavior:

| Port | Protocol | Expected Behavior | Actual Behavior |
|------|----------|-------------------|-----------------|
| 53   | DNS      | DNS queries/responses | Windows XP command shell |
| 21   | FTP      | FTP login banner | SYN → RST (port scan) |
| 23   | Telnet   | Telnet negotiation | Windows XP command shell |
| 80   | HTTP     | HTTP request/response | Windows XP command shell |

All three active sessions (53, 23, 80) respond with an identical banner:
```
Microsoft Windows XP [Version 5.1.2600]
(C) Copyright 1985-2001 Microsoft Corp.

C:\>
```

### Commands Executed

- **Port 53 (DNS):** `dir`, `exit`
- **Port 23 (Telnet):** `dir`, `ls -la` (fails — Windows host), `exit`
- **Port 80 (HTTP):** `dir`, `exit`

Port 21 (FTP) receives **6 SYN packets** across two source ports, all answered with RST — indicating either port scanning or a failed backdoor port.

## Covert Channel

**Mechanism:** A backdoor Trojan on the victim machine (192.168.1.2, Windows XP) listens on multiple well-known TCP ports (53, 23, 80), serving an interactive `cmd.exe` shell on each. By reusing ports that firewalls typically allow (DNS, HTTP), the backdoor evades simple port-based filtering. The attacker (192.168.1.3) connects to each port in sequence to confirm access and enumerate the filesystem.

**Cover Traffic:** Legitimate HTTP browsing to `goals365.com` (83.170.75.178) runs alongside the backdoor sessions, further masking the malicious activity.

## Wetzel Pattern

**Protocol Manipulation (Backdoor/Port Misuse)** — Well-known service ports are repurposed to carry unauthorized interactive shell traffic instead of their expected protocols.

## Metrics

| Metric | Value |
|--------|-------|
| **Bandwidth** | Unlimited (full interactive shell) |
| **Stealth** | Low–Medium |
| **Detection** | Deep Packet Inspection reveals non-protocol-conformant payloads (e.g., Windows shell banner on port 53). Simple port-based firewalls would miss this entirely. |
