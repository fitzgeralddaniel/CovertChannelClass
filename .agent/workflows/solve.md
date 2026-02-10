---
description: Analyze a pcap file to find a covert channel, create a solver script, and document the solution.
---

# Solve Covert Channel Exercise

This workflow guides you through analyzing a pcap file, identifying the covert channel, creating a python solver, and documenting the solution.

## 1. Context and Setup
- **Input**: The user will provide a pcap file path (e.g., `@{Handout}/exercises/Exercise4.pcap`).
- **Goal**: Identify the hidden data (covert channel), extract the message, and document it.
- **Naming Convention**:
    - Solver Script: `Handout/exercises/exercise[N]-solver.py`
    - Solution Doc: `Handout/exercises/exercise[N]-solution.md`
    - Determine `[N]` from the pcap filename.

## 2. Reconnaissance (Analysis)
Start by exploring the pcap file.
1.  **List the file**: 
    // turbo
    `ls -lh <pcap_file>`
2.  **Initial Scan**: 
    // turbo
    `tcpdump -r <pcap_file> -n -c 20`
3.  **Identify Anomalies**: Look for **ANY** deviation from standard protocol behavior. Examples include (but are NOT limited to):
    - **ICMP**: Check payloads (are they empty? do they contain data?) and IP IDs.
    - **TCP/UDP**: Check for unusual ports, flag combinations (e.g., SYN with data), or sequence number irregularities.
    - **IP Headers**: Check Identification (ID), Type of Service (TOS), and Time to Live (TTL) fields for variations.
    - **Timing**: Check for inter-arrival time patterns.
    - **Protocol Misuse**: Using fields for purposes other than intended (e.g., wrong error codes, reserved fields).
    - **CRITICAL**: Do not stop at these examples. ANY field or timing behavior could be the channel.

4.  **Deep Dive**:
    - Use `tshark` or small Python scripts (using `scapy`) to inspect specific fields if suspicious.
    - **Goal**: Form a hypothesis about where the data is hidden.

## 3. Develop Solver
Create a Python script to extract the message.
1.  **Create Script**: `Handout/exercises/exercise[N]-solver.py`
2.  **Implementation**:
    - Use `scapy` (`from scapy.all import *`) or `subprocess` calls to `tshark`.
    - logic to iterate through packets, extract the target field/payload, and decode it (usually ASCII).
    - Print the extracted message clearly.
    - **Contingency**: If the channel does not transmit a clear text message (e.g., it's binary data, a timing signal, or just the presence of a backdoor), instead print a "Proof of Concept" (e.g., "Found 50 packets with hidden data: [sample]") and explain the mechanism.

3.  **Verify**: Run the script: `python3 Handout/exercises/exercise[N]-solver.py <pcap_file>`
    - Ensure the output is a readable string or flag.
    - If it fails, debug and iterate.

## 4. Documentation
Create a solution write-up.
1.  **Create File**: `Handout/exercises/exercise[N]-solution.md`
2.  **Content Requirements**:
    - **Analysis**: Explain *how* a student would find this. (e.g., "Filter for ICMP and look at the payload").
    - **Covert Channel**: Define the mechanism (e.g., "Storage Channel in IP ID field").
    - **Message/Data**: The decoded string OR a description/sample of the data found if not a clear message.

    - **Wetzel Pattern**: Which pattern does this fit? (e.g., Header Manipulation, Protocol Manipulation, Timing Channel).
    - **Metrics**: Estimate Bandwidth (bits/packet) and Stealth (Low/Med/High).

## 5. Finalize
- Mark the task as complete.
- Ask the user if they want to proceed to the next exercise.
