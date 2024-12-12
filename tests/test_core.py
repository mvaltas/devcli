import os
from pathlib import Path

import pytest
from pyfakefs.fake_filesystem import PatchMode
from pyfakefs.fake_filesystem_unittest import Patcher
from typer import Typer
from typer.testing import CliRunner

from devcli.core import project_root, traverse_search, traverse_load_dynamic_commands, load_dynamic_commands

DYN_COMMAND = """
import devcli.framework as cmd
cli = cmd.new("test")
@cli.command()
def hello():
    pass
"""

runner = CliRunner()

@pytest.fixture
def fs_patch_open():
    with Patcher(patch_open_code=PatchMode.AUTO) as p:
        yield p.fs

def test_project_root_resolves_to_right_directory():
    assert str(project_root()) == os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


def test_project_root_resolves_to_right_directory_with_filename():
    assert str(project_root(__file__)) == os.path.abspath(__file__)


def test_traverse_search_for_file_name(fs):
    files = [
        Path("/org/dept/project/module/file.txt"),
        Path("/org/file.txt")
    ]
    for f in files:
        fs.create_file(f)

    assert traverse_search('file.txt', "/org/dept/project/module") == files


def test_traverse_search_for_directory(fs):
    expected = [
        Path("/org/dept/project/module/.devcli"),
        Path("/org/dept/project/.devcli"),
        Path("/org/dept/.devcli"),
        Path("/org/.devcli"),
        Path("/.devcli")
    ]
    for d in expected:
        fs.create_dir(d)

    assert traverse_search('.devcli', '/org/dept/project/module') == expected

def test_load_commands_dynamically():
    app = Typer()
    # This should load the example.py subcommand on .devcli
    load_dynamic_commands(app, project_root('.devcli'))
    # Executed the example command just loaded
    result = runner.invoke(app, ["example", "ping"])

    assert "PONG!" in result.output


def test_traverse_load_commands_dynamically(fs_patch_open):
    """
    This test uses PatchMode.AUTO from pyfakefs as we load commands
    dynamic using module loading which user ``open_code()`` function.
    This function is not by default faked by pyfakefs.

    see: <https://github.com/pytest-dev/pyfakefs/discussions/1079>.
    """
    # the user is current in the following directory
    fs_patch_open.create_dir('/org/dept/project/module')
    fs_patch_open.cwd = '/org/dept/project/module'
    # and two different commands are defined, one at module level and another at project level
    fs_patch_open.create_file("/org/dept/project/module/.devcli/module.py", contents=DYN_COMMAND)
    fs_patch_open.create_file('/org/dept/project/.devcli/project.py', contents=DYN_COMMAND)

    app = Typer()
    # we start our search from module directory
    traverse_load_dynamic_commands(app, '.devcli', Path.cwd())

    # both, project and module commands are available to run
    result = runner.invoke(app, ['project'])
    assert "Usage: root project" in result.output
    result = runner.invoke(app, ['module'])
    assert "Usage: root module" in result.output