import subprocess, asyncio
from subprocess import PIPE
from asyncio.subprocess import PIPE as aPIPE
import shlex, itertools, os, glob
from typing import NamedTuple, Optional, List

class CommandResults(NamedTuple):
    command: Optional[str]
    return_code: Optional[int]
    stdout: Optional[str]
    stderr: Optional[str]


BLANK_RESULTS = CommandResults(None, None, None, None)

##### STANDARD / SYNCRONOUS #####

def _split_expand(clitext: str) -> List[str]:
    split_command = shlex.split(clitext)
    split_expanded_command = []
    for part in split_command:
        part = os.path.expanduser(part) # expand '~' at begining of parts
        file_wildcard_expantion = (glob.glob(part)) # expand *,? for file_names
        if file_wildcard_expantion == []:
            split_expanded_command.append(part)
        else:
            split_expanded_command += file_wildcard_expantion
    return split_expanded_command

def _expand(clitext: str) -> str:
    return " ".join(_split_expand(clitext))

def run(command: str, stdin: Optional[str] = None, encoding: str = 'utf-8', capture_output: bool = True) -> CommandResults:
    command = command.strip()
    split_command = _split_expand(command)
    if '|' in split_command:
        grouped_commands = itertools.groupby(split_command, lambda x: x is "|")
        commands_seporated_on_pipe = [" ".join(list(sub_command_group)) for is_pipe, sub_command_group in grouped_commands if not is_pipe]
        return _run_pipeline(commands_seporated_on_pipe)
    else:
        process: subprocess.Popen
        if capture_output:
            process = subprocess.Popen(split_command, stdin=PIPE, stdout=PIPE, stderr=PIPE, encoding=encoding)
        else:
            process = subprocess.Popen(split_command, stdin=PIPE, encoding=encoding)
        stdout, stderr = process.communicate(stdin)
        return_code = process.wait()
        return CommandResults(command, return_code, stdout, stderr)

def _run_pipeline(commands: List[str], stdin: Optional[str] = None, encoding: str = 'utf-8') -> CommandResults:
    command_results = BLANK_RESULTS
    for command in commands:
        command_results = run(command, stdin=stdin, encoding=encoding)
        stdin = command_results.stdout
    return command_results


def cd(path:str) -> None:
    os.chdir(_expand(path))

def exists(path: str) -> bool:
    return os.path.exists(_expand(path))

def isdir(path: str) -> bool:
    return os.path.isdir(_expand(path))
