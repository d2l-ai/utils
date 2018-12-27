#!/bin/bash
# convert all .md files into .ipynb files without evaluation.
set -e

if [ $# -ne 2 ]; then
    echo "ERROR: needs two arguments. "
    echo "Usage:"
    echo "   $0 input_dir output_dir"
    echo "see upload_notebooks_no_output_github.sh for an example"
    exit -1
fi

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
IN_DIR="$( cd $1 >/dev/null 2>&1 && pwd )"
OUT_DIR="$( cd $2 >/dev/null 2>&1 && pwd )"

make -C ${SCRIPT_DIR} -f notebooks_no_output.mk IN_DIR=${IN_DIR} OUT_DIR=${OUT_DIR}
