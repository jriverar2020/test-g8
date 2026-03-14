from __future__ import annotations

import time


def test_mark_task_completed_updates_storage(desktop_app, read_tasks):
    desktop_app.create_task(
        title="Tarea por completar",
        description="Debe cambiar a completada",
        due_date="2026-03-21",
        priority="Media",
        priority_steps=0,
    )

    time.sleep(1.5)
    desktop_app.mark_completed()
    time.sleep(2)

    tasks = read_tasks()

    assert len(tasks) == 1
    assert tasks[0]["status"] in ("Completada", "Completado")