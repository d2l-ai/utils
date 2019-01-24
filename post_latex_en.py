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
    # A Taste of Deep Learning
    TOC2_START_CHAP_NO = 4

    UNNUMBERED = {'\\section{Summary}',
                  '\\section{References}',
                  '\\section{Problems}',
                  '\\section{Scan the QR Code to Discuss}',
                  '\\subsection{Summary}',
                  '\\subsection{References}',
                  '\\subsection{Problems}',
                  '\\subsection{Scan the QR Code to Discuss}'}

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


tex_file = 'build/_build/latex/d2l-en.tex'
unnumber_sections(tex_file)
