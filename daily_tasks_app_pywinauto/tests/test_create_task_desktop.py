from __future__ import annotations


def test_create_task_persists_data(desktop_app, read_tasks):
    desktop_app.create_task(
        title="Estudiar Pywinauto",
        description="Crear automatización desktop",
        due_date="2026-03-20",
        priority_steps=0,
    )

    tasks = read_tasks()
    assert len(tasks) == 1
    assert tasks[0]["title"] == "Estudiar Pywinauto"
    assert tasks[0]["description"] == "Crear automatización desktop"
    assert tasks[0]["due_date"] == "2026-03-20"
    assert tasks[0]["priority"] == "Alta"
    assert tasks[0]["status"] == "Pendiente"
