# NINA Python template
A template to fast setup python projects

## Requirements
- uv
- git

## How to use it
Make sure that `uv` is installed, then run:

```bash
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
Install development dependencies:
- **pinact**: `./scripts/install-pinact.sh`

## Testing the template
To test the template using copier-template-tester, run:
```bash
uvx pre-commit run -c .pre-commit-config-extra.yaml
```

## Maintenance
To update dependencies and tools:
```bash
./scripts/maintenance.sh
```

## How to version
To create a new release:
```bash
./scripts/release.sh <patch|minor|major>
```

Example:
```bash
./scripts/release.sh minor
```
