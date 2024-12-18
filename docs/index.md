---
layout: default
---

Welcome to the **devcli** documentation site! Since this tool aims to simplify
the development process, we need to ensure it's easy to use and understand.

## Installation

Installation can be done using Python tools [`poetry`](https://python-poetry.org/docs/#installation)
and [`pipx`](https://pypi.org/project/pipx/). If you don't have them installed, you can use [`homebrew`](https://brew.sh/) to install them.

```bash
$ brew install poetry
$ brew install pipx
```

Once you have them installed, you can install `devcli` by cloning the repository and running the following commands, like so:

```bash
$ git clone https://github.com/mvaltas/devcli.git
$ cd devcli
$ poetry build --format=wheel
$ pipx install --force dist/devcli*.whl
```



