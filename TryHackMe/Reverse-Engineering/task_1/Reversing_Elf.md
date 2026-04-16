<h1>Write-Up Reversing ELF</h1>
file **crackme1**

#1 View all allowed strings
```
strings crackme1
```
Most interesting files:
* .data
* .rodata
* main

Use objdump to view bytes of each file.
objdump берет этот бинарник и превращает его обратно в текст (ассемблер) или показывает структуру файла.:
```
┌──(amir㉿kali)-[~/Reverse-Engineering]
└─$ objdump -s -j .data crackme1


crackme1:     file format elf64-x86-64


Contents of section .data:

 600a70 00000000 00000000 00000000 00000000  ................ 
```
================================================================
**Is missing. File empty** 

```
┌──(amir㉿kali)-[~/Reverse-Engineering]
└─$ objdump -s -j .rodata crackme1     

crackme1:     file format elf64-x86-64

Contents of section .rodata:
 400710 01000200                             ....
```

**Here is empty also**
=====================================================
**Lets view algorithm on main page**
```
objdump -d -M intel crackme1 | grep -A 20 "main"
```
1. **-d** - means Disassemble
2. **-M intel** - Этот флаг отвечает за диалект языка.

    Intel vs AT&T: В мире x86 есть два основных способа записывать ассемблер.
    AT&T (по умолчанию в Linux): Выглядит ужасно для новичка: movq %rsp, %rbp. Везде проценты и доллары.
    Intel: Выглядит чисто: mov rbp, rsp. Именно этот синтаксис используется в большинстве учебников и в самой Windows.

3. grep -A 20 "main"
**-A 20** (After): Это значит "покажи мне строку, где нашел слово 'main', и еще 20 строк ПОСЛЕ нее".
Если ты просто введешь grep "main", ты увидишь только одну строчку: 0000000000400546 <main>:


