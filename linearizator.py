import random
from itertools import combinations, product
from math import log2
from sympy.logic.boolalg import ANFform
from sympy import var
import random
import sys
from PIL import Image
import os
from PIL import Image
import math
from PIL import Image
import numpy as np
import fractions
from fractions import Fraction
path = "C:/Users/Maxim/PycharmProjects/circuit-synthesis/iwls2025/truth_tables/ex181.truth"
gap = 1
linesmax = 15
def array(file_name):
    # print(f'Analyzing truth tables from the file {file_name}')

    # sys.stdout = f  # Redirect print output to file
    with open(file_name) as file:
        _truth_tables = [table.strip() for table in file.readlines()]
        assert all(len(_truth_tables[i]) == len(_truth_tables[i + 1]) for i in range(len(_truth_tables) - 1))
        truth_tables = _truth_tables
        duplicates = []
        for (tt1_id, tt1), (tt2_id, tt2) in combinations(enumerate(truth_tables), 2):
            if tt1 == tt2:
                duplicates.append((tt1_id, tt2_id))
            elif tt1 == ''.join(str(1 - int(c)) for c in tt2):
                duplicates.append((tt1_id, -tt2_id))
        if duplicates:
            print(f'  There are duplicates among the outputs: {duplicates}')

        from itertools import product
        from math import log2, sqrt
        sz = int(log2(len(truth_tables[0])))
        maxim = [[0 for i in range(1 << (sz // 2))] for j in range(1 << (sz // 2))]
        single_var = [0 for i in range(1<<sz)]
        for id_table, table in enumerate(truth_tables):
            sz = int(log2(len(table)))
            values = {x[::-1]: table[i] for i, x in enumerate(product((1, 0), repeat=sz))}
            this_bit = [[0 for i in range(1 << (sz // 2))] for j in range(1 << (sz // 2))]
            for v in product((0, 1), repeat=sz):
                mask = int(''.join(map(str, v[:])), 2)
                #print(mask)
                val = 0
                if values[v[::-1]] == '1':
                    val = 1
                num1 = int(''.join(map(str, v[:sz // 2])), 2)
                num2 = int(''.join(map(str, v[sz // 2:])), 2)
                this_bit[num1][num2] = val
                maxim[num1][num2] += (1<<id_table) * val
                single_var[mask] += (1<<id_table) * val
        return single_var

def line(x1, y1, x2, y2):
    return [Fraction((y2-y1),(x2-x1)), y1 - x1 * Fraction((y2-y1),(x2-x1))]
def linearizator(a):
    n = len(a)
    lans = 0
    rans = 1024*8
    pairs = []
    while rans - lans > 1:
        check = (lans+rans)//2
        print(check)
        pairs.clear()
        now = 0
        prev = 0
        success = 1
        while now < n:
            l = now+gap
            r = n
            while r-l > 1:
                c = (r+l)//2
                print(f"now={c}")
                lin = line(prev, a[prev], c, a[c])
                ok = True
                for i in range(prev, c+1):
                    if (abs(a[i] - (lin[0] * i + lin[1])) > check):
                        ok = False
                if ok == False:
                    r = c
                else:
                    l = c
            now = l
            if now - prev == gap:
                lans = check
                success = 0
                break
            pairs.append([prev,now])
            print(f"adding pair{[prev, now]}")
            prev = now+1
            now += 1
            if len(pairs) > linesmax:
                success = 0
                lans = check
                break
        if success == 1:
            rans = check

    check = rans
    pairs.clear()
    now = 0
    prev = 0
    while now < n:
        l = now + gap
        r = n
        while r - l > 1:
            c = (r+l)//2
            print(f"now = {c}")
            lin = line(prev, a[prev], c, a[c])
            ok = True
            for i in range(prev, c + 1):
                if (abs(a[i] - (lin[0] * i + lin[1])) > check):
                    ok = False
            if ok == False:
                r = c
            else:
                l = c
        now = l
        pairs.append([prev,now])
        print(f"adding pair{[prev, now]}")
        prev = now + 1
        now += 1
    print(rans)
    print(pairs)
    with open(f'{path.split('/')[-1]}-linear.txt', 'w', encoding='utf-8') as file:
        file.write(f'{str(rans)}\n')
        file.write(f'{str(pairs)}\n')
    print("recorded")

if __name__ == '__main__':

    arr = [180, 181, 182, 183, 184, 185, 188, 189, 190, 191, 192, 193, 194, 195, 198, 199]
    for x in arr:
        path = f"C:/Users/Maxim/PycharmProjects/circuit-synthesis/iwls2025/truth_tables/ex{x}.truth"
        a = array(path)
        linearizator(a)
