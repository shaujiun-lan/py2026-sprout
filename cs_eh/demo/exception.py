from rich.console import Console

console = Console()

try:
    1/0
except Exception:
    console.print_exception(show_locals=True)