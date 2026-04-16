<h1>Core Fundamental</h1>

A. Architecture of process (x86/x64)

* x86 - 32-bit memory. Limited to 4 GB of RAM 
* x64 - 64-bit memory. Can address over 16 exabytes, allowing for significantly faster performance

Программы не работают с переменными типа name или count. Они работают с:

    Регистрами: Это сверхбыстрые ячейки памяти внутри процессора.

        RAX, RBX, RCX, RDX — регистры общего назначения.

        RSP (Stack Pointer) — указывает на вершину стека.

        RIP (Instruction Pointer) — самый важный: он указывает на адрес следующей команды, которую выполнит процессор.

B. File Formats

* ELF (Executable and Linkable Format) — стандарт для Linux.
* PE (Portable Executable) — стандарт для Windows (.exe, .dll).
* Нужно знать, что такое секции: .text (здесь лежит сам код), .data (глобальные переменные), .rodata (текстовые строки).

<h1>Tools</h1>

* Statical analyze - Ghidra
	Статический анализ означает, что мы не запускаем программу, а просто изучаем её код.
	Ghidra разбирает бинарный файл (нули и единицы) и превращает их в Ассемблер, а затем — в псевдокод на Си.
* Dynamcal analyze - GDB
	Динамический анализ — это когда мы запускаем программу в контролируемой среде.
	GDB (GNU Debugger) позволяет тебе остановить программу в любой момент (поставить breakpoint).
* Универсальный комбайн - Radare2
	Всё то же самое, что Ghidra и GDB вместе взятые, но в терминале.
	Он невероятно быстрый и его легко автоматизировать скриптами. В нем можно и анализировать код, и сразу же его "патчить" 
	(изменять байты прямо в файле).
* Разведка - strings, file, nm (Показывает список имен функций (символов) внутри файла)



<h1>Assembler</h1>
1. Must know what do **mov, add, sub, jmp, cmp, call и ret.**
2. Must understand **"Calling Conventions"** Как функции передают данные друг другу через стек или регистры (например, System V AMD64 ABI в Linux).
3. Практикуйся на Crackmes:

    Скачай простое задание на Crackmes.one.

    Попробуй найти в коде проверку пароля и изменить логику так, чтобы любой пароль считался верным (это называется Patching).


**objdump -s -j .data:**

    -s (full-contents): Говорит утилите показать полное содержимое секции, а не только заголовки.

    -j .data (section): Указывает конкретную секцию. Без этого флага objdump вывалил бы тебе вообще всё содержимое файла (а там мегабайты мусора).

**readelf -x .data:**

    -x (hex-dump): Выводит содержимое секции в шестнадцатеричном виде. По сути, делает то же самое, что и objdump -s, но иногда в более удобном формате.


<h1>CRACKME-5</h1>

use 

```
ltrace ./crackme
```


<h1>CRACKME-6</h1>
```
objdump -d ./crackme6
```

Search function
** my_secure_test**

compare input value with password by ascii. Convert ascii value and get password


