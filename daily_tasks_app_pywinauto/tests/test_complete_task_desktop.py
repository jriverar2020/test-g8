from __future__ import annotations


def test_mark_task_completed_updates_storage(desktop_app, read_tasks):
    desktop_app.create_task(
        title="Cerrar actividad",
        description="Pendiente por completar",
        due_date="2026-03-22",
        priority_steps=1,
    )

    desktop_app.mark_selected_task_completed()

    tasks = read_tasks()
    assert len(tasks) == 1
    assert tasks[0]["status"] == "Completada"
