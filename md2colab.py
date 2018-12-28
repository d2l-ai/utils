import sys
import re
import os
import nbformat
from md2ipynb import reader, add_space_between_ascii_and_non_ascii

def get_svg_size(filename):
    """return width and height of a svg"""
    with open(filename) as f:
        lines = f.read().split('\n')
    width, height = None, None
    for l in lines:
        res = re.findall('<svg.*width="(\d+)pt".*height="(\d+)pt"', l)
        if len(res) > 0:
            # wired 1.25, maybe due to omni-graffle
            width = round(1.25*float(res[0][0]))
            height = round(1.25*float(res[0][1]))
        res = re.findall('width="([.\d]+)', l)
        if len(res) > 0:
            width = round(float(res[0]))
        res = re.findall('height="([.\d]+)', l)
        if len(res) > 0:
            height = round(float(res[0]))
        if width is not None and height is not None:
            return width, height
    assert False, 'cannot find height and width for ' + filename

def parse_image(line):
    """parse ![cap](img.png)"""
    # TODO(mli) wrong results if more than one image in a line
    res = re.findall('!\[(.*)\]\((.*)\)', line)
    assert len(res) <= 1
    if len(res) == 0:
        print(line)
        return None, None
    else:
        return res[0]

def get_github_url(fname, repo):
    return 'https://raw.githubusercontent.com/%s/master/%s' % (repo, fname)

def replace_image(source, input_dir, github_repo):
    if not '![' in source:
        return source
    lines = source.split('\n')
    for i, l in enumerate(lines):
        if not '![' in l or '\![' in l:
            continue
        cap, img = parse_image(l)
        # a strong assumption to get img filename relative the root by removing
        # tail ../
        img_url = get_github_url(img.replace('../', ''), github_repo)
        if img.endswith('.svg'):
            w, h = get_svg_size(input_dir + '/' + img)
            new_l = '<img src="%s" alt="%s" width=%d height=%d/>' % (
                img_url.replace('.svg', '.png'), cap, int(1.5*w), int(1.5*h))
        else:
            new_l = '![%s](%s)' % (cap, img_url)
        lines[i] = new_l
    return '\n'.join(lines)


if __name__ == '__main__':

    assert len(sys.argv) == 5, 'usage: input.md output.ipynb github_repo discuss_url'

    input_fn = sys.argv[1]
    input_dir = os.path.dirname(input_fn)
    output_fn = sys.argv[2]
    github_repo = sys.argv[3]
    discuss_url = sys.argv[4]

    with open(input_fn, 'r') as f:
        notebook = reader.read(f)

    for c in notebook.cells:
        if c.cell_type == 'markdown':
            c.source = add_space_between_ascii_and_non_ascii(c.source)
            c.source = replace_image(c.source, input_dir, github_repo)

    # add install mxnet at the beginning
    for c in notebook.cells:
        if c.cell_type =='code' and 'import' in c.source and 'mxnet' in c.source:
            install = '# Install dependencies before importing\n!pip install mxnet-cu92\n!pip install gluonbook\n\n'
            c.source = install + c.source
            break

    # replace the discuss link at the bottom
    for c in reversed(notebook.cells):
        if '<div id="discuss"' in c.source:
            lines = c.source.split('\n')
            for i, l in enumerate(lines):
                res = re.findall('topic_id="(\d+)"', l)
                if len(res) == 1:
                    new_l = '[Link to the discuss thread.](https://%s/t/%d).' % (discuss_url, int(res[0]))
                    lines[i] = new_l
            c.source = '\n'.join(lines)
            break

    # need to add language info to for syntax highlight in HTML
    notebook['metadata'].update({'language_info':{'name':'python'}})

    # ask colab to GPU instance TODO(mli) make it optional
    notebook['metadata'].update({'accelerator':'GPU'})

    with open(output_fn, 'w') as f:
        f.write(nbformat.writes(notebook))
