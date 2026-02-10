from scapy.all import *
import sys

# HID Usage Tables for Keyboard/Keypad
# (Standard Set)
hid_map = {
    0x04: 'a', 0x05: 'b', 0x06: 'c', 0x07: 'd', 0x08: 'e', 0x09: 'f', 0x0A: 'g', 0x0B: 'h', 0x0C: 'i', 0x0D: 'j',
    0x0E: 'k', 0x0F: 'l', 0x10: 'm', 0x11: 'n', 0x12: 'o', 0x13: 'p', 0x14: 'q', 0x15: 'r', 0x16: 's', 0x17: 't',
    0x18: 'u', 0x19: 'v', 0x1A: 'w', 0x1B: 'x', 0x1C: 'y', 0x1D: 'z',
    0x1E: '1', 0x1F: '2', 0x20: '3', 0x21: '4', 0x22: '5', 0x23: '6', 0x24: '7', 0x25: '8', 0x26: '9', 0x27: '0',
    0x28: '\n', 0x29: 'ESCAPE', 0x2A: 'DELETE', 0x2B: 'TAB', 0x2C: ' ', 0x2D: '-', 0x2E: '=', 0x2F: '[',
    0x30: ']', 0x31: '\\', 0x32: '#', 0x33: ';', 0x34: '\'', 0x35: '`', 0x36: ',', 0x37: '.', 0x38: '/',
    0x39: 'CAPSLOCK', 0x3A: 'F1', 0x3B: 'F2', 0x3C: 'F3', 0x3D: 'F4', 0x3E: 'F5', 0x3F: 'F6', 0x40: 'F7',
    0x41: 'F8', 0x42: 'F9', 0x43: 'F10', 0x44: 'F11', 0x45: 'F12'
}

# Shifted map (UpperCase) - simplified for common chars
hid_map_shift = {
    0x04: 'A', 0x05: 'B', 0x06: 'C', 0x07: 'D', 0x08: 'E', 0x09: 'F', 0x0A: 'G', 0x0B: 'H', 0x0C: 'I', 0x0D: 'J',
    0x0E: 'K', 0x0F: 'L', 0x10: 'M', 0x11: 'N', 0x12: 'O', 0x13: 'P', 0x14: 'Q', 0x15: 'R', 0x16: 'S', 0x17: 'T',
    0x18: 'U', 0x19: 'V', 0x1A: 'W', 0x1B: 'X', 0x1C: 'Y', 0x1D: 'Z',
    0x1E: '!', 0x1F: '@', 0x20: '#', 0x21: '$', 0x22: '%', 0x23: '^', 0x24: '&', 0x25: '*', 0x26: '(', 0x27: ')',
    0x2D: '_', 0x2E: '+', 0x2F: '{', 0x30: '}', 0x31: '|', 0x33: ':', 0x34: '"', 0x35: '~', 0x36: '<', 0x37: '>', 0x38: '?'
}

def solve_exercise9():
    packets = rdpcap("Handout/exercises/Exercise9.pcap")
    message = ""
    
    # We are looking for ICMP Echo Requests (Type 8)
    # The payload (load) seems to be a single byte corresponding to a HID code.
    # Note: Real HID reports are 8 bytes, but this exercise simplifies it to just the keycode byte in the payload.
    # We might need to handle modifiers (Shift) if they were encoded, but let's start simple.
    # Based on tcpdump, we saw payloads like '07', '05', '00', '06', etc.
    
    message_bytes = []
    
    for pkt in packets:
        if IP in pkt and ICMP in pkt:
            if pkt[ICMP].type == 8: # Echo Request
                if hasattr(pkt[ICMP], 'load') and len(pkt[ICMP].load) > 0:
                    code = pkt[ICMP].load[0]
                    message_bytes.append(code)

    print(f"Found {len(message_bytes)} bytes.")
    
    # Decoding Logic:
    # Analysis suggests that bytes are sent as nibbles.
    # Ex: 0x05, 0x03 -> 0x53 ('S')
    # The last byte 0x0a looks like a newline.
    
    decoded_msg = ""
    i = 0
    while i < len(message_bytes):
        # Check if we have a pair
        if i + 1 < len(message_bytes):
            high = message_bytes[i]
            low = message_bytes[i+1]
            
            # If the byte is 0x0a (newline), it might be a single byte or end of stream
            if high == 0x0a:
                decoded_msg += "\n"
                i += 1
                continue
                
            # Combine nibbles
            # Note: The payloads are like 0x05, 0x03. So we take the integer value.
            char_code = (high << 4) | low
            decoded_msg += chr(char_code)
            i += 2
        else:
            # Last byte
            if message_bytes[i] == 0x0a:
                decoded_msg += "\n"
            else:
                decoded_msg += f"[{message_bytes[i]:02x}]"
            i += 1
            
    print("Decoded Message:")
    print(decoded_msg)

if __name__ == "__main__":
    solve_exercise9()
