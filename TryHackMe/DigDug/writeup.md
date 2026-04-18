```
nmap -sV 10.112.189.17
```

Open ssh only (22)

```
dig axfr @10.112.189.17 givemetheflag.com
```

Error: connection refused.
Reasoning: The server does not support TCP-based zone transfers or bulk queries, which is a common security hardening measure (or a specific challenge constraint).

```
dig @10.112.189.17 givemetheflag.com A
```

;; ANSWER SECTION:
givemetheflag.com.  0  IN  TXT  "flag{0767ccd06e79853318f25aeb08ff83e2}"


