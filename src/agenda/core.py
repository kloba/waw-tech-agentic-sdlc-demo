"""Load a conference agenda and answer simple questions about it."""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass(frozen=True)
class Talk:
    id: str
    title: str
    speaker: str
    room: str
    track: str
    start: datetime
    end: datetime


def load_agenda(path: str | Path) -> list[Talk]:
    """Read talks from a JSON file and return them sorted by start time."""
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    talks = [
        Talk(
            id=item["id"],
            title=item["title"],
            speaker=item["speaker"],
            room=item["room"],
            track=item["track"],
            start=datetime.fromisoformat(item["start"]),
            end=datetime.fromisoformat(item["end"]),
        )
        for item in raw["talks"]
    ]
    return sorted(talks, key=lambda t: (t.start, t.room))


def talks_in_room(talks: list[Talk], room: str) -> list[Talk]:
    """Return the talks held in ``room`` (case-insensitive)."""
    return [t for t in talks if t.room.lower() == room.lower()]


def next_talk(talks: list[Talk], now: datetime, room: str | None = None) -> Talk | None:
    """Return the next talk that has not started yet, optionally in one room.

    A talk that starts exactly at ``now`` counts as the next talk.
    """
    candidates = talks_in_room(talks, room) if room else talks
    upcoming = [t for t in candidates if t.start > now]
    return min(upcoming, key=lambda t: t.start, default=None)


def find_conflicts(talks: list[Talk]) -> list[tuple[Talk, Talk]]:
    """Return pairs of talks that overlap in the same room."""
    conflicts = []
    for i, a in enumerate(talks):
        for b in talks[i + 1 :]:
            if a.room == b.room and a.start <= b.end and b.start <= a.end:
                conflicts.append((a, b))
    return conflicts