```
┌──(amir㉿kali)-[~/Reverse-Engineering]
└─$ objdump -d -M intel crackme1 | grep -A 20 "main"
0000000000400430 <__libc_start_main@plt>:
  400430:       ff 25 32 06 20 00       jmp    QWORD PTR [rip+0x200632]        # 600a68 <__libc_start_main@GLIBC_2.2.5>
  400436:       68 02 00 00 00          push   0x2
  40043b:       e9 c0 ff ff ff          jmp    400400 <.plt>

Disassembly of section .plt.got:

0000000000400440 <__gmon_start__@plt>:
  400440:       ff 25 f2 05 20 00       jmp    QWORD PTR [rip+0x2005f2]        # 600a38 <__gmon_start__>
  400446:       66 90                   xchg   ax,ax

Disassembly of section .text:

0000000000400450 <_start>:
  400450:       31 ed                   xor    ebp,ebp
  400452:       49 89 d1                mov    r9,rdx
  400455:       5e                      pop    rsi
  400456:       48 89 e2                mov    rdx,rsp
  400459:       48 83 e4 f0             and    rsp,0xfffffffffffffff0
  40045d:       50                      push   rax
  40045e:       54                      push   rsp
  40045f:       49 c7 c0 00 07 40 00    mov    r8,0x400700
--
  400474:       e8 b7 ff ff ff          call   400430 <__libc_start_main@plt>
  400479:       f4                      hlt
  40047a:       66 0f 1f 44 00 00       nop    WORD PTR [rax+rax*1+0x0]

0000000000400480 <deregister_tm_clones>:
  400480:       b8 87 0a 60 00          mov    eax,0x600a87
  400485:       55                      push   rbp
  400486:       48 2d 80 0a 60 00       sub    rax,0x600a80
  40048c:       48 83 f8 0e             cmp    rax,0xe
  400490:       48 89 e5                mov    rbp,rsp
  400493:       76 1b                   jbe    4004b0 <deregister_tm_clones+0x30>
  400495:       b8 00 00 00 00          mov    eax,0x0
  40049a:       48 85 c0                test   rax,rax
  40049d:       74 11                   je     4004b0 <deregister_tm_clones+0x30>
  40049f:       5d                      pop    rbp
  4004a0:       bf 80 0a 60 00          mov    edi,0x600a80
  4004a5:       ff e0                   jmp    rax
  4004a7:       66 0f 1f 84 00 00 00    nop    WORD PTR [rax+rax*1+0x0]
  4004ae:       00 00 
  4004b0:       5d                      pop    rbp
  4004b1:       c3                      ret
--
0000000000400546 <main>:
  400546:       55                      push   rbp
  400547:       48 89 e5                mov    rbp,rsp
  40054a:       48 81 ec a0 00 00 00    sub    rsp,0xa0
  400551:       89 bd 6c ff ff ff       mov    DWORD PTR [rbp-0x94],edi
  400557:       48 89 b5 60 ff ff ff    mov    QWORD PTR [rbp-0xa0],rsi
  40055e:       c7 45 90 25 00 00 00    mov    DWORD PTR [rbp-0x70],0x25
  400565:       c7 45 94 2b 00 00 00    mov    DWORD PTR [rbp-0x6c],0x2b
  40056c:       c7 45 98 20 00 00 00    mov    DWORD PTR [rbp-0x68],0x20
  400573:       c7 45 9c 26 00 00 00    mov    DWORD PTR [rbp-0x64],0x26
  40057a:       c7 45 a0 3a 00 00 00    mov    DWORD PTR [rbp-0x60],0x3a
  400581:       c7 45 a4 2d 00 00 00    mov    DWORD PTR [rbp-0x5c],0x2d
  400588:       c7 45 a8 2e 00 00 00    mov    DWORD PTR [rbp-0x58],0x2e
  40058f:       c7 45 ac 33 00 00 00    mov    DWORD PTR [rbp-0x54],0x33
  400596:       c7 45 b0 1e 00 00 00    mov    DWORD PTR [rbp-0x50],0x1e
  40059d:       c7 45 b4 33 00 00 00    mov    DWORD PTR [rbp-0x4c],0x33
  4005a4:       c7 45 b8 27 00 00 00    mov    DWORD PTR [rbp-0x48],0x27
  4005ab:       c7 45 bc 20 00 00 00    mov    DWORD PTR [rbp-0x44],0x20
  4005b2:       c7 45 c0 33 00 00 00    mov    DWORD PTR [rbp-0x40],0x33
  4005b9:       c7 45 c4 1e 00 00 00    mov    DWORD PTR [rbp-0x3c],0x1e
  4005c0:       c7 45 c8 2a 00 00 00    mov    DWORD PTR [rbp-0x38],0x2a
--
  40063b:       eb 2c                   jmp    400669 <main+0x123>
  40063d:       8b 45 fc                mov    eax,DWORD PTR [rbp-0x4]
  400640:       48 98                   cdqe
  400642:       0f b6 84 05 70 ff ff    movzx  eax,BYTE PTR [rbp+rax*1-0x90]
  400649:       ff 
  40064a:       89 c2                   mov    edx,eax
  40064c:       8b 45 fc                mov    eax,DWORD PTR [rbp-0x4]
  40064f:       48 98                   cdqe
  400651:       8b 44 85 90             mov    eax,DWORD PTR [rbp+rax*4-0x70]
  400655:       01 d0                   add    eax,edx
  400657:       89 c2                   mov    edx,eax
  400659:       8b 45 fc                mov    eax,DWORD PTR [rbp-0x4]
  40065c:       48 98                   cdqe
  40065e:       88 94 05 70 ff ff ff    mov    BYTE PTR [rbp+rax*1-0x90],dl
  400665:       83 45 fc 01             add    DWORD PTR [rbp-0x4],0x1
  400669:       8b 45 fc                mov    eax,DWORD PTR [rbp-0x4]
  40066c:       83 f8 1a                cmp    eax,0x1a
  40066f:       76 cc                   jbe    40063d <main+0xf7>
  400671:       48 8d 85 70 ff ff ff    lea    rax,[rbp-0x90]
  400678:       48 89 c7                mov    rdi,rax
  40067b:       e8 90 fd ff ff          call   400410 <puts@plt>
  400680:       b8 00 00 00 00          mov    eax,0x0
  400685:       c9                      leave
  400686:       c3                      ret
  400687:       66 0f 1f 84 00 00 00    nop    WORD PTR [rax+rax*1+0x0]
  40068e:       00 00 

0000000000400690 <__libc_csu_init>:
  400690:       41 57                   push   r15
  400692:       41 56                   push   r14
  400694:       41 89 ff                mov    r15d,edi
  400697:       41 55                   push   r13
  400699:       41 54                   push   r12
  40069b:       4c 8d 25 9e 01 20 00    lea    r12,[rip+0x20019e]        # 600840 <__frame_dummy_init_array_entry>
  4006a2:       55                      push   rbp
  4006a3:       48 8d 2d 9e 01 20 00    lea    rbp,[rip+0x20019e]        # 600848 <__do_global_dtors_aux_fini_array_entry>
  4006aa:       53                      push   rbx
  4006ab:       49 89 f6                mov    r14,rsi
```

