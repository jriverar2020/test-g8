from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk

from src.models.task import VALID_PRIORITIES, VALID_STATUSES
from src.services.task_manager import TaskManager


class MainWindow(ttk.Frame):
    def __init__(self, master: tk.Tk, task_manager: TaskManager) -> None:
        super().__init__(master, padding=16)
        self.master = master
        self.task_manager = task_manager
        self.selected_task_id: int | None = None
        self._build_ui()
        self._load_tasks()
        self._refresh_summary()

    def _build_ui(self) -> None:
        self.master.title("Gestor de Tareas Diarias")
        self.master.geometry("980x620")
        self.master.minsize(900, 560)
        self.pack(fill=tk.BOTH, expand=True)

        form_frame = ttk.LabelFrame(self, text="Formulario de tarea", padding=12)
        form_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 12))

        ttk.Label(form_frame, text="Título").grid(row=0, column=0, sticky="w")
        self.title_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.title_var, width=36).grid(row=1, column=0, sticky="ew", pady=(0, 8))

        ttk.Label(form_frame, text="Descripción").grid(row=2, column=0, sticky="w")
        self.description_text = tk.Text(form_frame, width=36, height=8)
        self.description_text.grid(row=3, column=0, sticky="ew", pady=(0, 8))

        ttk.Label(form_frame, text="Fecha límite (YYYY-MM-DD)").grid(row=4, column=0, sticky="w")
        self.due_date_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.due_date_var, width=36).grid(row=5, column=0, sticky="ew", pady=(0, 8))

        ttk.Label(form_frame, text="Prioridad").grid(row=6, column=0, sticky="w")
        self.priority_var = tk.StringVar(value="Media")
        ttk.Combobox(
            form_frame,
            textvariable=self.priority_var,
            values=sorted(VALID_PRIORITIES),
            state="readonly",
            width=33,
        ).grid(row=7, column=0, sticky="ew", pady=(0, 8))

        ttk.Label(form_frame, text="Estado").grid(row=8, column=0, sticky="w")
        self.status_var = tk.StringVar(value="Pendiente")
        ttk.Combobox(
            form_frame,
            textvariable=self.status_var,
            values=sorted(VALID_STATUSES),
            state="readonly",
            width=33,
        ).grid(row=9, column=0, sticky="ew", pady=(0, 12))

        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=10, column=0, sticky="ew")
        ttk.Button(button_frame, text="Guardar", command=self.save_task).pack(fill=tk.X, pady=2)
        ttk.Button(button_frame, text="Nueva tarea", command=self.clear_form).pack(fill=tk.X, pady=2)
        ttk.Button(button_frame, text="Marcar completada", command=self.complete_task).pack(fill=tk.X, pady=2)
        ttk.Button(button_frame, text="Eliminar", command=self.delete_task).pack(fill=tk.X, pady=2)

        table_frame = ttk.LabelFrame(self, text="Tareas registradas", padding=12)
        table_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.summary_var = tk.StringVar()
        ttk.Label(table_frame, textvariable=self.summary_var, font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(0, 10))

        columns = ("id", "title", "priority", "status", "due_date")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=18)
        for column, label, width in [
            ("id", "ID", 60),
            ("title", "Título", 260),
            ("priority", "Prioridad", 100),
            ("status", "Estado", 120),
            ("due_date", "Fecha", 120),
        ]:
            self.tree.heading(column, text=label)
            self.tree.column(column, width=width, anchor="center" if column != "title" else "w")
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.on_select_task)

    def _load_tasks(self) -> None:
        for row in self.tree.get_children():
            self.tree.delete(row)
        for task in self.task_manager.list_tasks():
            self.tree.insert("", tk.END, iid=str(task.id), values=(task.id, task.title, task.priority, task.status, task.due_date))

    def _refresh_summary(self) -> None:
        summary = self.task_manager.summary()
        self.summary_var.set(
            f"Total: {summary['total']} | Pendientes: {summary['pendientes']} | En progreso: {summary['en_progreso']} | Completadas: {summary['completadas']}"
        )

    def save_task(self) -> None:
        try:
            if self.selected_task_id is None:
                self.task_manager.add_task(
                    self.title_var.get(),
                    self.description_text.get("1.0", tk.END).strip(),
                    self.due_date_var.get(),
                    self.priority_var.get(),
                )
            else:
                self.task_manager.update_task(
                    self.selected_task_id,
                    self.title_var.get(),
                    self.description_text.get("1.0", tk.END).strip(),
                    self.due_date_var.get(),
                    self.priority_var.get(),
                    self.status_var.get(),
                )
            self.clear_form()
            self._load_tasks()
            self._refresh_summary()
        except ValueError as error:
            messagebox.showerror("Validación", str(error))

    def clear_form(self) -> None:
        self.selected_task_id = None
        self.title_var.set("")
        self.description_text.delete("1.0", tk.END)
        self.due_date_var.set("")
        self.priority_var.set("Media")
        self.status_var.set("Pendiente")
        self.tree.selection_remove(*self.tree.selection())

    def complete_task(self) -> None:
        if self.selected_task_id is None:
            messagebox.showwarning("Selección", "Selecciona una tarea primero.")
            return
        self.task_manager.mark_completed(self.selected_task_id)
        self._load_tasks()
        self._refresh_summary()
        self.status_var.set("Completada")

    def delete_task(self) -> None:
        if self.selected_task_id is None:
            messagebox.showwarning("Selección", "Selecciona una tarea primero.")
            return
        if not messagebox.askyesno("Confirmar", "¿Deseas eliminar la tarea seleccionada?"):
            return
        self.task_manager.remove_task(self.selected_task_id)
        self.clear_form()
        self._load_tasks()
        self._refresh_summary()

    def on_select_task(self, _event: tk.Event) -> None:
        selected = self.tree.selection()
        if not selected:
            return
        task_id = int(selected[0])
        task = self.task_manager.find_task(task_id)
        if not task:
            return
        self.selected_task_id = task.id
        self.title_var.set(task.title)
        self.description_text.delete("1.0", tk.END)
        self.description_text.insert("1.0", task.description)
        self.due_date_var.set(task.due_date)
        self.priority_var.set(task.priority)
        self.status_var.set(task.status)
