from __future__ import annotations

from typing import List, Optional

from src.models.task import Task
from src.storage.json_storage import JsonStorage


class TaskManager:
    def __init__(self, storage: JsonStorage) -> None:
        self.storage = storage
        self._tasks: List[Task] = [Task.from_dict(item) for item in self.storage.load()]

    def list_tasks(self) -> List[Task]:
        return sorted(self._tasks, key=lambda task: (task.status == "Completada", task.due_date, task.priority))

    def add_task(self, title: str, description: str, due_date: str, priority: str) -> Task:
        new_task = Task(
            id=self._next_id(),
            title=title,
            description=description,
            due_date=due_date,
            priority=priority,
        )
        new_task.validate()
        self._tasks.append(new_task)
        self._persist()
        return new_task

    def update_task(
        self,
        task_id: int,
        title: str,
        description: str,
        due_date: str,
        priority: str,
        status: str,
    ) -> Task:
        task = self.find_task(task_id)
        if not task:
            raise ValueError("No se encontró la tarea indicada.")
        task.title = title
        task.description = description
        task.due_date = due_date
        task.priority = priority
        task.status = status
        task.validate()
        self._persist()
        return task

    def remove_task(self, task_id: int) -> None:
        task = self.find_task(task_id)
        if not task:
            raise ValueError("No se encontró la tarea indicada.")
        self._tasks.remove(task)
        self._persist()

    def mark_completed(self, task_id: int) -> Task:
        task = self.find_task(task_id)
        if not task:
            raise ValueError("No se encontró la tarea indicada.")
        task.status = "Completada"
        self._persist()
        return task

    def find_task(self, task_id: int) -> Optional[Task]:
        return next((task for task in self._tasks if task.id == task_id), None)

    def summary(self) -> dict[str, int]:
        return {
            "total": len(self._tasks),
            "pendientes": sum(1 for task in self._tasks if task.status == "Pendiente"),
            "en_progreso": sum(1 for task in self._tasks if task.status == "En progreso"),
            "completadas": sum(1 for task in self._tasks if task.status == "Completada"),
        }

    def _next_id(self) -> int:
        return max((task.id for task in self._tasks), default=0) + 1

    def _persist(self) -> None:
        self.storage.save([task.to_dict() for task in self._tasks])
