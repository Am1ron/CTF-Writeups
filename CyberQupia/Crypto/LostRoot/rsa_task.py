from Crypto.Util.number import getPrime

p,q = getPrime(256), getPrime(256)
n = p*q
a = getPrime(128)
c1 = (p-a)**2>>128
c2 = (q+a)**2>>128
e = 65537
ct = pow(int.from_bytes(b'qupiya{fake_flag}','little'), e, n)
print(f"{n=}")
print(f"{c1=}")
print(f"{c2=}")
print(f"{ct=}")