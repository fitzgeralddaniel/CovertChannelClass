# Exercise 12 Solution — Iodine DNS Tunnel

## Analysis

1. **Initial observation**: All 46,930 packets are DNS queries/responses to subdomains of `hillary.clinton.io`, using NULL record type (type 10).
2. **Handshake identification**: Early queries (`yrbqy*`, `zqy*` prefixes) match the **iodine** DNS tunneling tool's handshake — version check, codec negotiation (Base32/Base64/Base128/Raw), and IP configuration (`10.0.0.1-10.0.0.2`).
3. **Data extraction**: DNS NULL response `rdata` contains a 2-byte iodine frame header followed by **zlib-compressed** TUN/TAP frames wrapping IPv4 packets.
4. **Tunneled traffic**: TCP connections to `45.55.178.79:9999` — a custom login service with ASCII art American flags, followed by `login:`/`password:` prompts.

## Covert Channel

**Mechanism**: Full IP-over-DNS tunnel using [iodine](https://github.com/yarrick/iodine). Upstream data encoded in DNS query subdomain labels (Base128 encoding); downstream data carried in DNS NULL record responses. All traffic compressed with zlib.

**Domain**: `hillary.clinton.io`  
**Tunnel IPs**: `10.0.0.1` ↔ `10.0.0.2`

## Extracted Data

The tunnel carries a **brute-force password attack** against a custom service on port 9999:

| Metric | Value |
|---|---|
| Total login attempts | 1,091 |
| Failed (ACCESS DENIED) | 891 |
| Successful (Welcome) | 200 |

**Successful usernames**: trump (73), bernie (67), Jeb (59), clinton (1)

## Wetzel Pattern

**Type**: Protocol Manipulation / Tunneling Channel  
**Sub-type**: DNS tunneling (full IP encapsulation via iodine)

## Metrics

| Metric | Value |
|---|---|
| Bandwidth | High — up to ~1,100 bytes/response (zlib compressed) via NULL records |
| Stealth | Low — NULL record queries to a suspicious domain, high volume (46K packets), large subdomain labels with binary data |
