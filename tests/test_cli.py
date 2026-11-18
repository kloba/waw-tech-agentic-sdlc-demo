from agenda.cli import main


def test_cli_list_filters_by_room(capsys):
    assert main(["list", "--room", "Expo"]) == 0
    out = capsys.readouterr().out.splitlines()
    assert len(out) == 2
    assert all("Expo" in line for line in out)


def test_cli_next_with_fixed_time(capsys):
    assert main(["next", "--now", "2026-11-26T10:20", "--room", "Lab"]) == 0
    assert "Postgres for vector search" in capsys.readouterr().out


def test_cli_next_after_last_talk(capsys):
    assert main(["next", "--now", "2026-11-26T19:00"]) == 0
    assert "No more talks today." in capsys.readouterr().out
