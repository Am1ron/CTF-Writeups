# CTF Writeup — ch3.pcapng
**Category:** Network Forensics  
**Flag:** `cycnet{9e3669d19b675d25050859043258f3c4}`

---

## Challenge Description

> Every machine asks questions. That's normal. That's expected. But this agent asked too many — and the answers didn't matter. Something was moving outbound, dressed up as curiosity. Fragmented, scattered, hiding in the one traffic type that almost never raises an alarm. Piece it back together.

---

## Overview

A 2,056-packet capture. The flavour text is specific: *questions* (DNS queries), *fragmented*, *almost never raises an alarm* (DNS is near-universally trusted). This points directly to **DNS exfiltration** — encoding data into outgoing query hostnames.

---

## Analysis

### Step 1 — Protocol Survey

| Protocol | Count |
|----------|-------|
| UDP (17) | 1,651 |
| TCP (6)  | 405   |

All UDP. No ICMP this time. The internal resolver is `10.23.23.2` — a likely target for covert DNS queries that never need to reach the public internet.

### Step 2 — Isolating DNS Traffic

Filtering for UDP port 53 yields **78 DNS packets** (39 query/response pairs). Most are legitimate — `fonts.gstatic.com`, `play.google.com`, `safebrowsing.googleapis.com` — background noise from a browser session. But eight queries stand out immediately:

```
6379636e65.cycnet.local
747b396533.cycnet.local
3636396431.cycnet.local
3962363735.cycnet.local
6432353035.cycnet.local
3038353930.cycnet.local
3433323538.cycnet.local
663363347d.cycnet.local
```

The subdomains are 10-character hex strings under the internal domain `cycnet.local`. These are not real hostname lookups — they're data.

### Step 3 — Decoding the Subdomains

Each hex subdomain decodes to a 5-character ASCII chunk:

| Hex subdomain  | Decoded |
|----------------|---------|
| `6379636e65`   | `cycne`  |
| `747b396533`   | `t{9e3`  |
| `3636396431`   | `669d1`  |
| `3962363735`   | `9b675`  |
| `6432353035`   | `d2505`  |
| `3038353930`   | `08590`  |
| `3433323538`   | `43258`  |
| `663363347d`   | `f3c4}`  |

### Step 4 — Reassembling in Order

The chunks must be reassembled in **packet timestamp order** to recover the original sequence. Sorting the eight `cycnet.local` queries by their capture timestamp:

```
ts=...317  →  cycne
ts=...116  →  t{9e3
ts=...908  →  669d1
ts=...347  →  9b675
ts=...722  →  d2505
ts=...580  →  08590
ts=...770  →  43258
ts=...380  →  f3c4}
```

Concatenated in order:

```
cycnet{9e3669d19b675d25050859043258f3c4}
```

---

## The Technique: DNS Exfiltration

DNS exfiltration encodes data into query **subdomains** and fires them at a controlled (or intercepted) nameserver. It works because:

1. **DNS is rarely inspected** — most firewalls pass port 53 queries without deep inspection
2. **Queries look routine** — a hostname lookup is the most common network operation there is
3. **No response needed** — the exfiltrating host doesn't need a real answer; the data is in the *question*
4. **Fragmentation is built-in** — large payloads split naturally across multiple queries, each carrying a chunk

Here the agent hex-encoded the flag, split it into 5-byte (10 hex char) chunks, and issued one DNS query per chunk to `cycnet.local` via the local resolver. The queries were spaced ~30–100ms apart — slow enough to avoid rate-limit triggers, fast enough to complete in under a second total.

Real-world tooling that uses this pattern includes `iodine`, `dnscat2`, and `dns2tcp`.

---

## Detection Notes

Indicators of this specific exfiltration:

- DNS queries with **long, random-looking hex subdomains** under an internal TLD
- Queries where the subdomain has **uniform length** (10 chars = 5 bytes each time) — suggests a programmatic chunking scheme
- Queries to `.local` domains that **generate no legitimate response** (NXDOMAIN or silence)
- A **burst of queries in rapid succession** to the same second-level domain from the same host

A simple detection rule: alert on any DNS query where the leftmost label is `>8` characters, matches `[0-9a-f]+`, and the SLD is an internal domain.

---

## Flag

```
cycnet{9e3669d19b675d25050859043258f3c4}
```
