<h1>W1seGuy Writeup</h1>

A detailed walkthrough of the W1seGuy challenge on TryHackMe, focusing on XOR Cipher Analysis and
Known Plaintext Attacks.

The challenge provides a target IP and a service listening on port 1337. We are also given a Python source file (source.py) 
that demonstrates how the server encrypts a flag using a repeating 5-character XOR key.


#1. Initial Reconnaissance
1. Connecting to the Service

First, we connect to the target machine using Netcat:

nc <TARGET_IP> 1337

Output:

    This XOR encoded text has flag 1:<random>
	 What is the encryption key?

2. Analyzing the Source Code

The provided source.py reveals the following logic:

    The key is 5 characters long (randomly chosen from letters and digits).

    The encryption method is a Repeating XOR.

    We know the flag format: it starts with THM{ and ends with }.


#2. Solve.py
Save the following code as solve.py:

import string
import argparse

def xor_decrypt(cipher_hex, key):
    cipher_bytes = bytes.fromhex(cipher_hex)
    plaintext = ""
    for i in range(len(cipher_bytes)):
        key_char = key[i % len(key)]
        plaintext += chr(cipher_bytes[i] ^ ord(key_char))
    return plaintext

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--encrypted', required=True, help="Hex string from nc")
    args = parser.parse_args()

    cipher_hex = args.encrypted
    cipher_bytes = bytes.fromhex(cipher_hex)
    
    # Step 1: Recover first 4 chars of the key using "THM{"
    known_start = "THM{"
    key_prefix = ""
    for i in range(len(known_start)):
        key_prefix += chr(cipher_bytes[i] ^ ord(known_start[i]))
    
    print(f"[*] Guessed key prefix: {key_prefix}")

    # Step 2: Brute-force the 5th character (62 possibilities)
    charset = string.ascii_letters + string.digits
    for char in charset:
        full_key = key_prefix + char
        decrypted = xor_decrypt(cipher_hex, full_key)
        
        # Validate based on the known flag format (ends with '}')
        if decrypted.endswith("}"):
            print(f"[+] FOUND KEY: {full_key}")
            print(f"[+] DECRYPTED FLAG: {decrypted}")
            return

if __name__ == "__main__":
    main()

**Result:**

    Key Found: ...

    Flag 1 Found: THM{...}

Enter the 5-character key back into the Netcat session.

The server will verify the key and provide the Final Flag.

