#!/usr/bin/env python3

import sys
import os

def _is_null(line): return not line

def _is_comment(line): return line[0] == '"'

def _quote2tex(lines):
    ret, state = '', 0
    for line in lines:
        line = line.strip()
        if _is_null(line) or _is_comment(line):
            continue
        elif state == 0:
            ret += '\\myquotepage{Sienna}{%s}\n' % (line)
            state = 1
        elif state == 1:
            ret += '{%s}\n\n\\newpage' % (line)
    return ret

def _verse2tex(lines):
    ret, state = '', 0

    ret += '\\phantom{anything}\n'
    if len(lines) < 12:
        ret += '\\vspace{2cm}\n'

    for line in lines:
        line = line.strip()
        if len(line) == 0:
            ret += '\n'
            if state == 2:  # blank line in verse content
                ret += '\\vspace{-0.4cm}\n'
            continue

        if state == 0:
            ret += '\\section{%s}\n' % (line)
            state = 1 # Author
        elif state == 1:
            ret += '%s\\\\\n' % (line)
            state = 2 # verse content
        else:
            ret += '%s\\\\\n' % (line)
    ret += '\n\\newpage\n'

    return ret

def to_tex(txt_file):
    suffix = os.path.splitext(txt_file)[-1]

    tex_file = txt_file.replace(suffix, '.tex')

    with open(txt_file, 'r') as txt_f:  lines = txt_f.readlines()

    if suffix == '.quote':
        ret = _quote2tex(lines)
    elif suffix == '.verse':
        ret = _verse2tex(lines)
    else:
        ret = 'not implemented warnning!'

    with open(tex_file, 'w') as tex_f:
        tex_f.write(ret)