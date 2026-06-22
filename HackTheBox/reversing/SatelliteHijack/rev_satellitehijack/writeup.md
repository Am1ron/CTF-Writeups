# Satellite Hijack — HackTheBox CTF Writeup

**Category:** Reverse Engineering  
**Flag:** `HTB{l4y3r5_0n_l4y3r5_0n_l4y3r5!}`

---

## Files

- `satellite` — ELF 64-bit PIE, not stripped
- `library.so` — ELF 64-bit shared object, stripped

---

## Overview: Four Layers of Obfuscation

| # | What | Technique |
|---|------|-----------|
| 1 | Binary flow | Reads from fd=1 (stdout), calls `send_satellite_message` from `library.so` |
| 2 | Backdoor trigger | Env var name Caesar-encoded on stack; `getenv` check |
| 3 | Encrypted payload | 4096-byte blob XOR'd with `0x2a` via `memfrob`, mmap'd RWX |
| 4 | Runtime GOT hook | Blob patches GOT `read` entry; validates HTB{ control code |

---

## Step-by-Step Solution

### Step 1 — Reconnaissance

```bash
$ file satellite library.so
satellite:  ELF 64-bit LSB pie executable, x86-64, not stripped
library.so: ELF 64-bit LSB shared object, x86-64, stripped

$ strings satellite | grep -i lib
./library.so
send_satellite_message
```

`satellite` loads `./library.so` at runtime via `dlopen`/PLT and calls `send_satellite_message`.

---

### Step 2 — Reversing `main`

```
1. setbuf(stdout, 0)
2. puts(banner)
3. send_satellite_message(0, "START")    ← installs the hook
4. loop:
   a. putchar('> ')
   b. read(1, buf, 0x400)               ← fd=1 (stdout!) — hooked by blob
   c. if result < 0: "ERROR READING DATA", continue
   d. printf("Sending `%s`\n", buf)
   e. send_satellite_message(0, buf)
   f. goto 4
```

> **Key quirk:** `read(1, ...)` reads from fd=1 (stdout). Designed for socket use where stdin/stdout share one fd. This also means a PTY is required for local testing.

---

### Step 3 — The Encoded Env Var (Layer 2)

`send_satellite_message` at file offset `0x25d0` builds a string on the stack using three `movabs` instructions, then decodes it with a −1 Caesar shift:

```python
encoded = b'TBU`QSPE`FOWJSPONFOU'
decoded = bytes([b - 1 for b in encoded]).decode()
# → "SAT_PROD_ENVIRONMENT"
```

```c
if (getenv("SAT_PROD_ENVIRONMENT") != NULL) {
    install_hook();   // func_23e3
}
// else: silent return
```

The value doesn't matter — only presence is checked.

---

### Step 4 — The Encrypted Blob (Layer 3)

`func_23e3` (called when the env var is set):

1. `getauxval(AT_PHDR)` → page-align → get load base of `satellite`
2. Parse its ELF dynamic section to locate the GOT address of `read`
3. `mmap(NULL, 0x1000, RWX, ANON)` → allocate executable memory
4. `memcpy(mmap, lib+0x11a9, 0x1000)` → copy encrypted blob
5. `memfrob(mmap, 0x1000)` → XOR every byte with `0x2a` (decrypt)
6. **`*(void**)read_got = mmap`** → patch GOT so `read` calls the blob

```python
blob = library_data[0x11a9 : 0x11a9 + 0x1000]
decrypted = bytes([b ^ 0x2a for b in blob])
# First bytes: 41 57 41 56 ... = push r15; push r14; ... (valid x86-64 prologue)
```

---

### Step 5 — The Blob (Layer 4)

When `main` calls `read(1, buf, 0x400)`, it now calls the blob with `(fd=1, buf, 0x400)`.

**Blob flow:**

```
entry(fd, buf, size):
  do syscall read(0, buf, size)     ← reads from stdin/socket
  if fd != 1: return bytes_read     ← passthrough for other fds
  if bytes_read < 4: return
  scan buf for "HTB{" (0x7b425448 LE)
  if found:
    call compare(ptr_after_HTB{, remaining_len)
    if compare returns 1:
      zero out buf[0..bytes_read]   ← suppress echo
      return -1                     ← main prints "ERROR READING DATA"
  return bytes_read                 ← normal
```

---

### Step 6 — The Comparison Function

The comparison function at blob offset `0x8c` builds a reference string on the stack using four `movabs` instructions with **overlapping offsets**:

```asm
movabs rax, "l5{0v0Y7"   ; → [rsp-0x28]  (bytes 0..7)
movabs rdx, "fVf?u>|:"   ; → [rsp-0x20]  (bytes 8..15)
movabs rax, ">|:O!|Lx"   ; → [rsp-0x1b]  (bytes 13..20, overwrites 13-15)
movabs rdx, "!o$j,;f\0"  ; → [rsp-0x13]  (bytes 21..28)
```

> ⚠️ **The critical detail:** the third chunk is stored at `rsp-0x1b`, not `rsp-0x18`. This means it overlaps with and overwrites bytes 13–15 of the second chunk. Getting the offsets wrong produces the wrong stored string.

**Correct stored string** (32 bytes, use first 28):

```
l5{0v0Y7fVf?u>|:O!|Lx!o$j,;f
         ^^^          (positions 13-15 = ">|:" overwritten by chunk3)
```

The validation loop: `input[i] XOR stored[i] == i` for `i = 0..27`

Solving for `input`:

```python
stored = b'l5{0v0Y7fVf?u>|:O!|Lx!o$j,;f'
expected = bytes([stored[i] ^ i for i in range(28)])
# → b'l4y3r5_0n_l4y3r5_0n_l4y3r5!}'
```

Verification of last 5 bytes:
```
[23] 0x24 ^ 23 = 51 = '3'
[24] 0x6a ^ 24 = 114 = 'r'
[25] 0x2c ^ 25 = 53 = '5'
[26] 0x3b ^ 26 = 33 = '!'
[27] 0x66 ^ 27 = 125 = '}'
```

**Control code / flag:** `HTB{l4y3r5_0n_l4y3r5_0n_l4y3r5!}`

---

### Step 7 — Exploit (Local Verification)

Since `main` reads from fd=1 (stdout), we need a PTY where both stdin and stdout share the same channel. We write our input to the PTY master, which the blob reads from fd=0 inside the process.

```python
import os, pty, select, time

env = os.environ.copy()
env['SAT_PROD_ENVIRONMENT'] = '1'   # activate hook (any value)
env['LD_PRELOAD'] = './library.so'

stored = b'l5{0v0Y7fVf?u>|:O!|Lx!o$j,;f'
control = b'HTB{' + bytes([stored[i] ^ i for i in range(28)])
# → b'HTB{l4y3r5_0n_l4y3r5_0n_l4y3r5!}'

master, slave = pty.openpty()
pid = os.fork()
if pid == 0:
    os.dup2(slave, 0); os.dup2(slave, 1); os.dup2(slave, 2)
    os.execve('./satellite', ['./satellite'], env)

# Wait for "> " prompt then send control code
buf = b''
while b'> ' not in buf:
    r, _, _ = select.select([master], [], [], 3)
    if r: buf += os.read(master, 4096)

os.write(master, control + b'\n')
time.sleep(0.8)
out = b''
while True:
    r, _, _ = select.select([master], [], [], 0.5)
    if r: out += os.read(master, 4096)
    else: break

print(out.decode(errors='replace'))
```

**Output:**
```
HTB{l4y3r5_0n_l4y3r5_0n_l4y3r5!}
ERROR READING DATA        ← blob returned -1: comparison succeeded ✓
>
```

---

## Key Mistakes to Avoid

**Wrong stored string (common trap):** If you compute the third `movabs` chunk as `rsp-0x18` instead of `rsp-0x1b`, you get:
```
stored (wrong) = l5{0v0Y7fVf?u>|:>|:O!|Lx!o$j,;f
stored (right) = l5{0v0Y7fVf?u>|:O!|Lx!o$j,;f
```
The wrong derivation produces `HTB{l4y3r5_0n_l4y3r5.m(\5iZo9v>q}` which the binary rejects.

**Ignoring the fd=1 read:** Piping stdin directly (`echo "..." | ./satellite`) fails silently. A PTY is required.

---

## Summary

```
file / strings          → loads ./library.so, calls send_satellite_message
objdump main            → read(1,...) — reads from stdout fd; loop calls send_satellite_message
send_satellite_message  → movabs x3 → decode -1 → "SAT_PROD_ENVIRONMENT"
                        → getenv() NULL check → call func_23e3
func_23e3               → getauxval → find GOT[read] → mmap RWX → memcpy blob
                        → memfrob XOR 0x2a → patch GOT[read] = mmap
blob (hooked read)      → syscall read(0,...) → scan for "HTB{" → compare 28 bytes
compare func            → 4x movabs with OVERLAPPING stack offsets
                        → stored = l5{0v0Y7fVf?u>|:O!|Lx!o$j,;f
                        → check: input[i] XOR stored[i] == i
                        → expected = stored[i] ^ i = l4y3r5_0n_l4y3r5_0n_l4y3r5!}
PTY exploit             → send HTB{l4y3r5_0n_l4y3r5_0n_l4y3r5!} → ERROR = success
```

**Flag:** `HTB{l4y3r5_0n_l4y3r5_0n_l4y3r5!}`
