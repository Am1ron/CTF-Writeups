# Sequence of Events — Network Forensics Writeup

**File:** `Sequence_of_Events.pcap`  
**Packets:** 641  
**Flag:** `CYCNET{b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7}`

---

## Overview

A 641-packet capture hides a covert message using the **TCP Initial Sequence Number (ISN)** field of unsolicited SYN packets. No payload. No completed handshakes. The message lives entirely in the handshake metadata.

---

## Reconnaissance

First pass: count the packet types and identify anomalies.

```
Total packets:        641
SYN (no ACK) packets:  70
Single source IP:   10.0.0.42
Primary target IP:  10.20.30.40  ← receives 45 SYNs, never responds
```

All 70 SYN packets originate from `10.0.0.42`. The bulk go to `10.20.30.40` — a host that returns nothing. No SYN-ACK, no RST. It just absorbs them.

---

## Traffic Structure

The SYNs split into two distinct phases:

### Phase 1 — Port 80 (5 packets, decoy/preamble)

| Time offset | Src port | Seq number (hex) |
|-------------|----------|------------------|
| +0s  | 44022 | `0x1a2b3c00` |
| +3s  | 44023 | `0x1b2b3c37` |
| +6s  | 44024 | `0x1c2b3c6e` |
| +9s  | 44025 | `0x1d2b3ca5` |
| +12s | 44026 | `0x1e2b3cdc` |

Large, incrementing values — plausible as noise or a scanner. These are camouflage.

### Phase 2 — Port 443 (40 packets, the message)

Sequence numbers drop to ASCII range (48–125). One character per SYN, sent every 7 seconds:

| Seq | ASCII |   | Seq | ASCII |
|-----|-------|---|-----|-------|
| 67  | `C`   |   | 54  | `6`   |
| 89  | `Y`   |   | 97  | `a`   |
| 67  | `C`   |   | 55  | `7`   |
| 78  | `N`   |   | 98  | `b`   |
| 69  | `E`   |   | 56  | `8`   |
| 84  | `T`   |   | 99  | `c`   |
| 123 | `{`   |   | 57  | `9`   |
| 98  | `b`   |   | 100 | `d`   |
| 50  | `2`   |   | 48  | `0`   |
| 99  | `c`   |   | 101 | `e`   |
| 51  | `3`   |   | 49  | `1`   |
| 100 | `d`   |   | 102 | `f`   |
| 52  | `4`   |   | 50  | `2`   |
| 101 | `e`   |   | 97  | `a`   |
| 53  | `5`   |   | 51  | `3`   |
| 102 | `f`   |   | 98  | `b`   |
| 54  | `6`   |   | 52  | `4`   |
| 97  | `a`   |   | 99  | `c`   |
| 55  | `7`   |   | 53  | `5`   |
| 98  | `b`   |   | 100 | `d`   |
| 56  | `8`   |   | 54  | `6`   |
| 99  | `c`   |   | 101 | `e`   |
| 57  | `9`   |   | 55  | `7`   |
| 100 | `d`   |   | 125 | `}`   |

---

## Decoding

```python
seqs = [
    67,89,67,78,69,84,123,
    98,50,99,51,100,52,101,53,102,54,97,55,98,56,99,57,100,48,
    101,49,102,50,97,51,98,52,99,53,100,54,101,55,
    125
]

flag = ''.join(chr(s) for s in seqs)
print(flag)
# CYCNET{b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7}
```

---

## Flag

```
CYCNET{b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7}
```

---

## The Technique: TCP ISN Covert Channel

The **Initial Sequence Number** is a 32-bit field in the TCP SYN packet. Per RFC 793, it should be randomized to prevent hijacking. It serves no functional purpose during a half-open (never-completed) connection — making it ideal dead space for encoding data.

**Why this works as a covert channel:**

- **No payload inspection catches it.** The message never appears in the data portion of any packet. DPI, SSL inspection, and content filters are all blind to it.
- **No connection is ever completed.** There's no session to reconstruct, no stream to follow. Standard "follow TCP stream" analysis returns nothing.
- **One-way transmission.** The receiver doesn't need to respond or even be alive. Any host passively observing the wire (or a compromised router, mirror port, or ISP tap) can read the message.
- **Timing is regular but unremarkable.** 7-second intervals between SYNs to the same dead IP could pass as a misconfigured keepalive or a background scanner.
- **Port 443 destination.** SYN packets to port 443 that never complete a TLS handshake are extremely common in real network traffic.

**Detection signals** (after the fact):
- Sequential port numbers on the source (`44027` → `44066`), never reused
- Sequence numbers all fall within printable ASCII range (32–126)
- Regular 7-second inter-packet timing with zero jitter
- Destination host produces zero response traffic

---

## Timeline

```
T+0s   Phase 1 begins — 5 SYNs to port 80, large seq numbers (cover traffic)
T+18s  Phase 2 begins — SYNs shift to port 443, seq numbers enter ASCII range
T+18s  'C' (67)
T+25s  'Y' (89)
T+32s  'C' (67)
...
T+291s '}' (125)  ← message complete
```

Total transmission time: ~4m 51s for 40 characters.

---

## References

- Rowland, C. (1997). *Covert Channels in the TCP/IP Protocol Suite.* First Monday.
- RFC 793 — Transmission Control Protocol (Initial Sequence Number specification)
- Murdoch & Lewis (2005). *Embedding Covert Channels into TCP/IP.* Information Hiding Workshop.
