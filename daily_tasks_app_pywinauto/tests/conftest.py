from __future__ import annotations

import json
import shutil
from pathlib import Path

import pytest

from pages.main_window import MainWindowPage
from utils.project_clone import clone_project


@pytest.fixture(scope="session")
def original_project_path() -> Path:
    return Path(__file__).resolve().parents[2] / "daily_tasks_app"


@pytest.fixture()
def isolated_project(tmp_path: Path, original_project_path: Path) -> Path:
    destination = tmp_path / "daily_tasks_app_test_instance"
    return clone_project(original_project_path, destination)


@pytest.fixture()
def desktop_app(isolated_project: Path):
    page = MainWindowPage(project_root=isolated_project)
    page.start()
    page.wait_until_ready()
    yield page
    page.stop()


@pytest.fixture()
def data_file(isolated_project: Path) -> Path:
    return isolated_project / "data" / "tasks.json"


@pytest.fixture()
def read_tasks(data_file: Path):
    def _reader() -> list[dict]:
        if not data_file.exists():
            return []
        with data_file.open("r", encoding="utf-8") as file:
            return json.load(file)
    return _reader
