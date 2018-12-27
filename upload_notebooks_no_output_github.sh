#!/bin/bash
# convert all .md files into .ipynb files without evaluation. Then upload them
# into a github repo
set -e
set -x

if [ $# -ne 2 ]; then
    echo "ERROR: needs three arguments. "
    echo "Usage:"
    echo "   $0 input_dir output_dir github_repo"
    exit -1
fi

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
IN_DIR="$( cd $1 >/dev/null 2>&1 && pwd )"
OUT_DIR=${IN_DIR}_notebooks
# OUT_DIR="$( cd $2 >/dev/null 2>&1 && pwd )"
GITHUB=$2

rm -rf ${OUT_DIR}
git clone ${GITHUB} ${OUT_DIR}
rm -rf ${OUT_DIR}/*

${SCRIPT_DIR}/notebooks_no_output.sh ${IN_DIR} ${OUT_DIR}
cd ${OUT_DIR}
git commit -am "Upload notebooks"
git push
