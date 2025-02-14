#!/usr/bin/env python3
from z3 import *

s = Solver()
a = [BitVec(f"a1_{i}", 64) for i in range(8)]
def add_ascii_constraints(x):
    cons = []
    for i in range(8):
        byte = Extract(8*i+7, 8*i, x)
        cons.append(And(byte >= 0x20, byte <= 0x7e))
    return cons
for i in range(8):
    s.add(add_ascii_constraints(a[i]))

s.add(a[6] ^ a[5] ^ (a[7] + a[0]) == 0xB88FB0CA8FDFCE2D)
s.add(a[1] - a[3] + a[5] + a[7] == 0xB25FDA858CBBE9A4)
s.add(a[5] - a[2] + a[3] == 0x2A465263556B6C5D)
s.add((a[4] + a[5]) ^ (a[2] + a[3]) ^ a[1] ^ a[6] == 0x6536450F5A1B3745)
s.add(a[7] - a[0] - a[1] == 0xAE6E7A5B94717582)
s.add(a[5] ^ a[4] ^ a[6] == 0xB7C393329797A24)
s.add(a[2] ^ a[1] ^ a[3] == 0x50644262757E456D)
s.add((a[7] + a[6]) ^ a[0] == 0x8F3FE115AA2DBB2B)
s.add(a[4] + a[3] + a[5] == 0xF81C2E3328F84344)
s.add(a[1] + a[0] + a[2] == 0x3D275D492E2A5429)

if s.check() == sat:
    model = s.model()
    results = [model[a[i]].as_long() for i in range(8)]
    for i, val in enumerate(results):
        hex_str = f"{val:016X}"
        ascii_bytes = val.to_bytes(8, byteorder='little')
        try:
            ascii_str = ascii_bytes.decode('ascii')
        except:
            ascii_str = "<non-ascii>"
        print(f"a1[{i}] = {hex_str} -> {ascii_str}")
else:
    print("No solution found.")
