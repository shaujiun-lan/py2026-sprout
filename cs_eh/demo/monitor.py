import time
import psutil
from rich.live import Live
from rich.table import Table
from rich.console import Console

def generate_cpu_table() -> Table:
    core_percentages = psutil.cpu_percent(interval=None, percpu=True)
    total_percent = psutil.cpu_percent(interval=None)

    try:
        cpu_freq = psutil.cpu_freq().current
        freq_info = f" | Freq: {cpu_freq:.0f} MHz"
    except Exception:
        freq_info = ""

    table = Table(
        title=f"Real-Time CPU Core Monitor (Total Load: {total_percent}%{freq_info})", 
        style="blue",
        title_justify="left"
    )
    
    table.add_column("Core", justify="center", style="cyan", no_wrap=True)
    table.add_column("Usage", justify="right", width=10)
    table.add_column("Live Load Chart", justify="left", width=45)

    for i, usage in enumerate(core_percentages):
        if usage < 50:
            color = "green"
        elif usage < 85:
            color = "yellow"
        else:
            color = "red"
            
        bar_length = int((usage / 100) * 40)
        bar_string = "█" * bar_length
        
        usage_str = f"[{color}]{usage:5.1f} %[/{color}]"
        bar_display = f"[{color}]{bar_string}[/{color}]"
        
        table.add_row(f"Core {i}", usage_str, bar_display)
        
    return table

console = Console()
console.clear() 

psutil.cpu_percent(interval=None, percpu=True)
psutil.cpu_percent(interval=None)

with Live(generate_cpu_table(), refresh_per_second=2, console=console) as live:
    try:
        while True:
            time.sleep(0.5)
            live.update(generate_cpu_table())
            
    except KeyboardInterrupt:
        pass

console.print("\n[bold green]Monitoring session ended safely.[/bold green]")
