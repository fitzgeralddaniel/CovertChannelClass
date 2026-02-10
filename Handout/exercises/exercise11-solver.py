#!/usr/bin/env python3
"""
Exercise 11 Solver — Morse Code via UDP Burst Sizes

Covert Channel: The number of UDP packets sent per burst encodes Morse code.
  - 3 packets in a burst = dot (.)
  - 6 packets in a burst = dash (-)
  - ~0.5s gap between bursts = symbol separator (within a letter)
  - ~1.5s gap between bursts = letter separator
  - ~4.0s gap between bursts = word separator

The UDP payload ("nottheflag" base64-encoded) is a decoy; the real message
is carried entirely in the burst-size / timing pattern.

Usage: python3 exercise11-solver.py [pcap_file]
"""

import subprocess
import sys

# ── Morse code lookup ────────────────────────────────────────────────────────
MORSE_CODE = {
    ".-": "A",   "-...": "B",  "-.-.": "C",  "-..": "D",   ".": "E",
    "..-.": "F",  "--.": "G",  "....": "H",  "..": "I",    ".---": "J",
    "-.-": "K",   ".-..": "L", "--": "M",    "-.": "N",    "---": "O",
    ".--.": "P",  "--.-": "Q", ".-.": "R",   "...": "S",   "-": "T",
    "..-": "U",   "...-": "V", ".--": "W",   "-..-": "X",  "-.--": "Y",
    "--..": "Z",
    ".----": "1", "..---": "2","...--": "3", "....-": "4", ".....": "5",
    "-....": "6", "--...": "7","---..": "8", "----.": "9", "-----": "0",
    "-.--.": "(",  "-.--.-": ")", ".-.-.-": ".", "--..--": ",",
    "..--..": "?", ".----.": "'", "-.-.--": "!", "-..-.": "/",
}

# ── Thresholds (seconds) ────────────────────────────────────────────────────
BURST_GAP   = 0.1   # gap > this → new burst
LETTER_GAP  = 0.8   # gap > this → new Morse letter
WORD_GAP    = 2.0   # gap > this → new word (space)
DOT_SIZE    = 3     # packets-per-burst for a dot
DASH_SIZE   = 6     # packets-per-burst for a dash
MIN_BURST   = 2     # ignore bursts smaller than this (end-of-stream markers)


def extract_timestamps(pcap_path: str) -> list[float]:
    """Return epoch timestamps of client→server (192.168.2.1) UDP packets."""
    result = subprocess.run(
        ["tshark", "-r", pcap_path,
         "-Y", "udp && ip.src==192.168.2.1",
         "-T", "fields", "-e", "frame.time_epoch"],
        capture_output=True, text=True, check=True,
    )
    return [float(t) for t in result.stdout.strip().split("\n") if t.strip()]


def timestamps_to_bursts(times: list[float]) -> list[tuple[int, float]]:
    """Group timestamps into bursts; return [(count, gap_after), …]."""
    bursts: list[tuple[int, float]] = []
    count = 1
    for i in range(1, len(times)):
        gap = times[i] - times[i - 1]
        if gap > BURST_GAP:
            bursts.append((count, gap))
            count = 1
        else:
            count += 1
    bursts.append((count, 0.0))
    return bursts


def decode_morse(bursts: list[tuple[int, float]]) -> str:
    """Convert burst sizes + gaps into a decoded Morse string."""
    morse_letters: list[str] = []
    current = ""

    for count, gap_after in bursts:
        if count < MIN_BURST:
            continue  # skip end-of-message markers

        current += "." if count == DOT_SIZE else "-"

        if gap_after > WORD_GAP:
            morse_letters.append(current)
            morse_letters.append(" ")
            current = ""
        elif gap_after > LETTER_GAP:
            morse_letters.append(current)
            current = ""

    if current:
        morse_letters.append(current)

    decoded = ""
    for ml in morse_letters:
        if ml == " ":
            decoded += " "
        else:
            decoded += MORSE_CODE.get(ml, f"[{ml}?]")
    return decoded


def main() -> None:
    pcap = sys.argv[1] if len(sys.argv) > 1 else "Handout/exercises/Exercise11.pcapng"

    times = extract_timestamps(pcap)
    bursts = timestamps_to_bursts(times)
    sizes = [b[0] for b in bursts]

    print(f"Client packets : {len(times)}")
    print(f"Bursts         : {len(bursts)}")
    print(f"Burst sizes    : {sizes}\n")

    message = decode_morse(bursts)
    print(f"Decoded message: {message}")


if __name__ == "__main__":
    main()
