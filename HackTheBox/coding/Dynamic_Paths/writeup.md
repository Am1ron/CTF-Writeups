name: Dynamic Paths
category: Coding
description:On your way to the vault, you decide to follow the underground tunnels, a vast and complicated network of paths used by early humans before the great war. From your previous hack, you already have a map of the tunnels, along with information like distances between sections of the tunnels. While you were studying it to figure your path, a wild super mutant behemoth came behind you and started attacking. Without a second thought, you run into the tunnel, but the behemoth came running inside as well. Can you use your extensive knowledge of the underground tunnels to reach your destination fast and outrun the behemoth?
addition file: nc 154.57.164.73:31005

running netcat

```
nc 154.57.164.73 31005
You will be given a number of t = 100 grids for the different regions you need to pass. For every map you will have the below values:
        1. The dimensions i x j of the map grid where 2 <= i, j <= 100
        2. The numbers n_i,j symbolizing the distances between the blocks where 1 <= n_i,j <= 50
You will start at the top left element, and your goal is to reach the bottom right, while only being allowed to move down or right, minimizing the sum of the numbers you pass. Provide the minimum sum.

Example Question:
        4 3
        2 5 1 9 2 3 9 1 3 11 7 4

This generates the following grid:
         2 5 1
         9 2 3
         9 1 3
        11 7 4

Example Response:
        17
(Optimal route is 2 -> 5 -> 2 -> 1 -> 3 -> 4)

Test 1/100
2 2
8 5 1 9
> 
```

1. The Challenge Analysis

You are connected to a remote server that provides:

    Dimensions: i (rows) and j (columns).

    Grid: A flattened list of integers representing the "distance" or "cost" of each section of the tunnel.

    Constraint: You can only move Down or Right.

    Objective: Find the path from (0,0) to (i−1,j−1) that results in the smallest sum of values.

2. The Algorithm: Dynamic Programming

Since each move depends on the previous position, and we want to avoid re-calculating the same paths thousands of times, we use Dynamic Programming (DP).

For any cell (i,j), the minimum cost to reach it is:
DP[i][j]=grid[i][j]+min(DP[i−1][j],DP[i][j−1])

    Base Case: The starting cell DP[0][0] is just the value of grid[0][0].

    First Row: You can only reach these cells by moving right. So, DP[0][j]=DP[0][j−1]+grid[0][j].

    First Column: You can only reach these cells by moving down. So, DP[i][0]=DP[i−1][0]+grid[i][0]

Ответ Gemini
HTB Challenge: Dynamic Paths (Writeup)

This challenge is a classic Minimum Path Sum problem wrapped in a network service. To outrun the behemoth, you have to solve 100 increasingly large grids in a very short time.
1. The Challenge Analysis

You are connected to a remote server that provides:

    Dimensions: i (rows) and j (columns).

    Grid: A flattened list of integers representing the "distance" or "cost" of each section of the tunnel.

    Constraint: You can only move Down or Right.

    Objective: Find the path from (0,0) to (i−1,j−1) that results in the smallest sum of values.

2. The Algorithm: Dynamic Programming

Since each move depends on the previous position, and we want to avoid re-calculating the same paths thousands of times, we use Dynamic Programming (DP).

For any cell (i,j), the minimum cost to reach it is:
DP[i][j]=grid[i][j]+min(DP[i−1][j],DP[i][j−1])

    Base Case: The starting cell DP[0][0] is just the value of grid[0][0].

    First Row: You can only reach these cells by moving right. So, DP[0][j]=DP[0][j−1]+grid[0][j].

    First Column: You can only reach these cells by moving down. So, DP[i][0]=DP[i−1][0]+grid[i][0].

3. Solution

```
from pwn import *

def solve():
    # Connect to the instance
    r = remote('154.57.164.73', 31005)

    # 1. Skip instructions and wait for the first test marker
    r.recvuntil(b'Test 1/100')
    r.recvline()

    for i in range(100):
        # 2. Parse dimensions
        dim_line = r.recvline().decode().strip()
        while not dim_line: dim_line = r.recvline().decode().strip()
        rows, cols = map(int, dim_line.split())

        # 3. Parse grid data
        data_line = r.recvline().decode().strip()
        nums = list(map(int, data_line.split()))
        
        # Reshape flat list to 2D
        grid = [nums[k * cols:(k + 1) * cols] for k in range(rows)]

        # 4. DP Calculation
        dp = [[0] * cols for _ in range(rows)]
        dp[0][0] = grid[0][0]

        for j in range(1, cols):
            dp[0][j] = dp[0][j-1] + grid[0][j]
        for row_idx in range(1, rows):
            dp[row_idx][0] = dp[row_idx-1][0] + grid[row_idx][0]

        for row_idx in range(1, rows):
            for col_idx in range(1, cols):
                dp[row_idx][col_idx] = grid[row_idx][col_idx] + min(
                    dp[row_idx-1][col_idx], 
                    dp[row_idx][col_idx-1]
                )

        # 5. Submit answer
        r.sendline(str(dp[-1][-1]).encode())
        print(f"Level {i+1} solved.")

        # Prepare for next header
        if i < 99:
            r.recvuntil(b'Test')
            r.recvline()

    # 6. Capture the Flag
    r.interactive()

solve()
```


