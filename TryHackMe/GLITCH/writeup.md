<h1>GLITCH</h1>
<h2>Recognize</h2>
1. scanning with **nmap** shows that 80 ports are open 
```
80/tcp open  http    nginx 1.14.0 (Ubuntu)
```

2. scanning open directories on url with **gobuster**
```
/img                  (Status: 301) [Size: 173] [--> /img/]
/js                   (Status: 301) [Size: 171] [--> /js/]
/secret               (Status: 200) [Size: 724]
/Secret               (Status: 200) [Size: 724]
```

3. 
