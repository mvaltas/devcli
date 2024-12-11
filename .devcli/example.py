import devcli.framework as cmd

cli = cmd.new("Simplest example of creating a command")


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
    Replies with a PONG! using basic color from rich text
    """
    cmd.echo('[green]PONG![/green]')


@cli.command()
def text():
    """
    Demo types of text output you can use
    out of the box.
    """
    cmd.echo('This is an echo(msg)')
    cmd.notice('This is a notice(msg)')
    cmd.warn('This is a warn(msg)')
    cmd.error('This is an error(msg)')

