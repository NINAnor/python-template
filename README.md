# NINA Python template
A template to fast setup python projects

## Requirements
- python
- uv
- [copier](https://github.com/copier-org/copier)

## How to use it
Make sure that `uv` is installed, then run:

```
uvx copier copy gh:ninanor/python-template my-awesome-python-project
```

Answer the questions and you are done.


## Features
Why should I use this template:

- Auto formatting and code checking using `ruff`
- optional `Docker` image
- Updatable template
- Visual Studio configurations

## I want the simpliest of the templates
Press `Enter` to all questions, you'll get a simple python project to start with.

**Keep in mind** that you can always change your answers, it's fine if you want to start with something simple and then for example you need docker. Update the template, change your answers in the survey and you will get the code for that!

## How to update
Basically you just need to run:
```
uvx copier update
```

You can now change your questions, in case you want to keep your previous answers use: `uvx copier update --defaults`.

This will try to check differences between your project and the template, if no conflicts are found you are done.
Check this [page](https://copier.readthedocs.io/en/stable/updating/) for more specific info about this feature.


## Available profiles
- python
    - docker; add standard files for dockerizing a python project

## Running pre-commit

[pre-commit](https://github.com/pre-commit/pre-commit) is a framework for managing pre-commit git hooks. The pre-commit git hooks are ways to identify issues in your code before pushing your changes to the repository, for instance missing semicolons, trailing whitespace, unused dependancies.

:sparkles: pre-commit doesn't change the functionality of your code

To run pre-commit on your code, run:

```
uv run pre-commit run --all
```

## Struggling with a template?
Please report any issues you have using the template, even if some documentation is unclear or is missing!


# Development
Needed tools:
- bump-my-version
- copier-template-tester (ctt)
- gitchangelog

You can install them by running:
```bash
uv tool install
```

## How to version
The changelog is populated based on the git history.
use `uv run bump-my-version` to update the version of the template.
then generate the updated changelog by running `uv run gitchangelog`.

Example:
```bash
uv run bump-my-version bump minor
uv sync
git add .
git commit -m "Bump version: 0.x.0 -> 0.y.0"
git tag v0.y.0
uv run gitchangelog
git add CHANGELOG.txt
git commit --amend --no-edit
git tag -f v0.y.0
```
