#!/usr/bin/env python3

import os
import txt2tex


for item in os.listdir('.'):
    if os.path.isdir(item) and not item.startswith('__'):
        # print(item)
        v = txt2tex.ToTex()
        for txt_file in os.listdir(item):
            # print(txt_file)
            v.load_text('%s/%s' % (item, txt_file))
            # v.dump_cooked()
            v.dump_raw()
            v.load_text('%s/%s' % (item, txt_file))
            v.dump_tex()