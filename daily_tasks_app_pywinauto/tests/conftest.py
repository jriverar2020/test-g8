from __future__ import annotations

import json
import shutil
import time
from pathlib import Path

import pytest

from pages.main_window import MainWindowPage


@pytest.fixture(scope="session")
def original_project_path() -> Path:
    """
    Ajusta esta ruta si tu proyecto original no está al mismo nivel.
    Estructura esperada:
    D:\
    ├── daily_tasks_app
    └── daily_tasks_app_pywinauto
    """
    return Path(__file__).resolve().parents[2] / "daily_tasks_app"


@pytest.fixture
def isolated_project(tmp_path: Path, original_project_path: Path) -> Path:
    destination = tmp_path / "daily_tasks_app_test_instance"
    shutil.copytree(original_project_path, destination)

    # Intentar dejar el JSON limpio
    possible_jsons = [
        destination / "data" / "tasks.json",
        destination / "tasks.json",
        destination / "src" / "data" / "tasks.json",
    ]

    created_any = False
    for json_file in possible_jsons:
        try:
            json_file.parent.mkdir(parents=True, exist_ok=True)
            json_file.write_text("[]", encoding="utf-8")
            created_any = True
        except Exception:
            continue

    if not created_any:
        raise RuntimeError("No fue posible preparar un tasks.json inicial en el proyecto aislado.")

    return destination


@pytest.fixture
def desktop_app(isolated_project: Path):
    page = MainWindowPage(isolated_project)
    page.start()
    page.wait_until_ready()
    yield page
    page.stop()


@pytest.fixture
def data_file(isolated_project: Path) -> Path:
    candidates = [
        isolated_project / "data" / "tasks.json",
        isolated_project / "tasks.json",
        isolated_project / "src" / "data" / "tasks.json",
    ]

    for candidate in candidates:
        if candidate.exists():
            return candidate

    return isolated_project / "data" / "tasks.json"


@pytest.fixture
def read_tasks(data_file: Path):
    def _read() -> list[dict]:
        if not data_file.exists():
            return []

        content = data_file.read_text(encoding="utf-8").strip()
        if not content:
            return []

        data = json.loads(content)
        if isinstance(data, dict) and "tasks" in data:
            return data["tasks"]
        if isinstance(data, list):
            return data
        return []

    return _read