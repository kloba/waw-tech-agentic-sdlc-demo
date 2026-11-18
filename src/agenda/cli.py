"""Command line interface: ``python -m agenda <command>``."""

from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path

from agenda.core import Talk, find_conflicts, load_agenda, next_talk, talks_in_room

DEFAULT_FILE = Path(__file__).resolve().parents[2] / "data" / "agenda.json"


def _fmt(talk: Talk) -> str:
    return f"{talk.start:%H:%M}-{talk.end:%H:%M}  {talk.room:<8} {talk.title} ({talk.speaker})"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="agenda", description="Query the conference agenda.")
    parser.add_argument("--file", type=Path, default=DEFAULT_FILE, help="agenda JSON file")
    sub = parser.add_subparsers(dest="command", required=True)

    list_cmd = sub.add_parser("list", help="list talks")
    list_cmd.add_argument("--room", help="only talks in this room")

    next_cmd = sub.add_parser("next", help="show the next talk")
    next_cmd.add_argument("--room", help="only talks in this room")
    next_cmd.add_argument("--now", type=datetime.fromisoformat, default=None, help="ISO time, default: now")

    sub.add_parser("conflicts", help="show overlapping talks in the same room")

    args = parser.parse_args(argv)
    talks = load_agenda(args.file)

    if args.command == "list":
        for talk in talks_in_room(talks, args.room) if args.room else talks:
            print(_fmt(talk))
    elif args.command == "next":
        talk = next_talk(talks, args.now or datetime.now(), room=args.room)
        print(_fmt(talk) if talk else "No more talks today.")
    elif args.command == "conflicts":
        pairs = find_conflicts(talks)
        for a, b in pairs:
            print(f"{a.room}: '{a.title}' overlaps '{b.title}'")
        if not pairs:
            print("No conflicts.")
    return 0
