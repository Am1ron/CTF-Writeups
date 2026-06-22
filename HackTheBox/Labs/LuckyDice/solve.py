from pwn import *
import re

HOST = '154.57.164.71'
PORT = 30458

r = remote(HOST, PORT)

r.recvuntil(b'> ')
r.sendline(b'1')  

r.recvuntil(b'Go!\n')

round_count = 0

try:
    while True:
        data = r.recvuntil(b'> ')
        print(data.decode('utf-8', errors='ignore')) 
        
        players_dice = re.findall(r'Player (\d+): ([\d ]+)', data.decode('utf-8'))
        
        max_score = -1
        winner_id = None
        
        for p_id, dice_str in players_dice:
            p_id = int(p_id)
            score = sum(map(int, dice_str.split()))

            if score >= max_score:
                max_score = score
                winner_id = p_id
        
        if winner_id is not None:
            round_count += 1
            print(f"[+] Round {round_count}: Winner is Player {winner_id} with score {max_score}")
            r.sendline(str(winner_id).encode())
            
except EOFError:
    print("[!] Соединение закрыто сервером.")
except Exception as e:
    print(f"[-] Произошла ошибка: {e}")

r.interactive()
