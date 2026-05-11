import builtins

from src import main


def test_interactive_cli_runs_multiple_commands(monkeypatch, capsys):
    commands = iter([
        "help",
        "build",
        "print hello",
        "load",
        "find good friends",
        "exit",
    ])

    calls = []
    build_index = {"hello": {"u1": 1}}
    loaded_index = {"good": {"u2": 2}, "friends": {"u2": 3}}

    monkeypatch.setattr(builtins, "input", lambda prompt="": next(commands))
    monkeypatch.setattr(main, "cmd_build", lambda: calls.append(("build", None)) or build_index)
    monkeypatch.setattr(main, "cmd_load", lambda: calls.append(("load", None)) or loaded_index)
    monkeypatch.setattr(main, "cmd_print", lambda word, index: calls.append(("print", word, index)))
    monkeypatch.setattr(main, "cmd_find", lambda query, index: calls.append(("find", query, index)))

    main.main()

    output = capsys.readouterr().out

    assert "Search Engine Tool (interactive shell)" in output
    assert "Commands:" in output
    assert calls == [
        ("build", None),
        ("print", "hello", build_index),
        ("load", None),
        ("find", "good friends", loaded_index),
    ]