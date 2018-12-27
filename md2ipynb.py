#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Convert .md files into .ipynb files, and optionaly evaluate each code cell.
"""
import sys
import os
import time
import notedown
import nbformat


def is_ascii(character):
    return ord(character) <= 128

def add_space_between_ascii_and_non_ascii(string):
    # no need to add space before/after a punctuate.
    punc = {' ', '\n', '\t', '\r', '，', '。', '？', '！', '、',
            '；', '：', '“', '”', '（', '）', '【', '】', '—',
            '…', '《', '》', '`', '(', ')', '[', ']', ',', '.',
            '?', '!', ';', ':', '\'', '"'}
    if len(string) == 0:
        return ''
    ret = []

    # We don't allow space within figure cpations, such as ![]().
    is_fig_caption = False
    num_left_brackets = 0
    for i in range(len(string) - 1):
        cur_char = string[i]
        next_char = string[i + 1]
        if cur_char == '[':
            if i > 0 and string[i - 1] == '!':
                is_fig_caption = True
            else:
                num_left_brackets += 1
        elif cur_char == ']':
            if num_left_brackets > 0:
                num_left_brackets -= 1
            else:
                is_fig_caption = False

        ret.append(cur_char)
        if ((is_ascii(cur_char) != is_ascii(next_char))
            and (cur_char not in punc)
            and (next_char not in punc)
            and not is_fig_caption):
            ret.append(' ')

    ret.append(string[-1])
    return ''.join(ret)

assert len(sys.argv) == 3, 'usage: input.md output.ipynb'

# timeout for each notebook, in sec
timeout = 20 * 60

# the files will be ingored for execution
ignore_execution = []

input_fn = sys.argv[1]
output_fn = sys.argv[2]

reader = notedown.MarkdownReader(match='strict')

do_eval = int(os.environ.get('EVAL', True))

# read
with open(input_fn, 'r') as f:
    notebook = reader.read(f)

for c in notebook.cells:
    c.source = add_space_between_ascii_and_non_ascii(c.source)

if do_eval and not any([i in input_fn for i in ignore_execution]):
    tic = time.time()
    notedown.run(notebook, timeout)
    print('=== Finished evaluation in %f sec'%(time.time()-tic))

# write
# need to add language info to for syntax highlight in HTML
notebook['metadata'].update({'language_info':{'name':'python'}})
# ask colab to GPU instance TODO(mli) make it optional
notebook['metadata'].update({'accelerator':'GPU'})

with open(output_fn, 'w') as f:
    f.write(nbformat.writes(notebook))
