from datetime import datetime

from agenda import find_conflicts, next_talk, talks_in_room
from conftest import make_talk


def at(hhmm: str) -> datetime:
    return datetime.fromisoformat(f"2026-11-26T{hhmm}")


def test_load_agenda_sorts_by_start(talks):
    starts = [t.start for t in talks]
    assert starts == sorted(starts)
    assert len(talks) == 9


def test_talks_in_room_is_case_insensitive(talks):
    assert {t.id for t in talks_in_room(talks, "lab")} == {"t3", "t5", "t9"}


def test_next_talk_returns_first_upcoming(talks):
    talk = next_talk(talks, at("09:10"))
    assert talk is not None
    assert talk.start == at("09:30")


def test_next_talk_in_room(talks):
    talk = next_talk(talks, at("09:40"), room="Main")
    assert talk is not None
    assert talk.id == "t4"


def test_next_talk_returns_none_after_last_talk(talks):
    assert next_talk(talks, at("18:00")) is None


def test_find_conflicts_detects_overlap_in_same_room():
    a = make_talk("a", "Main", "10:00", "11:00")
    b = make_talk("b", "Main", "10:30", "11:30")
    assert find_conflicts([a, b]) == [(a, b)]


def test_find_conflicts_ignores_other_rooms():
    a = make_talk("a", "Main", "10:00", "11:00")
    b = make_talk("b", "Lab", "10:30", "11:30")
    assert find_conflicts([a, b]) == []
