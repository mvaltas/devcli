import devcli.utils.shell as shell


def _expand(obj: enumerate[str]):
    return {index: value for index, value in obj}


def test_cmds_as_list_transformed_into_dict():
    cmds = shell.iter_for(["cmd1", "cmd2"])
    assert _expand(enumerate(["cmd1", "cmd2"])) == _expand(cmds)
