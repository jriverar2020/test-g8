from __future__ import annotations

import time


def test_delete_task_removes_record(desktop_app, read_tasks):
    desktop_app.create_task(
        title="Tarea a eliminar",
        description="Será eliminada",
        due_date="2026-03-22",
        priority="Media",
        priority_steps=0,
    )

    time.sleep(1.5)
    desktop_app.delete_task()
    time.sleep(2)

    tasks = read_tasks()

    assert len(tasks) == 0