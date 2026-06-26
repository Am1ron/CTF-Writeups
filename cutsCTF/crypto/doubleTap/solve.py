def xor_hex(hex1, hex2):
    return bytes(a ^ b for a, b in zip(bytes.fromhex(hex1), bytes.fromhex(hex2)))

ct_a = "075307e71df24a356279a2c5014c15f509fe167c4448d6fb1f4756e631f01f25586fe7dd170c39a51dc4486f6679eed119"
ct_b = "0b4f03fa4ef95e336679e1c9174b5cb40ff7407c7464f1dc015215b400f44135697cee84445109b40ff7492e736ea38945"
pt_b = b"open broadcast: all systems nominal, no alerts!!!"

# Step 1: XOR ciphertexts to get P_A ^ P_B
xor_ciphertexts = xor_hex(ct_a, ct_b)

# Step 2: XOR the result with PT_B to isolate PT_A
pt_a = bytes(a ^ b for a, b in zip(xor_ciphertexts, pt_b))

print(f"Decrypted Message: {pt_a.decode()}")

