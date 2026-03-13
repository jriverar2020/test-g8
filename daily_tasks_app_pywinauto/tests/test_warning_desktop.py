from __future__ import annotations

from pywinauto.keyboard import send_keys


def test_complete_without_selection_shows_warning(desktop_app, read_tasks):
    desktop_app.focus()
    send_keys("{TAB 6}")
    send_keys(" ")

    message = desktop_app.dismiss_warning_dialog()
    assert "Selecciona una tarea primero." in message
    assert read_tasks() == []
