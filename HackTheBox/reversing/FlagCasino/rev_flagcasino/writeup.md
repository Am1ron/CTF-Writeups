<h1>FlagCasino</h1>

**Category: Reversing**
**Objective:**
The program asks for 29 consecutive "winning" inputs. 
We need to identify the expected input for each stage to unlock the flag.

**Analyzing: **
Running 
```
objdump -d casino
```

The binary is a stripped 64-bit ELF. Looking at main:

    Loop: Runs exactly 29 times (cmp $0x1c, %eax at 125b).

    Input: Reads a single byte via scanf.

    Algorithm: 1.  The input byte is passed to srand(input).
    2.  rand() is called immediately.
    3.  The result is compared against a hardcoded 4-byte integer in the check array located at 0x4080.

**Vulnarable: The Seed-to-Output mapping is too small. Since the seed (srand) is only 1 byte (0-255), there are only 256 possible outputs for the first rand() call at any given step. This makes it trivial to brute-force.**

**Explotation: We need to extract the target integers from the check array**
 * Load: gdb ./casino
 * Extract: x/29dw 0x4080 (dumps 29 decimal words starting at the array address).

**Solution: **
```
import ctypes

# Load glibc for identical rand() behavior
libc = ctypes.CDLL("libc.so.6")

targets = [
    608905406, 183990277, 286129175, 128959393, 1795081523, 
    1322670498, 868603056, 677741240, 1127757600, 89789692, 
    421093279, 1127757600, 1662292864, 1633333913, 1795081523, 
    1819267000, 1127757600, 255697463, 1795081523, 1633333913, 
    677741240, 89789692, 988039572, 114810857, 1322670498, 
    214780621, 1473834340, 1633333913, 585743402
]

flag = ""
for target in targets:
    for i in range(256):
        libc.srand(i)
        if libc.rand() == target:
            flag += chr(i)
            break

print(f"Flag: {flag}")
```


