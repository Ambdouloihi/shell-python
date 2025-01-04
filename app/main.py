import sys


def main():
    while True:
        sys.stdout.write("$ ")

        command = input()

        match command.split():
            case ["exit", "0"]:
                exit()
            case _:
                print(f"{' '.join(command)}: command not found")


if __name__ == "__main__":
    main()
