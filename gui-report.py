import csv
import locale
from datetime import datetime, timedelta, date
import tkinter as tk
from tkinter import scrolledtext
from rich.console import Console
from rich.text import Text
from rich.panel import Panel

# === CONFIG ===
CSV_FILE = "/home/matias/pmwd/timeTable.csv"
SPANISH_TIME_FORMAT = "%a %d %b %Y %H:%M:%S %z"

console = Console()

# Attempt to set Spanish locale
try:
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
except locale.Error:
    console.print("⚠️ [yellow]Warning: Spanish locale 'es_ES.UTF-8' not available.[/yellow]")

def parse_time(ts):
    ts = ts.strip()
    if ts[-3:].startswith(("-", "+")):
        ts += "00"
    return datetime.strptime(ts, SPANISH_TIME_FORMAT)

def clean_int(value):
    return int(''.join(filter(str.isdigit, value)))

def read_today_tasks(filename):
    tasks = []
    with open(filename, newline='') as f:
        reader = csv.reader(f)
        headers = next(reader, None)  # Skip header

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

def build_text_timeline(tasks):
    """Build a string-based timeline for use in GUI."""
    if not tasks:
        return "[No tasks recorded for today.]"

    tasks.sort(key=lambda x: x["start"])
    timeline = ""
    previous_end = None

    for task in tasks:
        start = task["start"]
        end = task["end"]
        duration_minutes = max(1, int(task["duration"].total_seconds() // 60))

        if previous_end and start > previous_end:
            dead_time_minutes = int((start - previous_end).total_seconds() // 60)
            timeline += "|" * dead_time_minutes

        timeline += "-" * duration_minutes
        previous_end = end

    return timeline

def build_plain_text_report(tasks):
    timeline = build_text_timeline(tasks)
    report_lines = ["Timeline for Today\n" + "="*60 + "\n"]
    report_lines.append(timeline + "\n" + "="*60 + "\n")

    for task in tasks:
        report_lines.append(
            f"Start:    {task['start'].strftime('%H:%M:%S')}\n"
            f"End:      {task['end'].strftime('%H:%M:%S')}\n"
            f"Duration: {str(task['duration'])}\n"
            f"Details:  {task['desc_start']} → {task['desc_end']}\n"
            + "-"*60 + "\n"
        )
    return "\n".join(report_lines)

def show_report_gui(report_text):
    root = tk.Tk()
    root.title("Daily Task Report")

    text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=100, height=30)
    text_area.insert(tk.INSERT, report_text)
    text_area.configure(state='disabled')  # Make read-only
    text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    root.mainloop()

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
            timeline.append("█" * dead_time_minutes, style="grey50")

        timeline.append("█" * duration_minutes, style="red")
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

    # Show GUI with timeline + details
    report_text = build_plain_text_report(tasks)
    show_report_gui(report_text)

if __name__ == "__main__":
    tasks = read_today_tasks(CSV_FILE)
    print_timeline(tasks)
