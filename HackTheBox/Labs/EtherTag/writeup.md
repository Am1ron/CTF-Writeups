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

4. 
