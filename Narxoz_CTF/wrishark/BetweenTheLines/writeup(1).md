# CTF Writeup: Between the Lines

**Category:** Network Forensics  
**Flag:** `CYCNET{7d4e2f1a9b3c8e5d0f6a2b4c7e9d1f3a}`

---

## Challenge Description

> Your DLP tool flagged outbound HTTP traffic to an internal wiki at an unusual hour. The pages looked harmless — chapter titles, placeholder text. But the analyst who reviewed it noticed the responses were carrying something extra. Something the browser silently ignored.

---

## Overview

This challenge presents a `.pcap` file containing HTTP traffic to an internal wiki server (`wiki.corp`). The page bodies are completely benign — lorem-ipsum-style chapter text. The exfiltrated data is hidden in **custom HTTP response headers**, split across four sequential requests. A browser would never surface these headers to the user, making this a clean covert channel.

---

## Solution

### Step 1: Inspect the PCAP

Open the capture file and filter for HTTP traffic. The PCAP contains 219 packets, 38 of which carry TCP payload data.

```bash
# Using Python to parse manually (or tshark/Wireshark)
# Filter: tcp && http
```

Several hosts appear in the traffic: `wiki.corp`, `portal.corp`, `gitlab.corp`, `jira.corp`. Most are noise. Focus on `wiki.corp`.

---

### Step 2: Identify the Suspicious Headers

Early responses from `wiki.corp` include decoy custom headers to blend in:

| Endpoint | Decoy Header |
|---|---|
| `GET /` | `X-Session-ID: a1b2c3d4e5f6a7b8` |
| `GET /about` | `X-Request-ID: 9f8e7d6c5b4a3210` |
| `GET /docs` | `X-Token: nottheflagkeeplooking` |
| `GET /api/status` | `X-Content-Token: deadbeefcafe0000` |
| `GET /search` | `X-Session-ID: 0011223344556677` |

Note the `X-Token: nottheflagkeeplooking` — a deliberate troll embedded in the traffic.

---

### Step 3: Follow the Wiki Pages

The authenticated session (`Cookie: session=s3ss10n`) hits four sequential `/page/N` endpoints. Each response carries an `X-Content-Token` header:

| Request | `X-Content-Token` |
|---|---|
| `GET /page/1` | `CYCNET{7d4e` |
| `GET /page/2` | `2f1a9b3c` |
| `GET /page/3` | `8e5d0f6a` |
| `GET /page/4` | `2b4c7e9d1f3a}` |

The page bodies are red herrings. Chapter 3 even includes a meta-hint in its content:

> *"The answer was in the headers all along."*

---

### Step 4: Assemble the Flag

Concatenate the four `X-Content-Token` values in order:

```
CYCNET{7d4e  +  2f1a9b3c  +  8e5d0f6a  +  2b4c7e9d1f3a}
```

```
CYCNET{7d4e2f1a9b3c8e5d0f6a2b4c7e9d1f3a}
```

---

## Flag

```
CYCNET{7d4e2f1a9b3c8e5d0f6a2b4c7e9d1f3a}
```

---

## Key Takeaways

**Technique:** HTTP header steganography / covert channel exfiltration  
**Why it bypasses DLP:** Most DLP tools inspect request bodies, URLs, and common fields. Custom `X-*` response headers are frequently overlooked or not included in inspection rulesets. Browsers silently discard unrecognized headers, so the data is invisible to end users.

**Detection indicators:**
- Unusual custom response headers (`X-Content-Token`) on wiki/internal pages
- Sequential requests to paginated endpoints at odd hours
- Flag-like patterns (`{...}`) appearing split across multiple header values
- Traffic from an authenticated session to non-interactive endpoints at an unusual time

**Mitigation:** Configure DLP and web proxies to inspect all HTTP header fields, not just request bodies. Alert on non-standard `X-*` headers in responses from internal servers.
