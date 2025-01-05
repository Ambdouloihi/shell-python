import os
import sys
import shutil
from subprocess import run, PIPE
import shlex

BUILTIN_CMD = {"exit", "echo", "type", "pwd", "cd"}

REDIRECTION_MODES = {
    ">": ("w", True, False),
    "1>": ("w", True, False),
    ">>": ("a", True, False),
    "1>>": ("a", True, False),
    "2>": ("w", False, True),
    "2>>": ("a", False, True),
}


def type_cmd(command, stdout=sys.stdout, stderr=sys.stderr):
    if command in BUILTIN_CMD:
        print(f"{command} is a shell builtin", file=stdout)
    elif path := shutil.which(command):
        print(f"{command} is {path}", file=stdout)
    else:
        print(f"{command}: not found", file=stderr)


def cd_cmd(path, stderr=sys.stderr):
    try:
        os.chdir(os.path.expanduser(path))
    except OSError:
        print(f"cd: {path}: No such file or directory", file=stderr)


def handle_cmd(cmd_args, stdout=sys.stdout, stderr=sys.stderr):
    match cmd_args:
        case ["exit", "0"]:
            exit()
        case ["echo", *args]:
            print(*args, file=stdout)
        case ["type", cmd]:
            type_cmd(cmd, stdout, stderr)
        case ["pwd"]:
            print(os.getcwd(), file=stdout)
        case ["cd", pth]:
            cd_cmd(pth, stderr)
        case [cmd, *args] if shutil.which(cmd):
            process = run([cmd, *args], stdout=PIPE, stderr=PIPE, text=True)
            print(process.stdout, file=stdout, end="")
            print(process.stderr, file=stderr, end="")
        case _:
            print(f"{' '.join(cmd_args)}: command not found", file=stderr)


def main():
    while True:
        sys.stdout.write("$ ")
        command = input()
        match shlex.split(command):
            case [*cmd_args, op, file] if op in REDIRECTION_MODES:
                mode, capture_stdout, capture_stderr = REDIRECTION_MODES[op]
                with open(file, mode) as f:
                    handle_cmd(
                        cmd_args,
                        stdout=f if capture_stdout else None,
                        stderr=f if capture_stderr else None,
                    )
            case cmd_args:
                handle_cmd(cmd_args)


if __name__ == "__main__":
    main()
