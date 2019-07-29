# Guidelines for Contributors

## Commit Messages

Take your time to write brief, yet descriptive commit messages, especially their titles (the first line of a commit message). You can write a more detailed description of the commit on the further lines, but the commit title matters the most and therefore should be sufficiently descriptive.

## Pull Requests and Code Reviews

Every pull request into the `master` branch of the upstream fork should be reviewed and approved by at least one other contributor, regardless of how insignificant or safe the change might seem.

## Creating Issues

It may be difficult, depending on the number of currently open issues, but please check existing issues before creating a new one to avoid duplicates.

The title of an issue should properly describe it, so that its description only contains a context and additional details.

Always consider creating an issue before you start working on any changes or a new feature. That way you significantly lower the odds of multiple contributors working on the same thing without knowing and potentially save yourself and other people time and effort.

When you notice a bug that has not been reported before, always create an issue for it. Such issue should contain as much available context as possible. Useful context includes the steps to reproduce the bug and information about your environment (operating system version and the results of `python --version` and `pip freeze`). If you are running the application inside of a virtual environment, make sure to run the commands inside of it as well.

## Closing Issues

Once you decide that you want to work on an issue, assign yourself to the issue, so that other people can easily tell it is already being worked on.

Where applicable, close issues by adding `Close #N` to a commit message or the description of a related pull request.

To avoid any confusion, it is best to prefix the `#N` part with the username of the upstream fork's owner (e.g., `Close username#123`), otherwise you may accidentally end up referencing an issue or a pull request from a different fork.

## Libraries and Dependencies

When possible, avoid adding new dependencies, especially if they are difficult to install.

Ideally, all dependencies should be cross-platform and available for installation via `pip`.

## Ignored Files

### Configuration Files and Temporary Files

No local configuration files or temporary files should be tracked in the repository. This includes all IDE configuration files, pre-compiled Python bytecode files (`.pyc` files in `__pycache__` directories) and all output files produced by the application.

### Clones repositories

Cloned repositories should also never be included in commits, except for repositories specifically designated for use by the testing suite. Such repositories must be located within the `test/` directory as Git submodules.

### `.editorconfig`

There is currently only a single exception to this rule: `.editorconfig` - a configuration file supported by a vast majority of popular text editors and IDEs. This file helps with establishing some ground rules for all text files in the repository.

### `.gitignore`

Commonly occurring undesirable files can be included in `.gitignore` to avoid accidentally committing them. However, `.gitignore` should only be modified in serious cases; otherwise it will end up flooded with too many rules, which may eventually end up causing more trouble.
