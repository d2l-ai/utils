import subprocess

DIR = 'build/_build/html'

# Replace with space for all htmls
p = subprocess.Popen(['bash post_html_utils.sh replace_with_space ' + DIR], shell=True, executable='/bin/bash')
p.wait()

