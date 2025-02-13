from typer import Context

import devcli.framework as cmd

cli = cmd.new("Shortcuts to read from devcli configuration")


@cli.command()
def get(ctx: Context, key: str):
    cmd.echo(ctx.obj[key])
