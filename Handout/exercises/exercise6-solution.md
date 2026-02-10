# Exercise 6 Solution

## Analysis
The traffic consists of HTTP POST requests to `http://192.168.0.50:8080/gate.php`.
A quick scan reveals two key anomalies:
1.  **IP Identification Field**: The IP ID increments by a constant value of 7 between packets from the source `192.168.0.114`. Normal traffic usually increments by 1 or varies randomly. This suggests a pattern or signal, though the primary channel seems to be the payload.
2.  **HTTP POST Payloads**: The POST body contains `key=value` pairs with base64-encoded strings. The keys themselves are short strings (e.g., `S0ZPSVE=`, `VkFU`), while the values are long base64 strings involving high entropy.

Using a solver, we extract and decode these payloads. The content splits into two types:
- **Text**: Potentially Vigenere encrypted strings (keys suggest `ZOIE`, `VAT`, etc.).
- **Binary**: Data chunks that, when inspected, contain OpenPGP headers (specifically an OpenPGP Secret Key).

## Covert Channel
- **Mechanism**: **Storage Channel in HTTP POST Body**. The data is hidden within the parameters of HTTP POST requests.
- **Secondary Indicator**: **Timing/Sequence Channel** via IP ID increment (7), which might serve as a sequence number or a signal of covert traffic.

## Extracted Data
The channel is used to exfiltrate data, including:
1.  **Encrypted Text Messages**: Several strings that appear to be encrypted (likely Vigenere).
2.  **OpenPGP Secret Key**: A binary file was reconstructed from the payloads, identified by `file` as an OpenPGP Secret Key.

## Wetzel Pattern
- **Storage Channel**: The data is explicitly stored in the protocol fields (HTTP Body).

## Metrics
- **Bandwidth**: **High**. The channel transmits large blobs of data (hundreds of bytes per packet).
- **Stealth**: **Medium**. While HTTP traffic is common, the high entropy of the POST parameters and the constant IP ID increment are detectable by anomaly detection systems.

## Solution Script
A Python script `exercise6-solver.py` was created to specificially parse these packets, decode the base64 layers, and extract the binary artifacts.

## Post Analysis (Hint Based)
Further analysis (and hints) suggest the communication likely uses **ECDH (Elliptic Curve Diffie-Hellman)** for key exchange and **RC4** for stream encryption, wrapped in **Base64**.

### Impact on Analysis
1.  **Key Pair Exchange**: The two distinct POST parameter keys observed (`S0ZPSVE=` which decodes to `KFOIQ`/? and `198...`) likely represent ephemeral public keys or key identifiers used to derive a shared secret.
2.  **Encryption**: The "text" payloads that appeared to be Vigenere encrypted are more likely **RC4 encrypted streams**. RC4 is a stream cipher that XORs the plaintext with a keystream. The "Vigenere-like" appearance (high entropy but character-based if base64 decoded) fits this.
3.  **Binary Artifacts**: The OpenPGP Secret Key we extracted might have been transmitted in a "clear" binary block (after B64 decoding) or the RC4 keystream happened to align/reset, or perhaps that specific part of the communication was not RC4 encrypted (e.g., a "file transfer" mode vs "command and control" mode).

This explains why simple substitution ciphers failed on the text data. A full decryptor would require identifying the elliptic curve parameters, extracting the public keys, and deriving the RC4 key.
