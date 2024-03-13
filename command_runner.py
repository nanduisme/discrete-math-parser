from matplotlib import table
import rich
import table_gen

_COMMANDS = [
    "exit",
    "quit",
    "clear",
    "boolmode",
]


def run():
    while True:
        text = input("> ")

        if text == "":
            continue

        elif text in _COMMANDS:
            exit_code = run_command(text)
            if exit_code == 0:
                break
            continue

        else:
            tables = table_gen.process_input(text)
            for table in tables:
                print()
                rich.print(table)
            print()

def run_command(cmd: str):
    """
    Executes the given command and returns the appropriate exit code.

    Args:
        cmd (str): The command to be executed.

    Returns:
        int: The exit code. 0 if the command is 'exit' or 'quit', 1 if the command is empty or 'clear',
             and 1 for all other commands.
    """
    if cmd in ["exit", "quit"]:
        return 0  # exit
    if cmd == "":
        return 1  # continue
    if cmd == "clear":
        print("\033c", end="")
        return 1
    if cmd.startswith("boolmode"):
        table_gen._state["bool_mode"] = not table_gen._state["bool_mode"]
        bool_mode = table_gen._state["bool_mode"]
        rich.print(f"boolmode is now {bool_mode}\n")
        return 1
