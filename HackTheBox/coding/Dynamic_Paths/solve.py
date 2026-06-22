from pwn import *

def solve():
    # Connect to the instance
    r = remote('154.57.164.63', 30978)

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
