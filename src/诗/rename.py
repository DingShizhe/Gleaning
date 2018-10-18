#!/usr/bin/python3

import os

fs = os.listdir('.')

for f in fs:
    if f.endswith('verse'):
        g = f.replace('.verse', '')
        a,b = g.split('-')
        cmd = 'mv ' + f + ' '+b+'-'+a+'.verse'
        os.system(cmd)
        # print(cmd)