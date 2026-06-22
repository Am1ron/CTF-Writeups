
# HTB Challenge Writeup — `dontpanic`

**Category:** Reverse Engineering  
**Flag:** `HTB{d0nt_p4n1c_c4tch_the_3rror}`

---

## Challenge Description

> You've cut a deal with the Brotherhood; if you can locate and retrieve their stolen weapons cache, they'll provide you with the kerosene needed for your makeshift explosives for the underground tunnel excavation. The team has tracked the unique energy signature of the weapons to a small vault, currently being occupied by a gang of raiders who infiltrated the outpost by impersonating commonwealth traders. Using experimental stealth technology, you've slipped by the guards and arrive at the inner sanctum. Now, you must find a way past the highly sensitive heat-signature detection robot. Can you disable the security robot without setting off the alarm?

---

## Reconnaissance

Start with basic file identification:

```bash
file dontpanic
# ELF 64-bit LSB pie executable, x86-64, dynamically linked, with debug_info, not stripped
```

The binary is a **Rust executable** — not stripped, which is helpful. Since it's Rust, we should expect that string data may not be stored as a single contiguous buffer. Rust tends to inline comparisons as immediate operands in the code section rather than as `.rodata` strings.

```bash
strings dontpanic | grep -E "HTB\{.+\}"
# (no output)
```

No flag in plaintext. The flag is hidden in the binary's logic.

---

## Finding the Flag Check Logic

The binary has debug symbols, so `nm` quickly reveals the interesting functions:

```bash
nm dontpanic | grep -v "_ZN"
```

Two key symbols stand out:

| Address    | Symbol                  |
|------------|-------------------------|
| `0x9060`   | `_ZN3src10check_flag`   |
| `0x9230`   | `_ZN3src4main`          |

The `check_flag` function is called from `main` after reading stdin, trimming the newline, and passing the string as `(ptr, len)`.

---

## Analyzing `check_flag`

Disassembling `check_flag` at `0x9060` reveals the core mechanic:

```asm
; First: assert input length == 0x1f (31)
91cd:  cmp    $0x1f,%rsi
91d1:  jne    9200          ; panic if wrong length

; Then: loop over each of 31 characters
91e0:  lea    0x1(%rax),%r14
91e4:  movzbl (%rbx,%rax,1),%edi   ; load input[i] into dil
91e8:  call   *0x10(%rsp,%rax,8)   ; call dispatch_table[i](input[i])
91ec:  mov    %r14,%rax
91ef:  cmp    $0x1f,%r14
91f3:  jne    91e0
```

The function builds a **dispatch table of 31 function pointers** on the stack (`0x10(%rsp)` through `0x100(%rsp)`). Each entry points to a tiny checker function. The loop calls `table[i](input[i])` — passing each input character to its dedicated validator.

This is **why a GDB memory scan fails**: the flag is never stored as a string. Each character lives as an immediate operand inside a separate function body.

---

## The Checker Functions

Each checker function follows the same 3-instruction pattern:

```asm
8b80:  push   %rax
8b81:  cmp    $0x48,%dil    ; compare input byte against expected
8b85:  jb     8b8b
8b87:  jne    8ba4          ; panic if mismatch
8b89:  pop    %rax
8b8a:  ret
```

There are 19 unique checker functions, one per distinct character in the flag:

| Function Address | Expected Byte | Character |
|-----------------|---------------|-----------|
| `0x8a40`        | `0x68`        | `h`       |
| `0x8a80`        | `0x70`        | `p`       |
| `0x8ac0`        | `0x74`        | `t`       |
| `0x8b00`        | `0x5f`        | `_`       |
| `0x8b40`        | `0x63`        | `c`       |
| `0x8b80`        | `0x48`        | `H`       |
| `0x8bc0`        | `0x6f`        | `o`       |
| `0x8c00`        | `0x30`        | `0`       |
| `0x8c40`        | `0x72`        | `r`       |
| `0x8c80`        | `0x6e`        | `n`       |
| `0x8cc0`        | `0x31`        | `1`       |
| `0x8d00`        | `0x34`        | `4`       |
| `0x8d40`        | `0x42`        | `B`       |
| `0x8d80`        | `0x54`        | `T`       |
| `0x8dc0`        | `0x65`        | `e`       |
| `0x8e00`        | `0x7b`        | `{`       |
| `0x8e40`        | `0x64`        | `d`       |
| `0x8e80`        | `0x33`        | `3`       |
| `0x8ec0`        | `0x7d`        | `}`       |

---

## Reconstructing the Flag

The dispatch table is built by a sequence of `lea` + `mov` instructions in `check_flag`. Each stores a function pointer into `0x10(%rsp) + 8*i`. By tracing the register values at each store (tracking `rax`, `rcx`, `rdx`, `rdi`), we recover the full ordered table:

| Slot (offset) | Function | Character |
|---------------|----------|-----------|
| `0x10` | `8b80` | `H` |
| `0x18` | `8d80` | `T` |
| `0x20` | `8d40` | `B` |
| `0x28` | `8e00` | `{` |
| `0x30` | `8e40` | `d` |
| `0x38` | `8c00` | `0` |
| `0x40` | `8c80` | `n` |
| `0x48` | `8ac0` | `t` |
| `0x50` | `8b00` | `_` |
| `0x58` | `8a80` | `p` |
| `0x60` | `8d00` | `4` |
| `0x68` | `8c80` | `n` |
| `0x70` | `8cc0` | `1` |
| `0x78` | `8b40` | `c` |
| `0x80` | `8b00` | `_` |
| `0x88` | `8b40` | `c` |
| `0x90` | `8d00` | `4` |
| `0x98` | `8ac0` | `t` |
| `0xa0` | `8b40` | `c` |
| `0xa8` | `8a40` | `h` |
| `0xb0` | `8b00` | `_` |
| `0xb8` | `8ac0` | `t` |
| `0xc0` | `8a40` | `h` |
| `0xc8` | `8dc0` | `e` |
| `0xd0` | `8b00` | `_` |
| `0xd8` | `8e80` | `3` |
| `0xe0` | `8c40` | `r` |
| `0xe8` | `8c40` | `r` |
| `0xf0` | `8bc0` | `o` |
| `0xf8` | `8c40` | `r` |
| `0x100` | `8ec0` | `}` |

Concatenating all 31 characters in order:

```
HTB{d0nt_p4n1c_c4tch_the_3rror}
```

---

## Why the Initial GDB Approach Failed

The original GDB scan searched for a byte pattern (`0x40 0x80 0xff`) in the `.data` region (`0x8000–0x9000`). The `cmp $X, %dil` instruction has the encoding `40 80 ff XX` — so the approach was correct in principle, but:

1. **Wrong memory region** — the checker functions live in `.text` (code), not `.data`
2. **The scan found bytes out of order** — characters were discovered non-sequentially and mixed with GDB's own terminal output
3. **No contiguous flag string exists** — Rust's compiler never created one; each byte is an isolated immediate in a separate function

The correct approach is to treat the **dispatch table construction code** as the data source, tracing which function pointer gets stored at each index.

---

## Key Takeaway

Rust binaries frequently use per-character validator functions generated by monomorphization or match-arm lowering. When you see a loop over a table of function pointers where each function does a single comparison, the flag is encoded **as the ordering of those pointer assignments** — not as any stored string literal.

---

**Flag: `HTB{d0nt_p4n1c_c4tch_the_3rror}`**
