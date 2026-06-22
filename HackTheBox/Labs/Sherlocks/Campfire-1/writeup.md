1. Firstly to unzip on linux used 
```
7x x campfire-1.zip
```
Then you'll see two directorys with windows logs.

2. First question:
Analyzing Domain Controller Security Logs, can you confirm the UTC date & time when the kerberoasting activity occurred?
To dump the win logs on linux I used `chainsaw`
Exactly
```
chainsaw hunt -s ~/Tools/chainsaw/sigma/rules/windows/ --mapping ~/Tools/chainsaw/mappings/sigma-event-logs-all.yml .
```

Exact UTC time I found by this query: `2024-05-21 03:18:09`

3. Secant questions:
**What is the Service Name that was targeted?**
It's `MSSQLService`

4. Third questions: **It is really important to identify the Workstation from which this activity occurred. What is the IP Address of the workstation?**

So we are search by event ID: `4769` it's a Kerberos service ticket was requested
We can find the IP address by query previusly:
```
IpAddress: ::ffff:172.17.79.129
```

5. Next: **What is the full path of the tool used to perform the actual kerberoasting attack?**
Same query:
```
powerview.ps1
```

6. Next: **When was this script executed? (UTC)**
```
2024-05-21 03:16:32
```
7. **What is the full path of the tool used to perform the actual kerberoasting attack?**
Actually thought that answe is: `C:\Users\alonzo.spire\Downloads\powerview.ps1`. But we should find the path of **tool**. The tool is: `Rubeus`.
Answer:
```
C:\Users\Alonzo.spire\Downloads\Rubeus.exe
```

8. **When was the tool executed to dump credentials? (UTC)**
```
2024-05-21 03:18:08
```
