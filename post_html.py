import bs4
import os
import shutil
import subprocess
import tempfile

HTML_DIR = 'build/_build/html'
UTIL_DIR = 'build/utils'

# Replace with space for all htmls
p = subprocess.Popen(['bash ' + UTIL_DIR  + '/post_html_utils.sh replace_with_space ' + HTML_DIR],
                     shell=True, executable='/bin/bash')
p.wait()

# Edit index.html
source_file = HTML_DIR + '/index.html'
soup = bs4.BeautifulSoup(open(source_file), 'html.parser')
lang = soup.find('html')['lang']

# Replace title in index.html
if lang == 'en':
    title = 'Dive into Deep Learning: An Interactive Book with Math, Code, and Discussions'
elif lang == 'zh_CN':
    title = '《动手学深度学习》：面向中文读者、能运行、可讨论'
soup.find('title').string = title

# Hide subsection titles of Chapter 1 in index.html
for div in soup.find_all('div', {'class': 'toctree-wrapper compound'}):
    a = div.find('a', {'class': 'reference internal', 'href': 'chapter_introduction/deep-learning-intro.html'})
    if a:
        a.find_next().decompose()

# Write to index.html
_, target_file = tempfile.mkstemp()
with open(target_file, 'w') as target_f:
    target_f.write(str(soup))

os.remove(source_file)
shutil.move(target_file, source_file)

