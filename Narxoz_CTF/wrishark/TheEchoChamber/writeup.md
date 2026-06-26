# CTF Writeup — ch2.pcapng
**Category:** Network Forensics  
**Flag:** `cycnet{b53227da4280f0e18270f21dd77c9100}`

---

## Challenge Description

> Routine diagnostics. Nodes pinging nodes. Nothing unusual — or so they want you to think. The multi-agent system has been communicating in plain sight the entire time. Your job is to figure out how.

---

## Overview

A 1.2 MB packet capture containing 1,303 packets. The flavour text hints at covert communication hiding in plain sight — a classic signal for **protocol steganography** or **covert channel** techniques.

---

## Analysis

### Step 1 — Protocol Survey

Loading the capture and tallying IP protocols reveals a heavily skewed traffic distribution:

| Protocol | Count |
|----------|-------|
| UDP (17) | 1,211 |
| TCP (6)  | 88    |
| ICMP (1) | **2** |
| ARP      | 2     |

Over 98% of traffic is UDP/TCP — noise. But the **2 ICMP packets** are anomalous. Normal operational environments don't generate lone ping pairs to external resolvers mid-session.

### Step 2 — Inspecting the ICMP Packets

The two ICMP packets form a matching Echo Request / Echo Reply pair:

| Direction | Type | Source | Destination |
|-----------|------|--------|-------------|
| Request   | 8    | `10.23.23.135` | `8.8.8.8` |
| Reply     | 0    | `8.8.8.8` | `10.23.23.135` |

Pinging `8.8.8.8` (Google Public DNS) is textbook cover — it's the single most "normal-looking" ICMP target imaginable.

### Step 3 — Extracting the Payload

ICMP Echo packets consist of an 8-byte header (type, code, checksum, identifier, sequence), followed by an arbitrary data payload. Inspecting the raw bytes:

```
Full ICMP hex:
08 00 96 b6 00 00 00 00   ← 8-byte header (type=8, checksum, id, seq)
63 79 63 6e 65 74 7b 62   ← c y c n e t { b
35 33 32 32 37 64 61 34   ← 5 3 2 2 7 d a 4
32 38 30 66 30 65 31 38   ← 2 8 0 f 0 e 1 8
32 37 30 66 32 31 64 64   ← 2 7 0 f 2 1 d d
37 37 63 39 31 30 30 7d   ← 7 7 c 9 1 0 0 }
```

The 40-byte payload decodes directly to ASCII:

```
cycnet{b53227da4280f0e18270f21dd77c9100}
```

---

## The Technique: ICMP Covert Channel

ICMP covert channels exploit the **data payload field** of Echo Request/Reply packets to carry arbitrary information. This is a well-documented exfiltration technique because:

1. **ICMP has no port numbers** — port-based firewall rules don't apply
2. **Ping is universally whitelisted** — few environments block outbound ICMP echo
3. **No session state** — single packet, no handshake, leaves minimal log trail
4. **Payload is unvalidated** — the protocol spec places no restrictions on echo data content

The attacker (or agent) simply stuffs the flag into the ICMP payload field and fires it at an external address. The reply mirrors it back — confirming receipt.

Real-world tools that weaponise this technique include `ptunnel`, `icmptunnel`, and `icmp-exfil`.

---

## Detection Notes

This specific instance is detectable by:
- Filtering for ICMP traffic and inspecting payload bytes for non-standard content (normal `ping` utilities use repeating ASCII sequences like `abcdefgh...`)
- Alerting on ICMP payloads containing printable ASCII strings matching flag/secret patterns
- Baselining ICMP volume — two packets in a 1,303-packet capture is an outlier

---

## Flag

```
cycnet{b53227da4280f0e18270f21dd77c9100}
```
