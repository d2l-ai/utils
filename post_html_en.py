import subprocess

DIR = 'build/_build/html'

# Replace with space for all htmls
p = subprocess.Popen(['bash test.sh replace_with_space ' + DIR], shell=True, executable='/bin/bash')
p.wait()

