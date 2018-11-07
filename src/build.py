#!/usr/bin/env python3

import os, sys
import txt2tex

flag = False
if len(sys.argv) > 1 and sys.argv[1] == 's':
    flag = True

if flag:
    with open('./titlepg.tex', 'r') as f:
        import opencc
        text = opencc.convert(f.read(), config='t2s.json')
    with open('./titlepg.tex', 'w') as f:
        f.write(text)

for item in os.listdir('.'):
    if os.path.isdir(item) and not item.startswith('__'):
        # print(item)
        v = txt2tex.ToTex(jianti=flag)
        for txt_file in os.listdir(item):
            # print(txt_file)
            v.load_text('%s/%s' % (item, txt_file))
            # v.dump_cooked()
            v.dump_raw()
            v.load_text('%s/%s' % (item, txt_file))
            v.dump_tex()
