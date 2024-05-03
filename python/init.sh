#!/bin/bash

# exit on error
set -o errexit
# exit on error inside pipe
set -o pipefail
# prevent running the script if variables are not defined
set -o nounset

# print executed commands along with their result (useful for debugging)
# set -x

INITIAL_BRANCH=${1:?"Error. You must supply the initial branch name."}
TEMPLATE_TYPE=${2:?"Error. You must supply the template type"}

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

setup_venv() {
    if [ ! -d venv/ ]; then
        python3 -m venv venv;
        echo "setting up a virtual environment"
    else
        echo "virtual environment already present, skipping"
    fi
    source venv/bin/activate;
    pip install pre-commit;
}

command -v pre-commit >/dev/null 2>&1 || { echo "pre-commit is missing"; setup_venv; }

if [ -d .git/ ]; then
  echo "This project is already initialized. Running hooks"
  if [ ! -f .git/hooks/pre-commit ]; then
    echo "Installing hooks"
    pre-commit install;
  fi
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

if [[ $2 = "python" ]]; then
    setup_venv;
fi
