from __future__ import annotations

import json
from pathlib import Path
from typing import Any, List


class JsonStorage:
    def __init__(self, file_path: str) -> None:
        self.file_path = Path(file_path)
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

    def load(self) -> List[dict[str, Any]]:
        if not self.file_path.exists():
            return []
        with self.file_path.open("r", encoding="utf-8") as file:
            return json.load(file)

    def save(self, items: List[dict[str, Any]]) -> None:
        with self.file_path.open("w", encoding="utf-8") as file:
            json.dump(items, file, ensure_ascii=False, indent=2)
