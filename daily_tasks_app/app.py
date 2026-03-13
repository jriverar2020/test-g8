from __future__ import annotations

import tkinter as tk
from pathlib import Path

from src.services.task_manager import TaskManager
from src.storage.json_storage import JsonStorage
from src.ui.main_window import MainWindow


BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "tasks.json"


def main() -> None:
    storage = JsonStorage(str(DATA_FILE))
    manager = TaskManager(storage)
    root = tk.Tk()
    MainWindow(root, manager)
    root.mainloop()


if __name__ == "__main__":
    main()
