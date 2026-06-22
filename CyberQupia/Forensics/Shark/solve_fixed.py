import struct
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# ── 1. Read PCAP ──────────────────────────────────────────────────────────────
data = open('qupiya.pcap', 'rb').read()
pos = 24
packets = []
while pos + 16 <= len(data):
    incl_len = struct.unpack_from('<I', data, pos + 8)[0]
    pkt = data[pos + 16 : pos + 16 + incl_len]
    packets.append(pkt)
    pos += 16 + incl_len

# ── 2. Extract mouse HID payload (4 bytes after 27-byte USB header) ───────────
moves = []
for pkt in packets:
    p = pkt[27:]
    if len(p) == 4:
        buttons = p[0]
        dx = struct.unpack_from('b', p, 1)[0]   # signed
        dy = struct.unpack_from('b', p, 2)[0]   # signed
        moves.append((dx, dy, buttons))

print(f'Total mouse events: {len(moves)}')
print(f'First 10: {moves[:10]}')

# ── 3. Compute trajectory ─────────────────────────────────────────────────────
x, y = 0, 0
coords = [(x, y)]
for dx, dy, btn in moves:
    x += dx
    y += dy
    coords.append((x, y))

xs = [c[0] for c in coords]
ys = [c[1] for c in coords]
print(f'X range: {min(xs)} to {max(xs)}')
print(f'Y range: {min(ys)} to {max(ys)}')

# ── 4. Plot (Y inverted — screen coords) ──────────────────────────────────────
ys_inv = [-y for y in ys]

fig, ax = plt.subplots(figsize=(28, 10))
ax.set_facecolor('black')
fig.patch.set_facecolor('black')
ax.plot(xs, ys_inv, color='white', linewidth=0.8)
ax.set_aspect('equal')
ax.axis('off')
plt.tight_layout()
plt.savefig('flag.png', dpi=200, bbox_inches='tight', facecolor='black')
print('Saved flag.png')
