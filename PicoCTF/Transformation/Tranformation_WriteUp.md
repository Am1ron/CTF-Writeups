<h1>Transformation</h1>

**Decription:** I wonder what this really is...
enc ''.join([chr((ord(flag[i]) << 8) + ord(flag[i + 1])) for i in range(0, len(flag), 2)])

**Additional file: ** 'enc'
```
灩捯䍔䙻ㄶ形楴獟楮獴㌴摟潦弸形㝦㘲捡㕽
```

#1. Analyze of the algorithm (encoded).
Inside of file 'enc' we see encoded result which looks like a Chinese character)

The code takes two flag characters and combines them into one large unicode character.

new_char=(char1​≪8)+char2​

* ord(flag[i]) << 8: Takes the ASCII code of the first character and shifts it 8 bits to the left. In fact, this is multiplication by 28 (or 256).
* + ord(flag[i + 1]): adds the code of the second character to the lower 8 bits that have been released.
* chr(...): Turns the resulting number into a single character (which often looks like a Chinese character).

#2. Solution (decoded)
To get the original characters, we need to do the opposite.:

* First character: Get the highest 8 bits (divided by 256).
* Second character: Get the lower 8 bits (take the remainder of the division by 256).


Python script:
```
encoded_str = open('enc').read()
print(''.join([chr(ord(c) >> 8) + chr(ord(c) & 0xFF) for c in encoded_str]))
```

* **ord(c) >> 8:**  Shifts the bits to the right, returning us the first character.
* **ord(c) & 0xFF:** Uses a bitwise "And" (mask) to pick up only the last 8 bits — our second character. 

**As a result** picoCTF{flag}


