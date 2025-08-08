# NINA Python template
🚀 Skip the boring setup and jump straight into coding! This template gives you everything you need for a modern Python project - from code formatting to CI/CD - all configured and ready to go.

## Requirements
- [uv](https://github.com/astral-sh/uv) - An extremely fast Python package installer and resolver
- [git](https://git-scm.com/) - Version control system

## How to use it

### Creating a new project
Make sure that `uv` is installed, then run (replace `your-project-name` with your desired project name):

```bash
uvx --with copier_template_extensions copier copy --trust gh:ninanor/python-template your-project-name
```

Answer the questions and you are done.

### Applying to an existing project
To apply this template to an existing project directory:

```bash
cd your-existing-project
uvx --with copier_template_extensions copier copy --trust gh:ninanor/python-template .
```

This will add the template files to your current directory. Be careful as this may overwrite existing files.


## Features
Why should I use this template:

- **Auto formatting and code checking** using `ruff`
- **Updatable template** - Easy to keep up to date with latest practices
- **Visual Studio Code** configurations included
- **Pre-commit hooks** for code quality enforcement
- **GitHub Actions** workflows for CI/CD

### Optional features
When creating a project, you can choose from these additional features:
- **Docker** - Add standard files for dockerizing a Python project
- **Type annotations** - Make type annotations mandatory throughout the project
- **Notebook support** - Include Jupyter or Marimo notebook support

## I want the simplest of the templates
Press `Enter` to all questions, you'll get a simple Python project to start with.

**Keep in mind** that you can always change your answers, it's fine if you want to start with something simple and then for example you need Docker. Update the template, change your answers in the survey and you will get the code for that!

## How to update
Basically you just need to run:
```
uvx copier update --trust
```

You can now change your questions, in case you want to keep your previous answers use: `uvx copier update --trust --defaults`.

This will try to check differences between your project and the template, if no conflicts are found you are done.
Check this [page](https://copier.readthedocs.io/en/stable/updating/) for more specific info about this feature.

## Running pre-commit

[pre-commit](https://github.com/pre-commit/pre-commit) is a framework for managing pre-commit git hooks. The pre-commit git hooks are ways to identify issues in your code before pushing your changes to the repository, for instance missing semicolons, trailing whitespace, unused dependencies.

:sparkles: pre-commit doesn't change the functionality of your code

To run pre-commit on your code, first install dependencies:

```
uv sync --dev
```

Then run:

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
