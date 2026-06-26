# CTF Writeup — The Legacy Drop

**Category:** Network Forensics  
**Flag:** `cycnet{202cb962ac59075b964b07152d234b70}`

---

## Challenge Description

> Our autonomous penetration testing agent, operating under the internal project alias **koshkar-muyiz** (a nod to traditional Kazakh geometric patterns), successfully bypassed standard proxy filters by uploading a compressed payload to a legacy file server. We intercepted the transmission. The agent always secures its exfiltrated archives using its project alias.

**Given file:** `ch4.pcapng`

---

## Solution

### Step 1 — Identify the capture

```
file ch4.pcapng
# ch4.pcapng: pcapng capture file - version 1.0 (1388 bytes)
```

The capture is small (~1.4 KB), recorded on the loopback interface (`lo`) using Wireshark/Dumpcap 4.4.6 on Linux. All traffic is local (127.0.0.1 ↔ 127.0.0.1).

### Step 2 — Find the ZIP payload

Scanning the raw bytes reveals `PK\x03\x04` — the ZIP local file header magic — at offset **0x027e** inside a TCP data segment. The archive contains a single encrypted file:

```
Archive:  extracted.zip
  Length      Date    Time    Name
---------  ---------- -----   ----
       41  2026-03-15 10:14   flag.txt
---------                     -------
       41                     1 file
```

The encryption flag is set, confirming the archive is password-protected.

### Step 3 — Extract the ZIP from the pcap

```python
with open('ch4.pcapng', 'rb') as f:
    data = f.read()

pk_start = data.find(b'PK\x03\x04')        # offset 638
pk_end   = data.rfind(b'PK\x05\x06')       # offset 851
zip_data = data[pk_start : pk_end + 22]    # +22 = end-of-central-directory record

with open('extracted.zip', 'wb') as f:
    f.write(zip_data)
```

### Step 4 — Crack the password

The challenge description is the hint: *"The agent always secures its exfiltrated archives using its project alias."*  
**Password = `koshkar-muyiz`**

```bash
unzip -P koshkar-muyiz extracted.zip -d out/
cat out/flag.txt
```

### Step 5 — Read the flag

```
cycnet{202cb962ac59075b964b07152d234b70}
```

---

## Summary

| Step | Action | Detail |
|------|--------|--------|
| 1 | Open pcap | Loopback TCP traffic, ~1.4 KB capture |
| 2 | Locate payload | `PK\x03\x04` magic at byte offset 638 |
| 3 | Carve ZIP | Extracted 235-byte password-protected archive containing `flag.txt` |
| 4 | Derive password | Project alias `koshkar-muyiz` from challenge description |
| 5 | Get flag | `cycnet{202cb962ac59075b964b07152d234b70}` |

---

## Key Takeaway

The challenge tested two skills:
- **Network forensics** — carving a file from raw TCP payload bytes in a pcapng without relying on protocol dissectors.
- **Close reading** — the password was hidden in plain sight in the challenge text. The project alias `koshkar-muyiz` doubled as the archive password.
