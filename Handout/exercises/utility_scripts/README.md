# Utility Scripts

This directory contains helper scripts used during the analysis of the pcap files.

*   `scanner.py`: A generic script to extract and print ASCII strings from packet payloads. useful for finding cleartext flags or messages.
*   `check_dp.py`: A preliminary script to check for DoublePulsar signatures (SMB Mid=81).
*   `debug_smb.py`: A script to debug SMB traffic and print raw payloads, intended to help understand the SMB header structure.
*   `debug_smb_v2.py`: An enhanced version of the SMB debug script that includes support for SMBv2 headers and hex dumping.
*   `full_scan.py`: A script that attempts to scan the entire pcap for DoublePulsar signatures using Scapy.
