#!/usr/bin/env python3

import sys
import os


src_fp, des_dir = sys.argv[1:3]
src_fn = os.path.basename(src_fp).strip()
assert(len(src_fn.split('.')) >= 2)
suffix = os.path.splitext(src_fn)[-1] 
src_fnb = src_fn.rstrip(suffix)

des_fn = des_dir + '/' + src_fnb + '.tex'

with open(src_fp, 'r') as src_f:
    with open(des_fn, 'w') as des_f:
        s_lines = src_f.readlines()

        if suffix == '.verse':
            print('\\phantom{anything}', file=des_f)
            if len(s_lines) < 12:
                print('\\vspace{2cm}', file=des_f)

            state = 0 # Title
            for line in s_lines:
                line = line.strip()
                if len(line) == 0:
                    print('', file=des_f)
                    if state == 2:  # blank line in verse content
                        print('\\vspace{-0.4cm}', file=des_f)
                    continue

                if state == 0:
                    print('\\section{', line, '}', file=des_f)
                    state = 1 # Author
                elif state == 1:
                    print(line, '\\\\', file=des_f)
                    # print('\\vspace{-0.4cm}', file=des_f)
                    state = 2 # verse content
                else:
                    print(line, '\\\\', file=des_f)

            print('', file=des_f)
            print('\\newpage', file=des_f)

        elif suffix == '.quote':
            state = 0
            for line in s_lines:
                line = line.strip()
                if len(line) == 0:
                    continue
                elif line[0] == '"':    # comment
                    continue
                elif state == 0:
                    print('\\myquotepage{Sienna}{', line, '}', file=des_f)
                    state = 1
                elif state == 1:
                    print('{', line, '}\\newpage', file=des_f)