import os
from typer import Context
from pathlib import Path

import devcli.framework as cmd

cli = cmd.new("Edit different files using text editor")

logger = cmd.logger()

# closure to create partial func
def prep_editor(ctx: Context):
    def run_editor(file: Path):
        """Open editor on file"""
        c_editor = ctx.obj["devcli.commands.edit.editor"]
        e_editor = os.getenv("EDITOR", "vim")
        logger.info(f"env EDITOR={e_editor} config={c_editor}")

        # config first, env and last default
        editor = c_editor if c_editor else e_editor
        logger.info(f"selected editor: {editor}")

        os.execvp(editor, [editor, file])

    def open_editor(file: Path):
        run_editor(file)

    return open_editor


@cli.command()
def config(ctx: Context, dry: bool = False):
    """ Opens the most specific configuration """
    editor = prep_editor(ctx)
    configs = ctx.obj.files()
    logger.info(f"Found these configurations: {configs}")
    if not configs:
        cmd.stop("No configuration files were found.")
    elif dry:
        cmd.info(f"Will edit: {configs[-1]}")
    else:
        # last file is the most specific one
        editor(configs[-1])


@cli.command("command")
def edit_command(ctx: Context, name: str):
    """ Opens the command [name] for edit """
    editor = prep_editor(ctx)
    configs = ctx.obj.files()
    p = Path(configs[-1]).parent
    subcmd = p / f"{name}.py"
    logger.info(f"command search path: {subcmd}")
    if subcmd.exists():
        logger.info(f"command exists opening editor...")
        editor(subcmd)
    else:
        logger.info(f"command does not exist in {subcmd}, stopping.")
        cmd.stop(f"cmd: {subcmd.name} not found in path: {p}")
