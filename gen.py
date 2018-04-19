#!/usr/bin/env python3

import sys
import os

src_fp, des_dir = sys.argv[1:3]
src_fn = os.path.basename(src_fp).strip()
assert(len(src_fn.split('.')) >= 2)
src_fnb = src_fn.rstrip('.txt')
des_fn = des_dir + '/' + src_fnb + '.tex'

with open(src_fp, 'r') as src_f:
    with open(des_fn, 'w') as des_f:
        s_lines = src_f.readlines()
        print('\\phantom{anything}', file=des_f)
        if len(s_lines) < 12:
            print('\\vspace{2cm}', file=des_f)

        state = 0 # Title
        for line in s_lines:
            line = line.strip()
            if len(line) == 0:
                print('', file=des_f)
                continue

            if state == 0:
                print('\\section{', line, '}', file=des_f)
                state = 1 # Author
            elif state == 1:
                print(line, '\\\\', file=des_f)
                print('\\vspace{-0.4cm}', file=des_f)
                state = 2
            else:
                print(line, '\\\\', file=des_f)

        print('', file=des_f)
        print('\\newpage', file=des_f)