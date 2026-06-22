1. we have two file
 * upiya.pcapng
 * sslkeys.log

Open **.pcap** file go to **edit --> performance --> protocols --> TLC --> Master-Secret- log filename --> write path way to sslkeys.log**

2. Set filter to 
```
http
```

Or
```
http.request.method == "POST"
```

find only one traffic packet

3. Go to Follow --> HTTP Stream 
```
{"data": {"id": "f-421abe8ac0ecfaf39fbc91482cef75e28c0dfbc0e8f8ee0a2c1c476d4dd40d30-974c4bfc", "type": "comment", "links": {"self": "https://www.virustotal.com/api/v3/comments/f-421abe8ac0ecfaf39fbc91482cef75e28c0dfbc0e8f8ee0a2c1c476d4dd40d30-974c4bfc"}, "attributes": {"votes": {"positive": 0, "negative": 0, "abuse": 0}, "date": 1732903923, "text": "Heh", "html": "Heh", "tags": []}}}
```

4. Take hash and go to virustotal search following hash
```
421abe8ac0ecfaf39fbc91482cef75e28c0dfbc0e8f8ee0a2c1c476d4dd40d30
```

5. On comment find the base64
```
Y1hWd2FYbGhlMk15WDJOaGJsOWlaVjkyWVhKNWZRPT0=
```

6. 
```
echo "Y1hWd2FYbGhlMk15WDJOaGJsOWlaVjkyWVhKNWZRPT0=" | base64 -d                    
cXVwaXlhe2MyX2Nhbl9iZV92YXJ5fQ== 
```

Two times and get flag

7. Flag: **qupiya{c2_can_be_vary}**
