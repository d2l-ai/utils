#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Convert .md files into .ipynb files, and optionaly evaluate each code cell.
"""
import sys
import os
import time
import notedown
import nbformat

reader = notedown.MarkdownReader(match='strict')

if __name__ == '__main__':

    assert len(sys.argv) == 3, 'usage: input.md output.ipynb'

    # timeout for each notebook, in sec
    timeout = 20 * 60

    # the files will be ingored for execution
    ignore_execution = []

    input_fn = sys.argv[1]
    output_fn = sys.argv[2]


    do_eval = int(os.environ.get('EVAL', True))

    # read
    with open(input_fn, 'r') as f:
        notebook = reader.read(f)

    if do_eval and not any([i in input_fn for i in ignore_execution]):
        tic = time.time()
        notedown.run(notebook, timeout)
        print('=== Finished evaluation in %f sec'%(time.time()-tic))

    # write
    # need to add language info to for syntax highlight in HTML
    notebook['metadata'].update({'language_info':{'name':'python'}})

    with open(output_fn, 'w') as f:
        f.write(nbformat.writes(notebook))
