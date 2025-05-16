import csv
import locale
from datetime import datetime, timedelta, date
from rich.console import Console
from rich.text import Text
from rich.panel import Panel

# === CONFIG ===
CSV_FILE = "/home/matias/pmwd/timeTable.csv"
BLOCK_CHAR = "█"
SPANISH_TIME_FORMAT = "%a %d %b %Y %H:%M:%S %z"

console = Console()

# Attempt to set Spanish locale
try:
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
except locale.Error:
    console.print("⚠️ [yellow]Warning: Spanish locale 'es_ES.UTF-8' not available.[/yellow]")

def parse_time(ts):
    """Parse timestamps like 'vie 16 may 2025 19:53:46 -03' into datetime objects."""
    ts = ts.strip()
    if ts[-3:].startswith(("-", "+")):
        ts += "00"
    return datetime.strptime(ts, SPANISH_TIME_FORMAT)

def clean_int(value):
    """Remove non-digit characters and convert to int."""
    return int(''.join(filter(str.isdigit, value)))

def read_today_tasks(filename):
    tasks = []
    with open(filename, newline='') as f:
        reader = csv.reader(f)
        headers = next(reader, None)  # skip header row

        for row_num, row in enumerate(reader, start=2):
            if len(row) < 7:
                console.print(f"[yellow]Skipping line {row_num}: incomplete row.[/yellow]")
                continue

            start, desc_start, end, desc_end, h, m, s = row

            try:
                start_dt = parse_time(start)
                if start_dt.date() != date.today():
                    continue

                end_dt = parse_time(end)
                duration = timedelta(
                    hours=clean_int(h),
                    minutes=clean_int(m),
                    seconds=clean_int(s)
                )

                tasks.append({
                    "start": start_dt,
                    "desc_start": desc_start,
                    "end": end_dt,
                    "desc_end": desc_end,
                    "duration": duration
                })
            except Exception as e:
                console.print(f"[red]Skipping line {row_num} due to parse error: {e}[/red]")
    return tasks

def print_timeline(tasks):
    if not tasks:
        console.print("No tasks for today.", style="bold yellow")
        return

    tasks.sort(key=lambda x: x["start"])
    timeline = Text()
    previous_end = None

    for task in tasks:
        start = task["start"]
        end = task["end"]
        duration_minutes = max(1, int(task["duration"].total_seconds() // 60))

        if previous_end and start > previous_end:
            dead_time_minutes = int((start - previous_end).total_seconds() // 60)
            timeline.append(BLOCK_CHAR * dead_time_minutes, style="grey50")

        timeline.append(BLOCK_CHAR * duration_minutes, style="red")
        previous_end = end

    console.rule("[bold blue]Timeline for Today")
    console.print(timeline)

    for task in tasks:
        panel = Panel.fit(
            f"[bold]Start:[/bold] {task['start'].strftime('%H:%M:%S')}\n"
            f"[bold]End:[/bold] {task['end'].strftime('%H:%M:%S')}\n"
            f"[bold]Duration:[/bold] {str(task['duration'])}\n"
            f"[bold]Details:[/bold] {task['desc_start']} → {task['desc_end']}",
            title="Task",
            border_style="red"
        )
        console.print(panel)

if __name__ == "__main__":
    tasks = read_today_tasks(CSV_FILE)
    print_timeline(tasks)
