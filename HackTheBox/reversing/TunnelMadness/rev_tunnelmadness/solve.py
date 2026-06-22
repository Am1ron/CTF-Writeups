from pwn import *
p = remote('154.57.164.65', 31896)
for c in "UUURFURURRFRRFFUUFURRUFUFFRFUFUUUUFFRRUUUFURFDFFUFFRRRRRFRR":
	p.sendlineafter(b'?', c.encode())
	p.interactive()
