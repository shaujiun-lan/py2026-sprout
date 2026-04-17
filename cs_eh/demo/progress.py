import time
from rich.progress import (
    Progress,
    SpinnerColumn,
    TextColumn,
    BarColumn,
    TaskProgressColumn,
    TimeRemainingColumn,
)

custom_progress = Progress(
    SpinnerColumn("monkey"),
    TextColumn("[bold cyan]{task.description}"),
    BarColumn(
        bar_width=40,
        style="grey15",
        complete_style="green",
        finished_style="bold yellow"
    ),
    TaskProgressColumn(),
    TimeRemainingColumn(),
)

with custom_progress as progress:
    task1 = progress.add_task("task1", total=100)
    task2 = progress.add_task("task2", total=150)

    while not progress.finished:
        progress.update(task1, advance=0.5)
        progress.update(task2, advance=1.2)
        time.sleep(0.02)
