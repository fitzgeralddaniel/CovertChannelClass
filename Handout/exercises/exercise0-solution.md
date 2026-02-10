# Exercise 0 Solution: DoublePulsar Backdoor

## Analysis
To find the covert channel in this pcap, a student should:
1.  Open `Exercise0.pcap` in Wireshark.
2.  Notice the heavy SMB traffic on port 445.
3.  Filter for `smb` or `smb2`.
4.  Observe many `Trans2 Response` packets with the error `STATUS_NOT_IMPLEMENTED` (0xC0000002).
5.  Inspect the `Multiplex ID` (MID) in these packets. Regular traffic increments this ID or uses it to match requests/responses. In DoublePulsar infections, this field (along with the payload of the "error" response) is used to pass data back from the implant.
6.  A student can filter specifically for `smb.mid == 81` (0x51) or `smb.mid == 82` (0x52) to see clear indicators, though the `STATUS_NOT_IMPLEMENTED` on `Trans2` is the primary anomaly.

## Covert Channel
**Mechanism**: Storage Covered Channel / Protocol Manipulation
**Location**: SMB (Server Message Block) Protocol, specifically the `Multiplex ID` (MID) field and the payload data within a `Trans2 Response` that claims to be an error (`STATUS_NOT_IMPLEMENTED`). The implant modifies the OS kernel to hijack this specific error path to communicate without creating new sockets or processes.

## Message
The "message" in this context is the **existence and status of the DoublePulsar backdoor**. The specific data in the payload generally contains XOR-encrypted status information (architecture, OS version, etc.) confirming the machine is infected and ready for commands (like `Exec`, `Burn`, `Kill`).

## Wetzel Pattern
This fits the **Protocol Manipulation** pattern, specifically embedding data in header fields (`MID`) and error response payloads that should typically be empty or standard error structures.

## Metrics
*   **Bandwidth**: Low. It relies on the request/response cycle of SMB.
*   **Stealth**: High. It piggybacks on existing port 445 traffic, does not open new ports, and masquerades as standard protocol error messages, which are often ignored by IDS.
