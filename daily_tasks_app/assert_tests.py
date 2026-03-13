"""Pruebas sencillas usando assert puro de Python.

Ejecución:
    python assert_tests.py
"""
from pathlib import Path

from src.services.task_manager import TaskManager
from src.storage.json_storage import JsonStorage


TEST_FILE = Path(__file__).resolve().parent / "data" / "assert_tasks.json"


def build_manager() -> TaskManager:
    if TEST_FILE.exists():
        TEST_FILE.unlink()
    return TaskManager(JsonStorage(str(TEST_FILE)))


def test_crear_tarea() -> None:
    manager = build_manager()
    task = manager.add_task("Preparar clase", "Slides y ejemplos", "2026-03-25", "Alta")
    assert task.title == "Preparar clase"
    assert task.status == "Pendiente"


def test_resumen_tareas() -> None:
    manager = build_manager()
    manager.add_task("Tarea 1", "", "2026-03-25", "Alta")
    task = manager.add_task("Tarea 2", "", "2026-03-26", "Media")
    manager.mark_completed(task.id)
    summary = manager.summary()
    assert summary["total"] == 2
    assert summary["completadas"] == 1


def test_fecha_invalida() -> None:
    manager = build_manager()
    try:
        manager.add_task("Fecha", "", "25-03-2026", "Alta")
        raised = False
    except ValueError:
        raised = True
    assert raised is True


if __name__ == "__main__":
    tests = [test_crear_tarea, test_resumen_tareas, test_fecha_invalida]
    for test in tests:
        test()
        print(f"[OK] {test.__name__}")
    print("Todas las pruebas con assert se ejecutaron correctamente.")
