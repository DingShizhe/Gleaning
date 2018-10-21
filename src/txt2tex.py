#!/usr/bin/env python3

import re
import os


class ToTex(object):
    """
    ToTex Class Defination.

    """
    def __init__(self):
        """Constructor for ToTex"""
        self.src_path = ''
        self.title = ''
        self.title_line = ''
        self.author = ''
        self.author_line = ''
        self.times = ''
        self.content = ''
        self.state = 0

    def clear_obj(self):
        """Clear up"""
        self.title = ''
        self.title_line = ''
        self.author = ''
        self.author_line = ''
        self.times = ''
        self.content = ''
        self.state = 0

    def load_text(self, text_file):
        """Load and process source text file whose type can be '.quote' or '.verse'"""
        self.clear_obj()
        assert os.path.exists(text_file)
        self.src_path = text_file
        with open(text_file, 'r') as f:
            lines = f.readlines()

        if text_file.endswith('.quote'):
            self._parse_simple(lines)
        elif text_file.endswith('.verse'):
            self._parse_lines(lines)
            self._post_process()
        else:
            print('Warning: File %s\'s type is not implemented.' % text_file)

    def dump_tex(self):
        """Dump to .tex file to where the source stays"""
        suffix = os.path.splitext(self.src_path)[-1]
        tex_file = self.src_path.replace(suffix, '.tex')
        with open(tex_file, 'w') as f:
            f.write(self.content)

    def _parse_simple(self, lines):
        """Process .quote file, it's simple"""
        content, state = '', 0
        for line in lines:
            line = line.strip()
            if self._is_null(line) or self._is_comment(line):
                continue

            if state == 0:
                content += '\\myquotepage{Sienna}{%s}\n' % line
                state = 'FROM_S'
            elif state == 'FROM_S':
                content += '{%s}\n\n\\newpage' % line

        self.content = content

    def _parse_lines(self, lines):
        """parse .verse file"""
        for line in lines:
            line = line.strip()
            pure_line = re.sub(r'\{[^)]*\}', '', line)

            if self._is_null(line):
                self.content += '\n'
                if self.state == 2: self.content += '\n'
                continue
            elif self._is_comment(line):
                continue

            if self.state == 0:
                self.title = pure_line
                self.title_line = line
                self.state = 1

            elif self.state == 1:
                # if self.src_path.endswith('李白-春思.verse'):
                    # pure_line = re.sub(r'\{[^)]*\}', '', pure_line)
                    # print(pure_line)
                    # input()
                if '~' in line:
                    self.author, self.times = pure_line.split('~')
                else:
                    self.author, self.times = pure_line, ''
                self.author_line = line
                self.state = 2

            elif self.state == 2:
                self.content += line + '\n'

    def _post_process(self):
        """'.verse' file after parse need to converted to .tex"""
        self.content = self.content.replace('{', '\\footnote{')
        self.title_line = self.title_line.replace('{', '\\footnote{')
        self.author_line = self.author_line.replace('{', '\\footnote{')

        self.content = self.content.replace('\n', '\\\\\n')
        self.content = self.content.replace('\n\\\\\n\\\\\n', '\n\n\\vspace{-0.4cm}\n')

        content = '\\phantom{anything}\n\n'
        content += '\\section[{\\color{by}\\HuaWenKaiTi{%s}}~~%s]{%s}\n\n' %\
                   (self.author, self.title, self.title_line)
        content += '%s' % (self.author_line)

        self.content = content + self.content + '\n\\newpage'
        # print(self.content)

    @staticmethod
    def _is_null(line):
        """as you seen below"""
        return len(line) == 0

    @staticmethod
    def _is_comment(line):
        """as you seen below, '"' is the fst char of comment line"""
        return line.startswith('"')


''' for test
v = ToTex()
v.load_text('./句/1-年轻的时候，我想成为任何人，除了我自己。.quote')
print(v.content)
v.clear_obj()
v.load_text('./诗/余光中-飞将军.verse')
print(v.content)
'''