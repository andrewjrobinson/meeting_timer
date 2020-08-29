#!/bin/bash
#
# Runs unit tests (optionally selected tests files)
#

# get root directory
ROOT_DIR=$(readlink -f $(dirname $0)/..)

# run in subshell
(

cd $ROOT_DIR

if [ $# -ne 0 ]; then
    FILES=$@
else
    FILES=tests/test_*.py
fi

python3 -m unittest $FILES

) # end subshell
# pass exit code up
exit $?
