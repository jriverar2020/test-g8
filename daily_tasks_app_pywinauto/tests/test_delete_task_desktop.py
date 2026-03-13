from __future__ import annotations


def test_delete_task_removes_record(desktop_app, read_tasks):
    desktop_app.create_task(
        title="Eliminarme",
        description="Prueba de borrado",
        due_date="2026-03-25",
        priority_steps=2,
    )

    desktop_app.delete_selected_task()

    assert read_tasks() == []
