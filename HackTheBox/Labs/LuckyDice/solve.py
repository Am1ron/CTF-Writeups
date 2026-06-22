from pwn import *
import re

# Настройки подключения
HOST = '154.57.164.71'
PORT = 30458

r = remote(HOST, PORT)

# 1. Проходим стартовое меню
r.recvuntil(b'> ')
r.sendline(b'1')  # Соглашаемся на игру

# Ждем обратный отсчет (3... 2... 1... Go!)
r.recvuntil(b'Go!\n')

round_count = 0

try:
    while True:
        # Читаем данные раунда
        data = r.recvuntil(b'> ')
        print(data.decode('utf-8', errors='ignore')) # Выводим в консоль для дебага
        
        # Регуляркой вытаскиваем все строки вида "Player X: Y Z ..."
        # Группа 1: номер игрока, Группа 2: все его кубики
        players_dice = re.findall(r'Player (\d+): ([\d ]+)', data.decode('utf-8'))
        
        max_score = -1
        winner_id = None
        
        for p_id, dice_str in players_dice:
            p_id = int(p_id)
            # Считаем сумму кубиков игрока
            score = sum(map(int, dice_str.split()))
            
            # Если счет БОЛЬШЕ или РАВЕН (>=), обновляем победителя.
            # Знак ">=" автоматически закроет правило №4, так как более 
            # поздний игрок с таким же счетом перезапишет предыдущего.
            if score >= max_score:
                max_score = score
                winner_id = p_id
        
        # Отправляем ответ (номер выигравшего игрока)
        if winner_id is not None:
            round_count += 1
            print(f"[+] Round {round_count}: Winner is Player {winner_id} with score {max_score}")
            r.sendline(str(winner_id).encode())
            
except EOFError:
    print("[!] Соединение закрыто сервером.")
except Exception as e:
    print(f"[-] Произошла ошибка: {e}")

r.interactive()
