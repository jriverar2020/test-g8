from __future__ import annotations

import shutil
from pathlib import Path


IGNORED_DIRS = {"venv", "__pycache__", ".pytest_cache", ".scannerwork", ".git", ".idea", ".vscode"}
IGNORED_FILES = {"tasks.json"}


def clone_project(source_root: Path, destination_root: Path) -> Path:
    if destination_root.exists():
        shutil.rmtree(destination_root)

    def _ignore(_dir: str, names: list[str]) -> set[str]:
        ignored: set[str] = set()
        for name in names:
            if name in IGNORED_DIRS or name in IGNORED_FILES:
                ignored.add(name)
        return ignored

    shutil.copytree(source_root, destination_root, ignore=_ignore)
    data_dir = destination_root / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    return destination_root
