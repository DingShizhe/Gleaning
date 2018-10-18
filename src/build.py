#!/usr/bin/env python3

import sys
import os
import txt2tex


for item in os.listdir('.'):
    if os.path.isdir(item) and not item.startswith('__'):
        # print(item)
        for txt_file in os.listdir(item):
            # print(txt_file)
            txt2tex.to_tex('%s/%s' % (item, txt_file))