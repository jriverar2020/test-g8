from __future__ import annotations


def test_invalid_date_shows_validation_dialog(desktop_app, read_tasks):
    desktop_app.create_task(
        title="Fecha inválida",
        description="Caso negativo",
        due_date="20/03/2026",
        priority_steps=1,
    )

    message = desktop_app.dismiss_error_dialog()
    assert "YYYY-MM-DD" in message
    assert read_tasks() == []
