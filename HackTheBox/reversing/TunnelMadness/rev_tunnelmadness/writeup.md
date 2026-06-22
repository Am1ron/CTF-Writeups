# TunnelMadness — HackTheBox CTF Writeup

**Category:** Reverse Engineering  
**Difficulty:** Medium  
**Flag:** `HTB{tunn3l1ng_ab0ut_in_3d_79e43e727fb2c1169e1b362a07856d8a}`

---

## Description

> Within Vault 8707 are located master keys used to access any vault in the country. Unfortunately, the entrance was caved in long ago. There are decades old rumors that the few survivors managed to tunnel out deep underground and make their way to safety. Can you uncover their tunnel and break back into the vault?

We're given a single ELF binary: `tunnel`.

---

## Reconnaissance

```bash
$ file tunnel
tunnel: ELF 64-bit LSB pie executable, x86-64, not stripped

$ strings tunnel | grep -E "HTB|flag|Direction|Cannot"
Direction (L/R/F/B/U/D/Q)?
Cannot move that way
/flag.txt
HTB{fake_flag_for_testing}
You break into the vault and read the secrets within...
```

Key observations from `strings`:
- The binary is a **navigation challenge** — it accepts directional inputs `L/R/F/B/U/D/Q`
- It reads from `/flag.txt` on success
- The binary is **not stripped**, so function names are preserved

Symbols visible in the binary:
| Symbol | Purpose |
|--------|---------|
| `main` | Entry point, game loop |
| `get_cell` | Look up a maze cell by coordinates |
| `prompt_and_update_pos` | Handle player movement |
| `get_flag` | Read and print `/flag.txt` |
| `maze` | The maze data array |

---

## Reversing the Maze Structure

### `get_cell` — indexing formula

Disassembling `get_cell` reveals how a 3D coordinate `(x, y, z)` maps to a memory address:

```asm
rax = x * 25 * 16  = x * 400
rdx = y * 5  * 4   = y * 20
rax = rax + rdx         ; 400x + 20y
rax = rax + z           ; 400x + 20y + z
rax = rax * 16          ; each cell = 16 bytes
rax = rax + &maze       ; final address
```

This tells us the maze is a **20×20×20 grid** (indices 0–19 on each axis), with each cell being **16 bytes**.

### Cell structure

Each 16-byte cell is a struct of four 32-bit integers:

```c
struct Cell {
    int x;     // stored x coordinate
    int y;     // stored y coordinate
    int z;     // stored z coordinate
    int type;  // cell type
};
```

Cell types found in the data:

| Type | Meaning |
|------|---------|
| `0` | Start cell `(0,0,0)` |
| `1` | Open passage |
| `2` | Wall (impassable) |
| `3` | Exit / Vault `(19,19,19)` |

Out of 8000 total cells: **7936 walls**, **62 passages**, **1 start**, **1 exit** — a very sparse maze.

### Direction mapping

By reading the **jump table** at `0x2080` and tracing each handler in `prompt_and_update_pos`:

```
U → z + 1    (up)
D → z - 1    (down)
R → x + 1    (right)
L → x - 1    (left)
F → y + 1    (forward)
B → y - 1    (back)
```

> ⚠️ **Gotcha:** `B` decrements y and `F` increments y — the opposite of what you might intuitively expect. This caused the first solve attempt to fail.

---

## Extracting the Maze

The `maze` symbol sits in `.rodata` at file offset `0x20e0`. We extract all 8000 cells directly from the binary with Python:

```python
import struct

with open('tunnel', 'rb') as f:
    data = f.read()

maze_file_offset = 0x20e0
SIZE = 20
maze = {}

for i in range(SIZE**3):
    offset = maze_file_offset + i * 16
    cx, cy, cz, ctype = struct.unpack_from('<iiii', data, offset)
    maze[(cx, cy, cz)] = ctype
```

---

## Solving the Maze (BFS)

With the full maze map in memory, we run a standard **Breadth-First Search** from `(0,0,0)` to `(19,19,19)`, treating any cell with `type == 2` as a wall:

```python
from collections import deque

moves = {
    'L': (-1, 0, 0), 'R': (1, 0, 0),
    'B': (0, -1, 0), 'F': (0, 1, 0),
    'D': (0, 0, -1), 'U': (0, 0, 1)
}

start, goal = (0, 0, 0), (19, 19, 19)
queue = deque([(start, [])])
visited = {start}

while queue:
    (x, y, z), path = queue.popleft()
    if (x, y, z) == goal:
        print(''.join(path))
        break
    for move, (dx, dy, dz) in moves.items():
        nx, ny, nz = x+dx, y+dy, z+dz
        if 0 <= nx < 20 and 0 <= ny < 20 and 0 <= nz < 20:
            if maze.get((nx,ny,nz), 2) != 2 and (nx,ny,nz) not in visited:
                visited.add((nx,ny,nz))
                queue.append(((nx,ny,nz), path+[move]))
```

**Result — 59 moves:**

```
UUURFURURRFRRFFUUFURRUFUFFRFUFUUUUFFRRUUUFURFDFFUFFRRRRRFRR
```

---

## Getting the Flag

Instead of typing 59 characters by hand, we automate the remote interaction with `pwntools`:

```python
from pwn import *

p = remote('154.57.164.83', 30305)

for c in "UUURFURURRFRRFFUUFURRUFUFFRFUFUUUUFFRRUUUFURFDFFUFFRRRRRFRR":
    p.sendlineafter(b'?', c.encode())

p.interactive()
```

Output:

```
[+] Opening connection to 154.57.164.83 on port 30305: Done
[*] Switching to interactive mode
 You break into the vault and read the secrets within...
HTB{tunn3l1ng_ab0ut_in_3d_79e43e727fb2c1169e1b362a07856d8a}
```

---

## Summary

| Step | Action |
|------|--------|
| 1 | `strings` + `file` for initial recon |
| 2 | `objdump -d` to reverse `get_cell` and understand maze indexing |
| 3 | Trace jump table to get exact direction → axis mappings |
| 4 | Parse maze data directly from binary with Python `struct` |
| 5 | BFS to find shortest path (59 moves) |
| 6 | `pwntools` to automate input on the remote server |

**Flag:** `HTB{tunn3l1ng_ab0ut_in_3d_79e43e727fb2c1169e1b362a07856d8a}`
