from typing import Optional
from typer import Context, Option

import devcli.framework as cmd
from devcli.framework.errors import MissConfError
from devcli.utils.one_password import OnePassword

cli = cmd.new("Shortcuts for 1Password CLI")


def get_op(config, account: Optional[str] = None):
    # vault is optional and defaults to 'Private' on OnePassword
    vault = config["devcli.commands.op.vault"]
    if vault is None:
        vault = "Private"

    # account is mandatory and defaults to 'devcli.commands.op.accounts.default'
    if account is not None:
        acct = config[f"devcli.commands.op.accounts.{account}"]
    else:
        acct = config["devcli.commands.op.accounts.default"]
        if acct is None:
            raise MissConfError(
                topic="devcli.commands.op.accounts",
                entry="default",
                example="VALID_OP_ACCOUNT",
            )
    return OnePassword(acct, vault=vault)


@cli.command()
def credential(
    ctx: Context,
    key: str,
    account: Optional[str] = Option(None, "--account", help="1Password account to use"),
):
    """
    Will read from 1Password an entry in the form op://Private/{key}/credential
    """
    cmd.echo(get_op(ctx.obj, account).credential(key))


@cli.command()
def password(
    ctx: Context,
    item: str,
    account: Optional[str] = Option(None, "--account", help="1Password account to use"),
):
    """
    Will read from 1Password a login entry and return its password
    """
    cmd.echo(get_op(ctx.obj, account).password(item))
