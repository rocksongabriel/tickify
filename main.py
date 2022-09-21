#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime
from typing import List

from rich.console import Console
from rich.table import Table
import typer

from db.config import engine
from db.models import Base
from pomodoro import crud
from pomodoro.pomodoro import Pomodoro
from pomodoro.utils import clear_screen

Base.metadata.create_all(bind=engine)

# Instantiate console
console = Console()


time_options = [
    {
        "round_time": ("15:00", "15 minutes"),
        "short_break": ("3:00", "3 minutes"),
        "long_break": ("10:00", "10 minutes"),
    },
    {
        "round_time": ("15:00", "15 minutes"),
        "short_break": ("5:00", "5 minutes"),
        "long_break": ("10:00", "10 minutes"),
    },
    {
        "round_time": ("25:00", "25 minutes"),
        "short_break": ("5:00", "5 minutes"),
        "long_break": ("10:00", "10 minutes"),
    },
    {
        "round_time": ("30:00", "30 minutes"),
        "short_break": ("5:00", "5 minutes"),
        "long_break": ("10:00", "10 minutes"),
    },
    {
        "round_time": ("30:00", "30 minutes"),
        "short_break": ("10:00", "10 minutes"),
        "long_break": ("15:00", "15 minutes"),
    },
    {
        "round_time": ("45:00", "45 minutes"),
        "short_break": ("10:00", "10 minutes"),
        "long_break": ("15:00", "15 minutes"),
    },
    {
        "round_time": ("45:00", "45 minutes"),
        "short_break": ("10:00", "10 minutes"),
        "long_break": ("20:00", "20 minutes"),
    },
    {
        "round_time": ("60:00", "1 hour"),
        "short_break": ("10:00", "10 minutes"),
        "long_break": ("30:00", "30 minutes"),
    },
]


def display_time_options(options):
    """
    Display the time options for a pomodoro session
    """
    table = Table(
        title="Time Options for Pomodoro Session",
        title_style="bold green",
        show_lines=True,
    )
    table.add_column("Option", style="bold yellow")
    table.add_column("Round Time", style="bold green")
    table.add_column("Short Break Time", style="bold")
    table.add_column("Long Break Time", style="bold")

    for number, option in enumerate(options, start=1):
        table.add_row(
            str(number),
            option["round_time"][1],
            option["short_break"][1],
            option["long_break"][1],
        )

    console.print(table)


def display_program_options():
    table = Table(title="Options", title_style="bold green")

    table.add_column("Option Number", style="bold blue")
    table.add_column("Option", style="magenta bold")
    table.add_column("Description", style="bold italic")

    options: list[dict[str, str]] = [
        {
            "number": "1",
            "option": "Show Today's Statistics",
            "description": "View the statistics of all pomodoro sessions today",
        },
        {
            "number": "2",
            "option": "All Statistics",
            "description": "View all previous pomodoro sessions statistics",
        },
        {
            "number": "3",
            "option": "Run Pomodoro",
            "description": "Run a new pomodoro session",
        },
    ]

    for option in options:
        table.add_row(option["number"], option["option"], option["description"])

    console.print(table)


def start_new_pomodoro_instance():
    clear_screen()

    clear_screen()
    console.rule("[bold]Pomodoro session information")

    session_rounds = int(
        console.input("[bold yellow]How many rounds per session? eg, 4: ")
    )
    print()

    pomodoros = int(
        console.input(
            "[bold yellow]How many pomodoro sessions do you want to run? eg, 2: "
        )
    )
    print()
    # Pomodoro options
    display_time_options(time_options)
    time_option = eval(console.input("[bold yellow]Your time choice: "))

    round_time = int(time_options[time_option - 1]["round_time"][0].split(":")[0])
    short_break = int(time_options[time_option - 1]["short_break"][0].split(":")[0])
    long_break = int(time_options[time_option - 1]["long_break"][0].split(":")[0])

    # Instantiate pomodoro
    pomodoro = Pomodoro(
        pomodoros=pomodoros,
        session_rounds=session_rounds,
        session_minutes=round_time,
        short_break_minutes=short_break,
        long_break_minutes=long_break,
    )

    clear_screen()

    pomodoro.start()


def show_all_statistics():
    all_records = crud.get_all_records()

    table = Table(title="All Records", title_style="bold green")

    table.add_column("Started", style="bold")
    table.add_column("Ended", style="bold")
    table.add_column("Sessions", style="bold blue")
    table.add_column("Rounds Per Session", style="blue")
    table.add_column("Minutes per Round")
    table.add_column("Completed Sessions")
    table.add_column("Completed Rounds")
    table.add_column("Completed")

    for record in all_records:
        table.add_row(
            str(record.started),
            str(record.ended),
            str(record.number_of_sessions),
            str(record.rounds_per_session),
            str(record.minutes_per_session),
            str(record.total_completed_sessions),
            str(record.total_completed_rounds),
            str(record.done),
        )

    clear_screen()
    console.rule("[bold]Statistics")
    console.print(table)


def show_today_statistics():
    records = crud.get_todays_records()

    total_minutes_worked = 0

    table = Table(
        title=f"Pomodoros for Today: {datetime.today().date().strftime('%A %d %B %Y')}",
        title_style="bold green",
        title_justify="left",
    )

    table.add_column("Time Started", style="bold")
    table.add_column("Time Ended", style="bold")
    table.add_column("Sessions", style="bold blue")
    table.add_column("Rounds Per Session", style="bold blue")
    table.add_column("Minutes per Round", style="bold")
    table.add_column("Completed Sessions", style="bold")
    table.add_column("Completed Rounds", style="bold")
    table.add_column("Completed", style="bold")
    table.add_column("Time Spent Working", style="bold green")

    for record in records:
        minutes_worked = record.total_completed_rounds * record.minutes_per_session
        total_minutes_worked += minutes_worked

        table.add_row(
            str(record.started.time()),
            str(record.ended.time() if record.ended else "-"),
            str(record.number_of_sessions),
            str(record.rounds_per_session),
            str(record.minutes_per_session),
            str(record.total_completed_sessions),
            str(record.total_completed_rounds),
            str(record.done),
            f"{minutes_worked} minutes",
        )

    table.caption = f"Total Minutes Worked: {total_minutes_worked}"
    table.caption_style = "yellow"
    table.caption_justify = "right"

    clear_screen()
    console.rule(
        f"[bold red]Statistics for: {datetime.today().date().strftime('%A %d %B %Y')}"
    )  # TODO: make the date human readable
    console.print(table)
    print()


def main():
    clear_screen()

    # Display program options
    display_program_options()
    option = eval(console.input("[bold yellow]Enter your choice, eg, 1: "))

    if option == 1:
        show_today_statistics()
    elif option == 2:
        show_all_statistics()
    elif option == 3:
        start_new_pomodoro_instance()


if __name__ == "__main__":
    typer.run(main)
