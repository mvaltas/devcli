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

