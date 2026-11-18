from datetime import datetime
from pathlib import Path

import pytest

from agenda import Talk, load_agenda

DATA = Path(__file__).resolve().parents[1] / "data" / "agenda.json"


@pytest.fixture
def talks() -> list[Talk]:
    return load_agenda(DATA)


def make_talk(id: str, room: str, start: str, end: str, track: str = "AI") -> Talk:
    return Talk(
        id=id,
        title=f"Talk {id}",
        speaker="Test Speaker",
        room=room,
        track=track,
        start=datetime.fromisoformat(f"2026-11-26T{start}"),
        end=datetime.fromisoformat(f"2026-11-26T{end}"),
    )
