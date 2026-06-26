# Suspicious Gallery — CTF Forensics Writeup

**Challenge:** Suspicious Gallery  
**Category:** Forensics  
**Flag:** `CUTS{p4ck3t5_4nd_p1x3l5_gr8}`

---

## Description

> Our intelligence team intercepted suspicious file uploads to `gallery.cuts.uz`. Figure out what they are hiding!

We're given a `capture.pcap` file (~2MB). The domain name `gallery.cuts.uz` is a hint that the flag format is `CUTS{...}`.

---

## Step 1 — Reconnaissance

Start with a high-level look at the capture:

```bash
file capture.pcap
# pcap capture file, microsecond ts (little-endian) - version 2.4 (Ethernet)
```

Parsing the packet stream reveals **16 TCP flows** between two hosts:

| Client | Server |
|---|---|
| `192.168.1.105` | `10.20.30.40:80` |

The flows break down into a clear pattern:
- **4× POST** `/gallery/upload` — image uploads
- **4× GET** `/gallery/photos/photoN.png` — image downloads
- **8× HTTP responses** (one per request)

The server is `gallery-server/1.0` and responses confirm filenames: `photo1.png` through `photo4.png`.

---

## Step 2 — Extracting the Images

Since there's no `tshark` or `wireshark` in the environment, images are extracted manually by parsing raw TCP streams.

Each **POST** request is a `multipart/form-data` upload with boundary `WebKitFormBoundary000000000000000N`. The PNG data starts at the `\x89PNG` magic bytes inside the multipart body.

Four uploaded PNGs are extracted (all `400×300`, RGB, ~243KB each):

```
upload1.png  upload2.png  upload3.png  upload4.png
```

---

## Step 3 — PNG Chunk Analysis

Inspecting every PNG chunk reveals anomalies:

```
upload1.png  →  IHDR, IDAT×4, IEND         (no metadata)
upload2.png  →  IHDR, tEXt, IDAT×4, IEND   ← Comment: "4nd_"
upload3.png  →  IHDR, IDAT×4, IEND         (no metadata)
upload4.png  →  IHDR, tEXt, IDAT×4, IEND   ← Comment: "nothing to see here :)"
```

Two images have `tEXt` chunks:
- `upload2.png` → `4nd_` — looks like a **flag fragment**
- `upload4.png` → `nothing to see here :)` — a **decoy / red herring**

This is suspicious. The fragment `4nd_` suggests a flag of the form `CUTS{..._4nd_...}`.

---

## Step 4 — LSB Steganography

The images look visually similar but differ at the pixel level. The approach:

1. **Decompress** the IDAT zlib stream for each image
2. **Apply PNG filter reconstruction** properly (filter types 0–4) to recover true pixel values
3. **Extract LSBs** (least-significant bits) from every pixel byte in R, G, B order, row by row
4. **Pack** the bits into bytes and read the message

```python
import zlib, struct

def decode_png_proper(fname):
    # ... parse IHDR and IDAT chunks ...
    raw = zlib.decompress(idat_data)
    stride = width * 3
    prev_row = bytes(stride)
    recon = []
    for y in range(height):
        ftype = raw[y * (stride+1)]
        scanline = bytearray(raw[y*(stride+1)+1 : y*(stride+1)+1+stride])
        # apply filter (None/Sub/Up/Average/Paeth)
        ...
        recon.append(bytes(scanline))
        prev_row = bytes(scanline)
    return recon

def get_lsbs_as_bytes(rows, max_bytes=50):
    bits = [b & 1 for row in rows for b in row]
    return bytes(
        int(''.join(str(b) for b in bits[i:i+8]), 2)
        for i in range(0, max_bytes*8, 8)
    )
```

> **Important:** PNG filter reconstruction must happen *before* LSB extraction. Without it, the decompressed bytes are *filtered residuals*, not actual pixel values — the LSB message will be garbage.

### Results

| Image | LSB message (null-terminated) |
|---|---|
| `upload1.png` | **`CUTS{p4ck3t5_`** |
| `upload2.png` | (noise — flag piece carried in `tEXt` chunk instead) |
| `upload3.png` | **`p1x3l5_gr8}`** |
| `upload4.png` | (noise — `tEXt` chunk is decoy) |

---

## Step 5 — Flag Assembly

The flag is split across three different hiding spots:

```
upload1.png  →  LSB steganography  →  CUTS{p4ck3t5_
upload2.png  →  PNG tEXt chunk     →  4nd_
upload3.png  →  LSB steganography  →  p1x3l5_gr8}
```

Concatenating in order:

```
CUTS{p4ck3t5_} + 4nd_ + p1x3l5_gr8}
     ↓
CUTS{p4ck3t5_4nd_p1x3l5_gr8}
```

---

## Flag

```
CUTS{p4ck3t5_4nd_p1x3l5_gr8}
```

---

## Key Takeaways

- **Always inspect PNG chunks** beyond IHDR/IDAT/IEND — `tEXt`, `zTXt`, `iTXt` etc. can carry hidden data
- **PNG filter reconstruction is mandatory** before LSB extraction — skipping it produces random noise
- **Red herrings are real** — `upload4.png`'s `"nothing to see here :)"` comment was designed to waste time
- **Flag fragments can be spread** across multiple files and multiple steganographic techniques in a single challenge
- Tools like `zsteg` or `stegseek` would have automated the LSB discovery; manual Python analysis is a reliable fallback when tooling is unavailable
