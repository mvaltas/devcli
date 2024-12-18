import devcli.utils.shell as shell


def _expand(obj: enumerate[str]):
    return {index: value for index, value in obj}


def test_cmds_as_list_transformed_into_dict():
    cmds = shell.iter_for(["cmd1", "cmd2"])
    assert _expand(enumerate(["cmd1", "cmd2"])) == _expand(cmds)


def test_cmds_with_alias():
    cmds_dict = {"cmd1": "run_cmd1", "cmd2": "run_cmd2"}
    cmds = shell.iter_for(cmds_dict)
    assert cmds == cmds_dict.items()


def test_single_command_will_return_itself_as_alias():
    cmds = shell.iter_for("cmd with some arguments")
    assert cmds == {"cmd": "cmd with some arguments"}.items()


def test_capture_runs_command_return_results():
    result = shell.capture("echo -n $((1 + 1))")
    assert result == "2"


def test_it_is_possible_to_access_return_code():
    results = shell.run({"cmd1": "exit 126", "cmd2": "exit 255"})
    assert results["cmd1"]["exitcode"] == 126
    assert results["cmd2"]["exitcode"] == 255


def test_in_a_single_run_is_possible_to_collect_exitcode():
    results = shell.run("exit 111")
    assert results["exit"]["exitcode"] == 111


def test_in_multi_run_is_possible_to_collect_exitcode():
    results = shell.run(["exit 111", "exit 222"])
    assert results[0]["exitcode"] == 111
    assert results[1]["exitcode"] == 222


def test_result_transform_dict():
    orig = {
        123: {"alias": "cmd1", "code": "111"},
        456: {"alias": "cmd2", "code": "222"},
    }
    expect = {"cmd1": {"pid": 123, "code": "111"}, "cmd2": {"pid": 456, "code": "222"}}

    assert shell.promote_value_to_key(orig, new_key="alias", new_value="pid") == expect
