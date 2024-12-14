from rich import print


def echo(msg: str):
    """
    Just print a message into the terminal.
    It uses rich.print() which allows for color tagging like [red]message[/red].
    :param msg: A str with the message
    """
    print(msg)


def error(msg: str):
    """
    Print a message in red
    """
    print(f"[red]{msg}[/red]")


def warn(msg: str):
    """
    Prints a message in yellow
    """
    print(f"[yellow]{msg}[/yellow]")


def info(msg: str):
    """
    Prints a message in cyan
    """
    print(f"[cyan]{msg}[/cyan]")
