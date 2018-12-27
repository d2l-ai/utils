#!/bin/bash
# Upload files into a github repo.
set -ex

if [ $# -ne 2 ]; then
    echo "ERROR: needs two arguments. "
    echo "Sample usage:"
    echo "   $0 notebooks d2l-ai/notebooks"
    exit -1
fi

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
IN_DIR="$( cd $1 && pwd )"
REPO=$2
REPO_DIR=${IN_DIR}-git

# clone the repo, make sure GIT_USERNAME and GIT_PASSWORD have already set
rm -rf ${REPO_DIR}
git clone https://${GIT_USERNAME}:${GIT_PASSWORD}@github.com/${REPO}.git ${REPO_DIR}

# remove all except for README.md and .git. so we can remove deleted files properly
tmp1=$(mktemp)
tmp2=$(mktemp)
rm -f $tmp2
mv ${REPO_DIR}/README.md $tmp1
mv ${REPO_DIR}/.git $tmp2
rm -rf ${REPO_DIR}/*
mv $tmp1 ${REPO_DIR}/README.md
mv $tmp2 ${REPO_DIR}/.git

cp -r ${IN_DIR}/* ${REPO_DIR}

cd ${REPO_DIR}
git config --global push.default simple
git config --global user.name "Bot"
git config --global user.email "muli@cs.cmu.edu"
git add -f --all .
git commit -am "Upload"
git push origin master
