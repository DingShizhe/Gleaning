#!/usr/bin/env python3

import re
import os


class ToTex(object):
    """
    ToTex 定义。可以用这个类的方法，将两种格式的作品文件
    （Raw或Cooked）翻译为TeX文件。

     +----------> Cooked
     |     ToTex     |
    Raw <------------+
             |
            TeX
    """
    def __init__(self, jianti=False):
        """Constructor for ToTex"""
        self.jianti = jianti
        self.src_path = ''

        self.raw_parts = []
        self.footnotes = []
        self.note_idx = 0

    def load_text(self, text_file):
        """Load and process source text file whose 
        type can be '.quote' or '.verse'"""
        self._clear_obj()
        assert os.path.exists(text_file), text_file
        assert text_file.endswith('quote') or text_file.endswith('verse')
        self.src_path = text_file
        with open(text_file, 'r') as f:
            text = f.read()

        if self.jianti:
            import opencc
            text = opencc.convert(text, config='t2s.json')

        if '--------' in text:
            self._parse_cooked(text)
        else:
            self._parse(text)

    def dump_tex(self):
        """Dump to .tex file to where the source stays"""
        if self.src_path.endswith('verse'):
            content = self._post_process_v()
        elif self.src_path.endswith('quote'):
            content = self._post_process_q()

        suffix = os.path.splitext(self.src_path)[-1]
        tex_file = self.src_path.replace(suffix, '.tex')

        with open(tex_file, 'w') as f:
            f.write(content)

    def dump_raw(self, str_flag=True):
        parts = [x.strip() for x in self.raw_parts]
        text = '\n\n'.join(parts)
        text += '\n' if not text.endswith('\n') else ''
        if not str_flag:
            with open(self.src_path, 'w') as f: f.write(text)
        else:
            return text

    def dump_cooked(self):
        def repl(x):
            self.note_idx += 1
            return '[%s]' % str(self.note_idx)
        text = self.dump_raw()
        text = re.sub('\{(.*?)\}', repl, text)

        text += '\n\n--------\n'
        text += '\n'.join(['[%s] '%str(i+1)+x for i,x in enumerate(self.footnotes)])
        text += '\n' if not text.endswith('\n') else ''
        with open(self.src_path, 'w') as f: f.write(text)        

    def _parse(self, text):
        """分析verse作品文件，得到作品信息"""
        text = re.sub('".*\n', '', text)    # 去掉"
        text = re.sub(' *\n', '\n', text)   # 去掉行尾空格
        raw_parts = text.split('\n\n')
        raw_parts = [x.strip() for x in raw_parts if x.strip()] # 留下有效的

        self.raw_parts = raw_parts
        self.footnotes = re.findall(r'\{(.*?)\}', '\n'.join(raw_parts))

    def _parse_cooked(self, text):
        content, note_part = text.split('\n\n--------\n')
        notes_list = note_part.split('\n')
        notes_list = [x.split(' ', 1) for x in notes_list if x.strip()]
        # pprint.pprint(notes_list)
        for idx, note in notes_list:
            content = content.replace(idx, '{%s}'%note)
        # print(content)
        self._parse(content)
        pass
        
    def _post_process_v(self):
        """'.verse' file after parse need to converted to .tex"""
        raw_parts = self.raw_parts

        title = self._remove_notes(raw_parts[0])
        author_line = self._remove_notes(raw_parts[1])
        tmp = author_line.split('~')
        author, times = tmp[0], '' if len(tmp) == 1 else tmp[1]

        # 脚注
        parts = [p.replace('{', '\\footnote{') for p in raw_parts]

        # 题目 作者
        parts[0] = '\\begin{section}[{\\color{by}\\HuaWenKaiTi{%s}}~~%s]{%s}' \
            % (author, title, parts[0])
        parts[1] = '%s\\\\\n' % parts[1]
        parts[2:] = ['\\vspace{-0.45cm}%s\\\\'%p.replace('\n', '\\\\\n') for p in parts[2:]]
        parts = ['\\phantom{anything}\n'] + parts
        parts += ['\\end{section}']

        # 跋 XXX
        fst_par = 3
        if '(' in parts[3]:
            parts[3] = parts[3].replace('(', '\n\\begin{spacing}{1.2}\n\\textit{')
            parts[3] = parts[3].replace(')', '}\\\\\\\n\\end{spacing}')
            parts[3] = parts[3].rstrip('\\\\')
            parts[4].replace('vspace{-0.45cm}', 'vspace{-0.6cm}')
            fst_par = 4

        if '\n' in parts[fst_par]: parts[0] += '\\setlength{\\parindent}{0pt}\n'
        else: parts[0] += '\\setlength{\\parindent}{15pt}\n'

        content =  '\n\n'.join(parts) + '\n\\newpage'
        return content

    def _post_process_q(self):
        """Process .quote file, it's simple"""
        assert len(self.raw_parts) == 2, self.src_path
        # if len(self.raw_parts) != 2:
            # print(self.raw_parts)
        parts = [p.strip().replace('{', '\\footnote{') for p in self.raw_parts]
        content = '\\myquotepage{Sienna}{%s}\n' % parts[0]
        content += '{%s}\n\n\\newpage' % parts[1]

        return content

    def _clear_obj(self):
        self.src_path = ''
        self.raw_parts = []
        self.footnotes = []
        self.note_idx = 0

    @staticmethod
    def _is_null(line):
        """as you seen below"""
        return len(line) == 0

    @staticmethod
    def _is_comment(line):
        """as you seen below, '"' is the fst char of comment line"""
        return line.startswith('"')

    @staticmethod
    def _remove_notes(line):
        return re.sub(r'\{.*?\}', '', line)


''' For Test
v = ToTex()
# v.load_text('./句/1-年轻的时候，我想成为任何人，除了我自己。.quote')
v.load_text('./诗/张九龄-望月怀远.verse')
# v.dump_cooked()
# v.dump_tex()

test_string = """望月懷遠

張九齡[1]~【唐】

海上生明月，天涯共此時[2]。
情人怨遙夜，竟夕[3]起相思。
滅燭憐[4]光[5]滿，披衣覺露滋。
不堪盈手[6]贈，還寢夢佳期。

--------
[1] 張九齡（678-740）：唐開元尚書丞相，詩人。字子壽，一名博物，漢族，韶州曲江（今廣東韶關市）人。長安年間進士。官至中書侍郎同中書門下平章事。後罷相，爲荊州長史。詩風清淡。他忠耿盡職，秉公守則，直言敢諫，選賢任能，不徇私枉法，不趨炎附勢，敢與惡勢力作鬥爭，爲『開元之治』作出了積極貢獻。他的五言古詩，以素練質樸的語言，寄託深遠的人生慨望，對掃除唐初所沿習的六朝綺靡詩風，貢獻尤大。譽爲『嶺南第一人』。
[2] 謝莊《月賦》：『隔千里兮共明月』。
[3] 竟夕，終宵，即一整夜。
[4] 憐，愛。
[5] 光，這裏是月光。
[6] 盈手，雙手捧滿之意。陸機《擬明月何皎皎》：『照之有餘輝，攬之不盈手。』"""

v._parse_cooked(test_string)
'''