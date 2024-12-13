from typer import Context

import devcli.framework as cmd
from devcli.framework.errors import MissConfError
from devcli.utils.one_password import OnePassword

cli = cmd.new("Shortcuts for 1Password CLI")


def get_op(config):
    # vault is optional and defaults to 'Private' on OnePassword
    vault = config["devcli.commands.op.vault"]
    if vault is None:
        vault = "Private"

    # account is mandatory for op cli to work
    acct = config["devcli.commands.op.account"]
    if acct is None:
        raise MissConfError(
            topic="devcli.commands.op", entry="account", example="VALID_OP_ACCOUNT"
        )
    return OnePassword(acct, vault=vault)


@cli.command()
def credential(ctx: Context, key: str):
    """
    Will read from 1Password an entry in the form op://Private/{key}/credential
    """
    cmd.echo(get_op(ctx.obj).credential(key))


@cli.command()
def password(ctx: Context, item: str):
    """
    Will read from 1Password a login entry and return its password
    """
    cmd.echo(get_op(ctx.obj).password(item))
