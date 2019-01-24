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

# Replace title in index.html
soup.find('title').string = 'Dive into Deep Learning &#8212; An Interactive Book with Math, Code, and Discussions'

# Hide  subsection titles of Chapter 1 in index.html
soup.find('a', {'class': 'reference internal',
				'href': 'chapter_introduction/deep-learning-intro.html'}).find_next().decompose()

# Write to index.html
_, target_file = tempfile.mkstemp()
with open(target_file, 'w') as target_f:
	target_f.write(str(soup))

os.remove(source_file)
shutil.move(target_file, source_file)

