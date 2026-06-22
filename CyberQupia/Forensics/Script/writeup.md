1. analyze file
```
file obfuscated.ps1 
obfuscated.ps1: ASCII text, with CR line terminators
```

2. Read file
```
cat obfuscated.ps1 
',"`n",' ',' ',' ',' ',"`$",'c','i','p','h','e','r','B','y','t','e','s',' ','=',' ','[','C','o','n','v','e','r','t',']',':',':','F','r','o','m','B','a','s','',"`n",' ',' ',' ',' ','f','o','r',' ',"`(","`$",'i',' ','=',' ','0',';',' ',"`$",'i',' ','-','l','t',' ',"`$",'c','i','p','h','e','r','B','y','t','e','s','.',"`n",' ',' ',' ',' ',' ',' ',' ',' ',"`$",'r','e','s','u','l','t',' ','+','=',' ',"`$",'c','i','p','h','e','r','B','y','t','e','s','[',"`$",'i',']',' ','-'',"`n",' ',' ',' ',' ','[','S','y','s','t','e','m','.','T','e','x','t','.','E','n','c','o','d','i','n','g',']',':',':','U','T','F','8','.','G','e','t','S','t',"`n","`$",'e','n','c','r','y','p','t','e','d','F','l','a','g',' ','=',' ','"','c','H','d','z','a','H','t','i','e','m','B','2','b','V','1','y','N','X','d','',"`n","`$",'y','o','u','t','u','b','e','L','i','n','k',' ','=',' ','"','h','t','t','p','s',':','/','/','w','w','w','.','y','o','u','t','u','b','e','.','c','',"`n",'W','r','i','t','e','-','H','o','s','t',' ','"','d','l','y','a',' ','p','o','l','u','c','h','e','n','i','e',' ','f','l','a','g','a',' ','n','a','z','h',"`n") -join ''); Invoke-Expression $obfuscated 
```
3. run on PowerShell
```
pwsh -File obfuscated.ps1
dlya poluchenie flaga nazhmite ssylku:
https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

4. On the function we see (almost) encrypted_flag = **"cHdzaHtiemlwbV1yNXdqcXZqXnFgczNzdV1hMW52Xm92bGltfA=="**
 * Also see key of XOR **$key = @([byte]1, [byte]2, [byte]3)**

5. Solution script
```
import base64

# Данные из скрипта
encrypted = "cHdzaHtiemlwbV1yNXdqcXZqXnFgczNzdV1hMW52Xm92bGltfA=="
key = [1, 2, 3]

# Шаг 1: Base64 → байты
cipher_bytes = base64.b64decode(encrypted)

# Шаг 2: XOR каждый байт с ключом (циклически)
result = []
for i, b in enumerate(cipher_bytes):
    result.append(b ^ key[i % len(key)])
    # key[i % 3] → 1, 2, 3, 1, 2, 3, 1, 2, 3...

# Шаг 3: байты → строка
flag = bytes(result).decode('utf-8')
print(flag)
```

Flag: **qupiya{ksl_q4uipti_scr1pt_b0lu_mumkn}**  - incorrect
flag: **qupiya{bul_q4uipti_scr1pt_b0lu_mumkn}**  - correct

