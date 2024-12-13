from typer import Context
import devcli.framework as cmd

cli = cmd.new("Examples on how create cli commands with *devcli*")


@cli.command()
def hello(name: str, rainbow: bool = False):
    """
    Simplest example of a command, it just outputs "Hello, NAME!"

    If --rainbow is passed it will make it colorful
    """
    if rainbow:
        colors = ["red", "orange1", "yellow1", "green", "blue", "purple"]
        name = "".join(
            f"[{colors[i % len(colors)]}]{char}[/{colors[i % len(colors)]}]"
            for i, char in enumerate(name)
        )
    cmd.echo(f"Hello, {name}!")


@cli.command()
def ping():
    """
    Replies with a PONG!
    """
    cmd.echo("PONG!")


@cli.command()
def text():
    """
    Demo types of text output you can use
    out of the box as shortcuts.
    """
    cmd.echo("This is a cmd.echo(msg)")
    cmd.notice("This is a cmd.notice(msg)")
    cmd.warn("This is a cmd.warn(msg)")
    cmd.error("This is a cmd.error(msg)")


@cli.command()
def config(ctx: Context):
    """
    Example of access to global configurations
    """
    cmd.echo(f"Default devcli config: {ctx.obj['devcli']}")
