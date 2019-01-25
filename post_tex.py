import os
import re
import shutil
import tempfile

TEX_FILE_EN = 'build/_build/latex/d2l-en.tex'
TEX_FILE_ZH = 'build/_build/latex/d2l-zh.tex'

UNNUMBERED_EN = {'\\section{Summary}',
                 '\\section{Reference}',
                 '\\section{References}',
                 '\\section{Problem}',
                 '\\section{Problems}',
                 '\\section{Scan the QR Code to Discuss}',
                 '\\subsection{Summary}',
                 '\\subsection{Reference}',
                 '\\subsection{References}',
                 '\\subsection{Problem}',
                 '\\subsection{Problems}',
                 '\\subsection{Scan the QR Code to Discuss}'}

UNNUMBERED_ZH = {'\\section{小结}',
                 '\\section{参考文献}',
                 '\\section{练习}',
                 '\\section{扫码直达讨论区}',
                 '\\subsection{小结}',
                 '\\subsection{参考文献}',
                 '\\subsection{练习}',
                 '\\subsection{扫码直达讨论区}'}

# Preface and Using this Book are numbered chapters
NUM_UNNUMBERED_CHAPS_EN = 2
NUM_UNNUMBERED_CHAPS_ZH = 2

# A Taste of Deep Learning
TOC2_START_CHAP_NO_EN = 4
# Prerequisites
TOC2_START_CHAP_NO_ZH = 4


class TempFile():
    def __init__(self, source_file):
        self.source_file = source_file
        _, self.target_file = tempfile.mkstemp()

    def __enter__(self):
        return self.target_file

    def __exit__(self, exc_type, exc_val, exc_tb):
        os.remove(self.source_file)
        shutil.move(self.target_file, self.source_file)


def unnumber_sections(source_file, unnumbered, num_unnumbered_chaps, toc2_start_chap_no):
    preface_reached = False
    ch2_reached = False
    num_chaps = 0
    with TempFile(source_file) as target_file:
        with open(target_file, 'w') as target_f, open(source_file, 'r') as source_f:
            for l in source_f:
                if l.startswith('\\chapter{'):
                    num_chaps += 1
                    # Unnumber unnumbered chapters
                    if num_chaps <= num_unnumbered_chaps:
                        chap_name = re.split('{|}', l)[1]
                        out_line = '\\chapter*{' + chap_name + '}\\addcontentsline{toc}{chapter}{' + chap_name + '}\n'
                        target_f.write(out_line)
                    # Set tocdepth to 2 after Chap 1
                    elif num_chaps == toc2_start_chap_no:
                        target_f.write('\\addtocontents{toc}{\\protect\\setcounter{tocdepth}{2}}\n')
                        target_f.write(l)
                    else:
                        target_f.write(l)
                # Unnumber all sections in unnumbered chapters
                elif 1 <= num_chaps <= num_unnumbered_chaps:
                    if l.startswith('\\section'):
                        target_f.write(l.replace('\\section', '\\section*'))
                    elif l.startswith('\\subsection'):
                        target_f.write(l.replace('\\subsection', '\\subsection*'))
                    elif l.startswith('\\subsubsection'):
                        target_f.write(l.replace('\\subsubsection', '\\subsubsection*'))
                    else:
                        target_f.write(l)
                # Unnumber summary, references, problems, qr code in numbered chapters
                elif l.rstrip() in unnumbered:
                    target_f.write(l.replace('section{', 'section*{'))
                else:
                    target_f.write(l)


if __name__ == '__main__':
    assert len(sys.argv) == 2
    lang = sys.argv[1]
    assert lang in {'zh', 'en'}, 'arg1 must be zh or en'

    if lang == 'en':
        tex_file = TEX_FILE_EN
        unnumbered = UNNUMBERED_EN
        num_unnumbered_chaps = NUM_UNNUMBERED_CHAPS_EN
        toc2_start_chap_no = TOC2_START_CHAP_NO_EN
    elif lang == 'zh':
        tex_file = TEX_FILE_ZH
        unnumbered = UNNUMBERED_ZH
        num_unnumbered_chaps = NUM_UNNUMBERED_CHAPS_ZH
        toc2_start_chap_no = TOC2_START_CHAP_NO_ZH

    unnumber_sections(source_file, unnumbered, num_unnumbered_chaps, toc2_start_chap_no)

