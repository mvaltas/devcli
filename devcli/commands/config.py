from typer import Context

import devcli.framework as cmd

cli = cmd.new("Shortcuts to read from devcli configuration")


@cli.command()
def get(ctx: Context, key: str):
    """
    Gets the value of a config using 'key'
    """
    cmd.echo(ctx.obj[key])


@cli.command()
def get_all(ctx: Context):
    """
    List all configurations after parsing in TOML format

    The configuration will not necessarily resemble the
    original configuration files. Topics will be shown
    until the (n - 1) key, follow by their values.
    """
    cmd.echo(ctx.obj)
