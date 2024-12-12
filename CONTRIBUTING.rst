=========================
Contributing to *devcli*
=========================

Thank you very much for your interest in contributing with *devcli*. I'll try
to outline some guidance if you want to extend and improve this tool.

Package organization
--------------------

* ``devcli.core`` - dedicated only to the basic cli setup and execution
* ``devcli.config`` - dedicated to the config subsystem, parsing and access
* ``devcli.framework`` - dedicated to things that enable the creation of subcommands
* ``devcli.utils`` - utility functions that can be used internally or imported to subcommands
* ``devcli.commands`` - out of the box commands, these should only depend on ``devcli.utils`` and ``devcli.framework``


Principles behind devcli
--------------------------

- **Simplicity at core**: As simple as possible at its core.
  Its power comes for the ability to extend it. As more complex the core gets,
  the harder it will be to extend it.

- **Extensibility**: Easy to extend. Given the simplicity of
  its core, it should be easy to add new commands.

- **Discoverability**: Commands should be easy to discover and understand. The paradigm
  of commands, subcommands, and options should be leveraged to explain the target system
  of the command.

- **Proximity**: Information on how to work with a system should be close to the system
  itself.

- **Interfacing**: *devcli* serves as an interface to other systems. As such, it should
  provide the features necessary to help create and diagnose these interfaces,
  rather than functioning as the system itself.

- **Disposability**: Under any circumstance, the system which *devcli* interfaces should rely on it to work.
  It is meant to help developers, not to be the part of the system. Removing it should not be detrimental
  to the system.

