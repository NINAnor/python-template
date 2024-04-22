# NINA Python template
A template to fast setup python projects

## Requirements
- python
- pip
- pipx (optional, but recommended)
- [copier](https://github.com/copier-org/copier)

## How to use it
Make sure that `copier` is installed, then run:

```
copier copy gh:ninanor/python-template my-awesome-python-project
```

Answer the questions and you are done.


## Features
Why should I use this template:

- Auto formatting and code checking using `ruff`
- optional `Docker` image
- Updatable template
- Visual Studio configurations
- Git automatic setup


## How to update
Basically you just need to run:
```
copier update --trust
```

This will try to check differences between your project and the template, if no conflicts are found you are done.
Check this [page](https://copier.readthedocs.io/en/stable/updating/) for more specific info about this feature.
