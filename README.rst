devcli - A command line tool for developers
=========================================================

Why
---

There's probably no shortage of tools for developers. *devcli* came from two
necessities I had. First, I wanted to avoid memorizing complex command lines
and the order of commands for daily repetitive tasks—something like [The
General Problem](https://xkcd.com/974/). During my time as a software
consultant, I had to memorize a lot of these commands for each new project. The
second necessity was a consequence of the first. Since new commands had to be
added and removed easily, I needed a way to "framework" the creation of these
commands, and that's when I decided to create *devcli*.

Principles behind devcli
---------------------------------

- **Simplicity at core**: As simple as possible at its core.
  Its power comes for the ability to extend it. As more complex the core gets,
  the harder it will be to extend it.

- **Extensibility**: Easy to extend. Given the simplicity of
  its core, it should be easy to add new commands.

- **Discoverability**: Commands should be easy to discover and understand. The paradignm
  of commands, subcommands, and options should be leaveraged to explain the target system
  of the command.

- **Proximity**: Information on how to work with a system should be close to the system
  itself.

- **Interfacing**: *devcli* is an interface to other systems, as such, it should provide
  the features to help create such interfaces and diagnose it, and not to be the system.

- **Ephemeralbility**: Under any circumstance, the system should rely on *devcli* to work.
  It is meant to help the developers, not to be the system. Removing it should not be detrimental
  to the system.

