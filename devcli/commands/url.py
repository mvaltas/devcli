from typer import Context

import devcli.framework as cmd
import devcli.utils.shell as shell
from devcli.framework.errors import MissConfError

cli = cmd.new("Shortcuts URLs bookmarking")


def fuzzy_search(urls: dict, key: str):
    """
    A simple fuzzy search for the URL key, if no exact
    matches are found the 'last' partial match will be
    used as fallback.

    The last partial match is the first alphabetically
    so, if entries are 'site', and 'site-prod' and the
    search is 'si', we should return 'site' value.
    """
    partial_match = None
    for k, v in reversed(sorted(urls.items())):
        if key == k:
            return v
        elif key in k:
            partial_match = v
    return partial_match


@cli.command()
def open(ctx: Context, key: str):
    """
    Open a URL from the configuration
    """
    url = fuzzy_search(ctx.obj[f"devcli.commands.url"], key)
    if url is None:
        raise MissConfError(topic="devcli.commands.url", entry=key, example="VALID_URL")

    cmd.info(f"Opening '{url}'")
    shell.run(f"open '{url}'")


@cli.command()
def list(ctx: Context):
    """
    List all the URLs in the configuration
    """
    urls = ctx.obj[f"devcli.commands.url"]
    cmd.info("Available URLs:\n")
    for k, v in urls.items():
        cmd.echo(f"{k}: {v}")


@cli.command()
def search(ctx: Context, key: str):
    """
    Search for a URL in the configuration
    """
    cmd.info(f"Searching for '[green]{key}[/green]' in URLs\n")
    for k, v in ctx.obj[f"devcli.commands.url"].items():
        if key in k or key in v:
            cmd.echo(f"{k}: {v}")
