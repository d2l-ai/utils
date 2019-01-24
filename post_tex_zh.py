from os import remove
import re
from shutil import move
from tempfile import mkstemp


def unnumber_sections(source_file):
    _, target_file = mkstemp()
    preface_reached = False
    ch2_reached = False
    # Preface and Using this Book are numbered chapters
    NUM_UNNUMBERED_CHAPS = 2
    # Prerequisites
    TOC2_START_CHAP_NO = 4

    UNNUMBERED = {'\\section{小结}',
                  '\\section{参考文献}',
                  '\\section{练习}',
                  '\\section{扫码直达讨论区}',
                  '\\subsection{小结}',
                  '\\subsection{参考文献}',
                  '\\subsection{练习}',
                  '\\subsection{扫码直达讨论区}'}

    num_chaps = 0
    with open(target_file, 'w') as target_f, open(source_file, 'r') as source_f:
        for l in source_f:
            if l.startswith('\\chapter{'):
                num_chaps += 1
                # Unnumber unnumbered chapters
                if num_chaps <= NUM_UNNUMBERED_CHAPS:
                    chap_name = re.split('{|}', l)[1]
                    out_line = '\\chapter*{' + chap_name + '}\\addcontentsline{toc}{chapter}{' + chap_name + '}\n'
                    target_f.write(out_line)
                # Set tocdepth to 2 after Chap 1
                elif num_chaps == TOC2_START_CHAP_NO:
                    target_f.write('\\addtocontents{toc}{\\protect\\setcounter{tocdepth}{2}}\n')
                    target_f.write(l)
                else:
                    target_f.write(l)
            # Unnumber all sections in unnumbered chapters
            elif 1 <= num_chaps <= NUM_UNNUMBERED_CHAPS:
                if l.startswith('\\section'):
                    target_f.write(l.replace('\\section', '\\section*'))
                elif l.startswith('\\subsection'):
                    target_f.write(l.replace('\\subsection', '\\subsection*'))
                elif l.startswith('\\subsubsection'):
                    target_f.write(l.replace('\\subsubsection', '\\subsubsection*'))
                else:
                    target_f.write(l)
            # Unnumber summary, references, problems, qr code in numbered chapters
            elif l.rstrip() in UNNUMBERED:
                target_f.write(l.replace('section{', 'section*{'))
            else:
                target_f.write(l)

    remove(source_file)
    move(target_file, source_file)


tex_file = 'build/_build/latex/d2l-zh.tex'
unnumber_sections(tex_file)
