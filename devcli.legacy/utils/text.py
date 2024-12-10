from io import StringIO

from rich import Console


def styled_text(text: str, sty: str = None, end: str = ""):
    out = StringIO()
    console = Console(file=out, force_terminal=True)
    console.print(text, style=sty, end=end)
    return out.getvalue()
