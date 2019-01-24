import subprocess

HTML_DIR = 'build/_build/html'
UTIL_DIR = 'build/utils'

# Replace with space for all htmls
p = subprocess.Popen(['bash ' + UTIL_DIR  + '/post_html_utils.sh replace_with_space ' + HTML_DIR],
                     shell=True, executable='/bin/bash')
p.wait()

