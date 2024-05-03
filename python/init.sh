#!/bin/bash

# exit on error
set -o errexit
# exit on error inside pipe
set -o pipefail
# print executed commands along with their result (useful for debugging)
# set -x

# This script will setup a git repository if not present
# And will fix formatting errors that are produced by Jinja template inheritance

run_hooks() {
    # find all the hooks installed, excluding the commented ones
    hooks=$(cat .pre-commit-config.yaml | grep id: | awk '$1 ~ /^[^;#]/' | awk '{print $3}')
    while read hook; do
        # execute each hook one by one
        # NOTE: this is necessary because pre-commit will not execute all
        #       the hooks if there's an error
        pre-commit run $hook -a || true;
        git add .;
    done <<< "$hooks"
}

if [ -d .git/ ]; then
  echo "This project is already initialized. Running hooks"
  git add .;
  run_hooks;
  exit 0
fi

if [[ $PWD == /tmp* ]]; then
    echo "This is copier update. Running hooks"
else
    echo "New repository, set up git and run hooks"
fi

git init . -b $1;
pre-commit install;
git add .;
run_hooks;
git commit -m "Initial commit";
