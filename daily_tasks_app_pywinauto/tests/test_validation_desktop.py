from __future__ import annotations

import time


def test_invalid_date_shows_validation_dialog(desktop_app, read_tasks):
    desktop_app.create_task(
        title="Fecha inválida",
        description="Debe mostrar error",
        due_date="20/03/2026",
        priority="Media",
        priority_steps=0,
    )

    time.sleep(1.0)
    message = desktop_app.dismiss_error_dialog().lower()
    tasks = read_tasks()

    assert "fecha" in message or "yyyy-mm-dd" in message or "error" in message
    assert len(tasks) == 0