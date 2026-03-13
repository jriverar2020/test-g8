from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import date
from typing import Any, Dict


VALID_PRIORITIES = {"Alta", "Media", "Baja"}
VALID_STATUSES = {"Pendiente", "En progreso", "Completada"}


@dataclass
class Task:
    id: int
    title: str
    description: str
    due_date: str
    priority: str = "Media"
    status: str = "Pendiente"

    def validate(self) -> None:
        if not self.title.strip():
            raise ValueError("El título es obligatorio.")
        if self.priority not in VALID_PRIORITIES:
            raise ValueError(f"Prioridad inválida: {self.priority}")
        if self.status not in VALID_STATUSES:
            raise ValueError(f"Estado inválido: {self.status}")
        try:
            date.fromisoformat(self.due_date)
        except ValueError as exc:
            raise ValueError("La fecha debe tener el formato YYYY-MM-DD.") from exc

    def to_dict(self) -> Dict[str, Any]:
        self.validate()
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Task":
        task = cls(
            id=int(data["id"]),
            title=str(data["title"]),
            description=str(data.get("description", "")),
            due_date=str(data["due_date"]),
            priority=str(data.get("priority", "Media")),
            status=str(data.get("status", "Pendiente")),
        )
        task.validate()
        return task
