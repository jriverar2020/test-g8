from pathlib import Path

from src.services.task_manager import TaskManager
from src.storage.json_storage import JsonStorage


def build_manager(tmp_path: Path) -> TaskManager:
    return TaskManager(JsonStorage(str(tmp_path / "tasks.json")))


def test_add_task_creates_task(tmp_path: Path) -> None:
    manager = build_manager(tmp_path)

    created = manager.add_task("Estudiar", "Repasar pruebas", "2026-03-20", "Alta")

    assert created.id == 1
    assert created.title == "Estudiar"
    assert len(manager.list_tasks()) == 1


def test_mark_completed_changes_status(tmp_path: Path) -> None:
    manager = build_manager(tmp_path)
    task = manager.add_task("Leer", "Capítulo 2", "2026-03-21", "Media")

    updated = manager.mark_completed(task.id)

    assert updated.status == "Completada"


def test_update_task_validates_due_date(tmp_path: Path) -> None:
    manager = build_manager(tmp_path)
    task = manager.add_task("Comprar", "Mercado", "2026-03-19", "Baja")

    try:
        manager.update_task(task.id, "Comprar", "Mercado", "19/03/2026", "Baja", "Pendiente")
        raised = False
    except ValueError:
        raised = True

    assert raised is True


def test_remove_task_deletes_record(tmp_path: Path) -> None:
    manager = build_manager(tmp_path)
    task = manager.add_task("Llamar", "Cliente", "2026-03-18", "Media")

    manager.remove_task(task.id)

    assert manager.list_tasks() == []
