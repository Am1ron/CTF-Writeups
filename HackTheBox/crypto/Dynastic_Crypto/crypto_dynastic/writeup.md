Description

The challenge provides a Python encryption script and an output file containing a ciphertext. The goal is to reverse the encryption algorithm to retrieve the original flag.

1. Technical Analysis

The encryption function encrypt(m) in source.py follows these rules:

    Identity Mapping: Characters are converted to a 0-25 integer range (A=0,B=1,…) using ord(a) - 0x41.

    Position-Based Shift: For every character at index i, the algorithm adds the value of i to the character's integer representation.

    Modulo Operation: The result is kept within the alphabet range using % 26.

    Non-Alphabetic Characters: Symbols like underscores (_), question marks (?), and exclamation points (!) are skipped and remain unchanged.

2. The mathematical formula for the encryption is:
Ei​=(Pi​+i)(mod26)

3. Decryption Logic

To decrypt the message, we simply subtract the index i from the ciphertext character index:
Pi​=(Ei​−i)(mod26)

4. Solution

```
def decrypt(c):
    m = ''
    for i in range(len(c)):
        ch = c[i]
        if not ch.isalpha():
            mch = ch
        else:
            # Convert char to 0-25, subtract index, wrap with modulo
            chi = ord(ch) - 0x41
            mch = chr((chi - i) % 26 + 0x41)
        m += mch
    return m

ciphertext = "DJF_CTA_SWYH_NPDKK_MBZ_QPHTIGPMZY_KRZSQE?!_ZL_CN_PGLIMCU_YU_KJODME_RYGZXL"
print(f"HTB{{{decrypt(ciphertext)}}}")
```


