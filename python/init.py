#!/usr/bin/env python3
import logging
import pathlib
import subprocess
import sys
from argparse import ArgumentParser
from tempfile import TemporaryDirectory


def run_hooks(output):
    from yaml import safe_load

    repository = get_repo()

    with pathlib.Path(".pre-commit-config.yaml").open(mode="r") as pre_commit_conf_file:
        pre_commit_conf = safe_load(pre_commit_conf_file.read())
        hooks = []
        for repo in pre_commit_conf["repos"]:
            for hook in repo["hooks"]:
                hooks.append(hook["id"])

        logging.debug(hooks)

        for hook in hooks:
            subprocess.run(
                ["pre-commit", "run", hook, "-a"],
                stdout=output,
            )
            repository.git.add(".")


def install_precommit(output):
    logging.debug("Install precommit")
    subprocess.check_call(
        ["pre-commit", "install"], stdout=output, stderr=subprocess.STDOUT
    )
    subprocess.check_call(
        ["pre-commit", "autoupdate"],
        stdout=output,
    )


def get_repo(initial_branch=None):
    from git import Repo

    if initial_branch:
        logging.debug("Initializing a new git repository")
        Repo.init(initial_branch=initial_branch)
    return Repo(pathlib.Path.cwd())


def setup(initial_branch, output):
    updating = False
    git_initialized = False
    pre_commit_installed = False

    with TemporaryDirectory() as tmp_dir:
        if pathlib.Path.cwd().is_relative_to(pathlib.Path(tmp_dir).parent):
            updating = True

    git_initialized = pathlib.Path(".git").exists()
    if git_initialized:
        pre_commit_installed = pathlib.Path(".git/hooks/pre-commit").exists()

    logging.debug(
        {
            "updating": updating,
            "git_initialized": git_initialized,
            "pre_commit_installed": pre_commit_installed,
            "path": pathlib.Path.cwd(),
        }
    )

    # if updating:
    #     if not pre_commit_installed:
    #         install_precommit()

    #     subprocess.check_call(["pre-commit", "autoupdate"])
    #     run_hooks()
    #     return

    if git_initialized:
        repo = get_repo()
        repo.git.add(".")
        subprocess.run(
            ["pre-commit", "run", "-a"],
            stdout=output,
        )
    else:
        logging.debug("initializing git")
        repo = get_repo(initial_branch=initial_branch)
        install_precommit(output=output)
        repo.git.add(".")
        run_hooks(output=output)
        logging.debug("making commit")
        repo.git.commit(m="Initial commit")


def install_dependencies(output):
    logging.debug("initializing dependencies")
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", "-e", ".[tools]"],
        stdout=output,
    )


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "initial_branch", metavar="initial_branch", type=str, help="initial branch name"
    )
    parser.add_argument(
        "template_type", metavar="template_type", type=str, help="template_type"
    )
    parser.add_argument("-d", "--debug", action="store_true")
    args = parser.parse_args()
    logging.basicConfig(
        format="%(levelname)s:%(message)s",
        level=logging.DEBUG if args.debug else logging.INFO,
    )
    output = None if args.debug else subprocess.DEVNULL
    install_dependencies(output=output)
    setup(initial_branch=args.initial_branch, output=output)
