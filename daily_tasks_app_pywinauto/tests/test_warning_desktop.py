from __future__ import annotations

import time


def test_complete_without_selection_shows_warning(desktop_app, read_tasks):
    time.sleep(1.0)
    desktop_app.mark_completed()
    time.sleep(1.0)

    message = desktop_app.dismiss_warning_dialog().lower()
    tasks = read_tasks()

    assert "seleccione" in message or "selecciona" in message or "advertencia" in message or "warning" in message
    assert len(tasks) == 0