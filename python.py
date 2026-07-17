from math import *

n = 10 + 26 + 32724
i = ceil(log2(n))
ser = ceil(223 * i / 8)
for j in range(10000000000, 1, -1):
    if ser * j <= 17 * 1024 * 1024 * 1024:
        print(j)
        break
