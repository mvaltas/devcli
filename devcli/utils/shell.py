import logging
import os
import random
import shlex
import subprocess
import threading
from io import StringIO
from typing import Union, List

from rich.console import Console

logger = logging.getLogger(__name__)


def styled_text(text: str, sty: str = None, end: str = ""):
    out = StringIO()
    console = Console(file=out, force_terminal=True)
    console.print(text, style=sty, end=end)
    return out.getvalue()


def _prepare_command(command):
    quoted_command = shlex.quote(command)
    # attempt to use user's shell, fallback to /bin/sh
    user_shell = os.environ.get("SHELL", "/bin/sh")
    logger.debug(f"resolving shell to: {user_shell}")
    final_command = f"{user_shell} -c {quoted_command}"
    return final_command


def create_process(command: str, cwd: str = os.curdir):
    logger.info(f"create process for: {command}")
    final_command = _prepare_command(command)
    logger.debug(f"about to execute: {final_command}, on: {cwd}")
    proc = subprocess.Popen(
        final_command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        env=os.environ,
        cwd=cwd,
        bufsize=1,
        universal_newlines=True,
        text=True,
    )
    return proc


def process_output(process, process_name: str):
    while True:
        output = process.stdout.readline()
        if process.poll() is not None and output == "":
            break
        if output:
            print(f"{process_name}: {output.strip()}")


def start_process_thread(process, alias):
    thread = threading.Thread(target=process_output, args=(process, alias))
    thread.start()
    return thread


def iter_for(commands):
    """
    Will return an iterable in the form of k,v for
    any str in a list, dict or purely a str
    """
    logger.debug(f"creating iterator for: {commands}")
    if isinstance(commands, list):
        return enumerate(commands)
    elif isinstance(commands, dict):
        return commands.items()
    else:
        # since commands is a single command, split any arguments
        # and get the command name as its own alias
        alias = os.path.basename(commands.split(" ")[0])
        return iter_for({alias: commands})


def interactive(command: str, cwd: str = os.curdir):
    """
    Will spawn the command for interactive shell session
    """
    logger.debug(f"running shell: {command}")
    final_command = _prepare_command(command)
    logger.debug(f"about to execute: {final_command}, on: {cwd}")
    proc = subprocess.Popen(
        final_command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        env=os.environ,
        cwd=cwd,
        bufsize=1,
        universal_newlines=True,
        text=True,
    )
    return proc


def run(command: Union[str, List[str], dict], cwd: str = os.curdir) -> dict:
    """
    A basic shell execution that will execute the command and directly
    output its messages. It won't capture the output and calling this
    is a run and forget.

    If more than one command is given, in a list or a dict format they
    will be fired in order but immediately sent to the background.
    The outputs will be collected in the order they return from
    the commands.
    """
    results = {}
    procs = []
    for alias, cmd in iter_for(command):
        process = create_process(cmd, cwd)
        results.update({process.pid: {"alias": alias}})
        thread = start_process_thread(
            process, styled_text(f"{alias}", f"color({random.randint(1, 231)})")
        )
        procs.append((process, thread))
    for proc, thread in procs:
        results[proc.pid]["exitcode"] = proc.wait()
        thread.join()

    return promote_value_to_key(results, new_key="alias", new_value="pid")


def capture(command: str, cwd: str = os.curdir) -> str:
    """
    A run which captures the output and returns it, it won't display the stdout
    of the command during its execution.
    """
    logger.debug(f"running shell: {command}")
    final_command = _prepare_command(command)
    logger.debug(f"about to execute: {final_command}, on: {cwd}")
    result = subprocess.run(
        final_command, cwd=cwd, shell=True, capture_output=True, text=True
    )
    logger.debug(f"return code: {result.returncode}")
    return result.stdout


def promote_value_to_key(nested_dict: dict, new_key: str, new_value: str) -> dict:
    """This function works on a dict which has values that are also dicts.
    It will swap a value of the nested dict and add the key as a value.
    It works with the assumption that the values that can be accessed
    on 'new_key' are unique enough to become keys on the dict, if
    not data will be lost during the transformation.

    Example:
        { 123: {"alias": "cmd1", "code": "111" },
          456: {"alias": "cmd2", "code": "222" }}
        transform with new_key="alias", new_value="pid" results in
        { "cmd1": { "pid": 123, "code": "111" },
          "cmd2": { "pid": 456, "code": "222" }}
    """
    transformed_dict = {}
    for key, value in nested_dict.items():
        nk_key = value.pop(new_key)
        if nk_key not in transformed_dict:
            transformed_dict[nk_key] = {}
        transformed_dict[nk_key].update({new_value: key, **value})
    return transformed_dict


class ShellExecutable:
    logger = logging.getLogger(__name__)

    def __init__(self):
        self.result = None

    def capture(self, cmd: str):
        self.result = capture(cmd)
        return self.result
