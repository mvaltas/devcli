---
layout: default
---

Welcome to the **devcli** documentation site! This tool aims to simplify the
development process, so we want to make sure it's easy to use and understand.

## Installation

Installation can be done using Python tools [`uv`](https://docs.astral.sh/uv/)
and [`pipx`](https://pypi.org/project/pipx/). If you don't have them installed,
you can use [`homebrew`](https://brew.sh/) to install them. You also can use
[`just`](https://github.com/casey/just) for some helpful shortcuts in development.


```bash
$ brew install uv
$ brew install pipx
$ brew install just # optional
```

Once you have them installed, you can install `devcli` locally by cloning the
repository and running the following commands, like so:

```bash
$ git clone https://github.com/mvaltas/devcli.git
$ cd devcli
$ uv build --wheel
$ pipx install --force dist/devcli*.whl
```

When installing with `pipx` the default target will be:

```bash
${HOME}/.local/pipx/venvs/devcli/bin/devcli
```

You can add this directory to your path, like so:
```bash
$ export PATH=${PATH}:${HOME}/.local/pipx/venvs/devcli/bin
```

You can refresh your command hash by:
```bash
$ hash -r
```


## Usage

This tool is designed with the principle of *discoverability*, which means you
can explore it by running it without any arguments. This way, you'll be able to
see the available commands and learn more about them:

```
$ devcli

Usage: devcli [OPTIONS] COMMAND [ARGS]...

╭─ Options ────────────────────────────────────────────────────────────╮
│ --debug            Enable debug log                                  │
│ --verbose          Enable info log                                   │
│ --help             Show this message and exit.                       │
╰──────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────╮
│ example          Examples on how create cli commands with *devcli*   │
╰──────────────────────────────────────────────────────────────────────╯
```

## Extending

*devcli* will scan for directories named `.devcli`, where it will expect two
things: other commands to load and a configuration file named `devcli.toml`
(which can be empty). You can check the
[`example`](https://github.com/mvaltas/devcli/blob/main/.devcli/example.py) for
some ways to extend it. For the simplest case, you can create a file named
`hello.py` in your `.devcli` directory, like this:

```python
import devcli.framework as cmd

cli = cmd.new("This is a hello world command")

@cli.command()
def say():
    """Simply replies with a Hello, World!"""
    print("Hello, World!")

```

Once you did that, running *devcli* again you see a new command available called `hello`:

```
$ devcli

    Usage: devcli [OPTIONS] COMMAND [ARGS]...

╭─ Options ────────────────────────────────────────────────────────────╮
│ --debug            Enable debug log                                  │
│ --verbose          Enable info log                                   │
│ --help             Show this message and exit.                       │
╰──────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────╮
│ example          Examples on how create cli commands with *devcli*   │
│ hello            This is a hello world command                       │
╰──────────────────────────────────────────────────────────────────────╯

```

That's it, now you can run the `--help` to inspect your new command documentation::


```
$ devcli hello --help

Usage: devcli hello [OPTIONS] COMMAND [ARGS]...

This is a hello world command

╭─ Options ───────────────────────────────────────────╮
│ --help          Show this message and exit.         │
╰─────────────────────────────────────────────────────╯
╭─ Commands ──────────────────────────────────────────╮
│ say          Simply replies with Hello, World!      │
╰─────────────────────────────────────────────────────╯
```

And if you call your new command::

```bash
$ devcli hello say
Hello, World!
```

Now you have created your first *devcli* command. To learn more about how to create commands check
the [`example`](https://github.com/mvaltas/devcli/blob/main/.devcli/example.py) command for more
advanced options.

