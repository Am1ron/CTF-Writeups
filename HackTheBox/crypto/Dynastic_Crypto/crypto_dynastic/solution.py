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

