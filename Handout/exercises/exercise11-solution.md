# Exercise 11 — Morse Code via UDP Burst Sizes

## Analysis

1. **Protocol overview** – The capture contains 658 UDP packets between `192.168.2.1:62056` and `192.168.2.4:23284` over ~63 seconds. Client→server packets carry a 16-byte payload that decodes (hex → ASCII → base64) to the string `nottheflag`. Server replies are a 4-byte `ACK`. The payload content is a **decoy**.

2. **Spotting the channel** – Although every packet carries the same payload, the packets arrive in distinct **bursts** separated by ~0.5 s gaps. The number of packets per burst alternates between exactly **3** and **6**, an unusual pattern that suggests binary encoding.

3. **Identifying Morse code** – Mapping 3 → dot (`.`) and 6 → dash (`-`) reveals valid Morse characters. Three levels of inter-burst timing distinguish:
   | Gap duration | Meaning |
   |---|---|
   | ~0.5 s | symbol separator (dot/dash within a letter) |
   | ~1.5 s | letter separator |
   | ~4.0 s | word separator |

## Covert Channel

**Mechanism**: Storage channel encoded in the **number of UDP packets per burst** (3 = dot, 6 = dash) combined with a **timing channel** (inter-burst gaps) for letter/word boundaries. The payload is fixed cover traffic; all information is carried structurally.

## Decoded Message

```
FLAG(H4CK7H3PL4N37)
```

## Wetzel Pattern

**Hybrid — Size/Count Manipulation + Timing Channel**

- The burst *size* (count of packets) encodes the Morse symbol (storage component).
- The inter-burst *timing gap* encodes symbol, letter, and word boundaries (timing component).

## Metrics

| Metric | Value |
|---|---|
| **Bandwidth** | ~1 Morse symbol per burst (~2 s per letter including gaps); very low data rate |
| **Stealth** | **Medium** — individual packets look normal; statistical analysis of arrival timing or burst sizes quickly reveals the pattern |
