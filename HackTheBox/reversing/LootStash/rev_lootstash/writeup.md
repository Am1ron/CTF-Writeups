<h1>LootStash</h1>

**Category: Reversing**
**Objective: **
The program seeds a random number generator, picks a random index, and prints one "loot" item from a large array. We need to find the flag hidden somewhere within that massive list of strings.

**Analysis: **
run ```objdump -d stash```

* Seeding: It calls time(0) and then srand() (addresses 21d4–21db). This means the "randomness" depends on when you run the file.
* The Loop: It prints dots and sleeps (a simple distraction).
* The Logic: 1. It calls rand() at 2216.
2. It performs complex math (multiplication by a magic constant 0x8080808080808081) to calculate an index. This is standard compiler optimization for a modulo operation (likely index = rand() % count).
3. It uses this index to offset into an array called gear at 0x7060 (lea 0x4dfc(%rip), %rax).
4. It prints the string found at that address.

**Vulnerable: **
The "vulnerability" isn't a bug in the code, but the fact that the flag is stored as a plaintext string inside the binary's data section along with all the other "loot" items. We don't need to predict the rand() output if we can just search the binary's strings.

**Exploitation: **
combinate command ```strings``` and ```grep```

**Solution: **
```
strings stash | grep "HTB{"
```


