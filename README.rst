devcli - A command line tool to create command line tools
=========================================================

Why
---

There's probably no shortage of tools for developers. *devcli* came from two
necessities I had. First, I wanted to avoid memorizing complex command lines
and the order of commands for daily repetitive tasks—something like `The
General Problem <https://xkcd.com/974/>`_. During my time as a software
consultant, I had to memorize a lot of these commands for each new project. The
second necessity was a consequence of the first. Since new commands had to be
added and removed easily, I needed a way to "framework" the creation of these
commands, and that's when I decided to create *devcli*.

Installation
------------

For now the easiest way to use *devcli* is to clone this repository and
using `just <https://github.com/casey/just>`_. You can install ``just`` using
`homebrew <https://brew.sh/>`_ on macOS. I don't have the resources to support
other platforms. Dependencies are managed through `poetry <https://python-poetry.org/>`_ so you need to install
it too if you don't have it::

    $ brew install just
    $ git clone https://github.com/mvaltas/devcli.git
    $ cd devcli
    $ just install

This should be enough to install *devcli* and make it available on your path.

Usage
-----

This tool is designed with the principle of **discoverability**, which means
that to explore the tool you can run it without arguments and be able to explore
the commands available and find more about them::

    devcli

    Usage: devcli [OPTIONS] COMMAND [ARGS]...

    ╭─ Options ────────────────────────────────────────────────────────────╮
    │ --debug            Enable debug log                                  │
    │ --verbose          Enable info log                                   │
    │ --help             Show this message and exit.                       │
    ╰──────────────────────────────────────────────────────────────────────╯
    ╭─ Commands ───────────────────────────────────────────────────────────╮
    │ example          Examples on how create cli commands with *devcli*   │
    │ op               Shortcuts for 1Password CLI                         │
    ╰──────────────────────────────────────────────────────────────────────╯

Extending
---------

*devcli* will scan for directories called ``.devcli`` in these directories it will expect two things,
other commands to load and a configuration file ``devcli.toml`` (which can be empty). You can check
the `example <https://github.com/mvaltas/devcli/blob/main/.devcli/example.py>`_ for some examples
of how you can extend. For the simplest case we can create a file ``hello.py`` in your ``.devcli``
directory, like so::

    import devcli.framework as cmd
    cli = cmd.new("This is a hello world command")
    @cli.command()
    def say():
        """Simply replies with a Hello, World!"""
        print("Hello, World!")

Once you did that, running *devcli* again you see a new command available called ``hello``::

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
    │ op               Shortcuts for 1Password CLI                         │
    ╰──────────────────────────────────────────────────────────────────────╯

That's it, now you can run the ``--help`` to inspect your new command documentation::

    $ devcli hello --help

     Usage: devcli hello [OPTIONS] COMMAND [ARGS]...

     This is a hello world command

    ╭─ Options ───────────────────────────────────────────╮
    │ --help          Show this message and exit.         │
    ╰─────────────────────────────────────────────────────╯
    ╭─ Commands ──────────────────────────────────────────╮
    │ say          Simply replies with Hello, World!      │
    ╰─────────────────────────────────────────────────────╯

And if you call your new command::

    $ devcli hello say
    Hello, World!

Now you have created your first *devcli* command. To learn more about how to create commands check
the `example <https://github.com/mvaltas/devcli/blob/main/.devcli/example.py>`_ command for more
advanced options.

