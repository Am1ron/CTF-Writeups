from Crypto.Util.number import getPrime, bytes_to_long
from math import gcd

p = getPrime(2048)
q = getPrime(2048)
phi = (p-1)*(q-1)
e = getPrime(4)
while gcd(e, phi) != 1:
    p = getPrime(2048)
    q = getPrime(2048)
    phi = (p-1)*(q-1)
n = p*q
d = pow(e, -1, phi)

flag = b"qupiya{fake_flag}"
flag = bytes_to_long(flag)
ct = pow(flag, e, n)
print(f"{ct=}")