#1. Ингредиенты (Стек)
Посмотри на этот блок команд mov:
Фрагмент кода
```
40055e: mov DWORD PTR [rbp-0x70], 0x25
400565: mov DWORD PTR [rbp-0x6c], 0x2b
...
```
Когда ты видишь много идущих подряд команд mov в память (адреса типа rbp-0x...), которые записывают туда числа — это явный признак того, что программа собирает строку или массив прямо в процессе работы.

Почему так? Разработчик не хотел, чтобы команда strings сразу нашла флаг. Он разбил его на отдельные байты и спрятал их внутри инструкций.

#2. Процесс готовки (Цикл)
Чуть ниже ты видишь странный прыжок jmp 400669 и последующий cmp eax, 0x1a с jbe (jump if below or equal).

    Что это: Это типичный цикл for или while.
    Как я это понял: Программа сравнивает счетчик в EAX с числом 0x1a (это 26 в десятичной системе). Значит, она делает что-то 26 раз — скорее всего, обрабатывает каждый символ флага.

#3. Cекретный соус (Математика)
Внутри цикла есть ключевая команда:
Фрагмент кода
```
400655: add eax, edx
```
Она берет байт (который, вероятно, является частью зашифрованного флага) и складывает его с другим числом. Это простейший алгоритм расшифровки.

эта программа шифрует (или расшифровывает) флаг прямо в памяти.

=========================================================================

<h1>Dynamical Analyze</h1>

run:
```
gdb ./crackme1
```

Поставь точку остановки (breakpoint) на функцию puts, потому что в этот момент флаг уже готов и лежит в памяти:
```
b puts
```
**b** - Breakpoint 

Run program
```
r
```

Когда программа остановится, флаг будет передан в функцию puts через регистр RDI (в Linux 64-bit первый аргумент функции всегда в RDI).
```
x/s $rdi
```

Это самая «магическая» команда. Разберем её по частям:

    x (Examine): Команда «исследовать память».

    /s (Format: String): Мы говорим GDB: «Трактуй те байты, которые ты найдешь, как текстовую строку (ASCII), пока не встретишь нулевой байт (конец строки)».

    $rdi (Register): В 64-битных системах Linux существует правило (Calling Convention): первый аргумент любой функции всегда кладется в регистр процессора RDI.

**As a result:** Breakpoint 1, 0x00007ffff7c80e60 in puts ()
   from /usr/lib/x86_64-linux-gnu/libc.so.6
(gdb) x/s $rdi
0x7fffffffdc60: "flag{not_that_kind_of_elf}"
(gdb) 
zsh: suspended  gdb ./crackme1

**Flag is: ** "flag{not_that_kind_of_elf}"


