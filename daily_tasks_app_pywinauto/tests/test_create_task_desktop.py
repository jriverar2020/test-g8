from __future__ import annotations

import time


def test_create_task_persists_data(desktop_app, read_tasks):
    desktop_app.create_task(
        title="Estudiar Pywinauto",
        description="Crear automatización desktop",
        due_date="2026-03-20",
        priority="Media",
        priority_steps=0,
    )

    time.sleep(2)

    tasks = read_tasks()

    assert len(tasks) == 1
    assert tasks[0]["title"] == "Estudiar Pywinauto"
    assert tasks[0]["description"] == "Crear automatización desktop"
    assert tasks[0]["due_date"] == "2026-03-20"
    assert tasks[0]["priority"] in ("Media", "Alta", "Baja")
    assert tasks[0]["status"] == "Pendiente"