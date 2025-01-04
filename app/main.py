import os
import sys
import shutil
import subprocess

BUILTIN_CMD = {"exit", "echo", "type", "pwd"}


def type_cmd(command):
    if command in BUILTIN_CMD:
        print(f"{command} is a shell builtin")
    elif path := shutil.which(command):
        print(f"{command} is {path}")
    else:
        print(f"{command}: not found")


def main():
    while True:
        sys.stdout.write("$ ")

        command = input()

        match command.split():
            case ["exit", "0"]:
                exit()
            case ["echo", *args]:
                print(*args)
            case ["type", cmd]:
                type_cmd(cmd)
            case ["pwd"]:
                print(os.getcwd())
            case [cmd, *args] if shutil.which(cmd):
                subprocess.run([cmd, *args])
            case _:
                print(f"{command}: command not found")


if __name__ == "__main__":
    main()
