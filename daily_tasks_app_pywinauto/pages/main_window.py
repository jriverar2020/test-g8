from __future__ import annotations

import time
from pathlib import Path
from typing import Optional

from pywinauto import Application, Desktop
from pywinauto.findwindows import ElementNotFoundError
from pywinauto.keyboard import send_keys
from pywinauto.timings import TimeoutError as PywinautoTimeoutError


class MainWindowPage:
    """
    Automatiza la ventana principal de la app Tkinter.

    Estrategia:
    1. Conectarse a la ventana por título.
    2. Usar el foco inicial y navegación por TAB, que en esta UI es estable.
    3. Verificar efectos persistidos leyendo data/tasks.json del clon temporal.

    Esta aproximación evita depender por completo de identificadores internos de Tkinter,
    que pueden variar entre equipos o versiones de Windows.
    """

    WINDOW_TITLE = "Gestor de Tareas Diarias"

    def __init__(self, project_root: Path, python_executable: str = "python") -> None:
        self.project_root = Path(project_root)
        self.python_executable = python_executable
        self.app: Optional[Application] = None
        self.window = None

    def start(self) -> "MainWindowPage":
        cmd = f'"{self.python_executable}" app.py'
        self.app = Application(backend="win32").start(cmd_line=cmd, cwd=str(self.project_root))
        self.window = self.app.window(title=self.WINDOW_TITLE)
        self.window.wait("visible", timeout=15)
        self.window.set_focus()
        time.sleep(0.8)
        return self

    def connect_existing(self) -> "MainWindowPage":
        self.app = Application(backend="win32").connect(title=self.WINDOW_TITLE)
        self.window = self.app.window(title=self.WINDOW_TITLE)
        self.window.wait("visible", timeout=15)
        return self

    def stop(self) -> None:
        if self.window is not None:
            try:
                self.window.close()
                time.sleep(0.5)
            except Exception:
                pass

    def focus(self) -> None:
        if self.window is None:
            raise RuntimeError("La aplicación no está iniciada.")
        self.window.set_focus()
        time.sleep(0.2)

    def reset_form(self) -> None:
        self.focus()
        # Título -> descripción -> fecha -> prioridad -> estado -> botones
        # Botón "Nueva tarea" queda después de Guardar.
        send_keys("^a{BACKSPACE}")
        send_keys("{TAB}")
        send_keys("^a{BACKSPACE}")
        send_keys("{TAB}")
        send_keys("^a{BACKSPACE}")
        send_keys("{TAB}")
        send_keys("{DOWN}")
        send_keys("{TAB}")
        send_keys("{DOWN}")
        send_keys("{TAB}")  # Guardar
        send_keys("{TAB}")  # Nueva tarea
        send_keys(" ")
        time.sleep(0.4)

    def create_task(self, title: str, description: str, due_date: str, priority_steps: int = 1) -> None:
        """
        priority_steps:
        0 = Alta, 1 = Media, 2 = Baja (orden alfabético esperado del Combobox)
        """
        self.focus()
        send_keys("^a{BACKSPACE}")
        send_keys(title, with_spaces=True)
        send_keys("{TAB}")
        send_keys("^a{BACKSPACE}")
        send_keys(description, with_spaces=True)
        send_keys("{TAB}")
        send_keys("^a{BACKSPACE}")
        send_keys(due_date)
        send_keys("{TAB}")
        for _ in range(priority_steps):
            send_keys("{DOWN}")
        send_keys("{TAB}")  # estado
        send_keys("{TAB}")  # guardar
        send_keys(" ")
        time.sleep(0.8)

    def save_current_form(self) -> None:
        self.focus()
        send_keys("{TAB 5}")
        send_keys(" ")
        time.sleep(0.6)

    def open_first_task_from_table(self) -> None:
        self.focus()
        # Desde el foco inicial del formulario: 4 TAB a botones, 4 más hasta la tabla.
        send_keys("{TAB 9}")
        send_keys("{DOWN}")
        send_keys("{ENTER}")
        time.sleep(0.8)

    def mark_selected_task_completed(self) -> None:
        self.open_first_task_from_table()
        # Con la tarea cargada en el formulario, el botón "Marcar completada" queda tras dos tabs desde Guardar.
        send_keys("{TAB 6}")
        send_keys(" ")
        time.sleep(0.8)

    def delete_selected_task(self) -> None:
        self.open_first_task_from_table()
        send_keys("{TAB 7}")
        send_keys(" ")
        time.sleep(0.5)
        send_keys("%y")
        time.sleep(0.8)

    def dismiss_error_dialog(self) -> str:
        dialog = Desktop(backend="win32").window(title="Validación")
        dialog.wait("visible", timeout=10)
        message = dialog.window_text()
        try:
            static = dialog.child_window(class_name="Static")
            extracted = static.window_text()
            if extracted:
                message = extracted
        except Exception:
            pass
        try:
            dialog.child_window(title="OK", class_name="Button").click()
        except Exception:
            send_keys("{ENTER}")
        time.sleep(0.5)
        return message

    def dismiss_warning_dialog(self) -> str:
        dialog = Desktop(backend="win32").window(title="Selección")
        dialog.wait("visible", timeout=10)
        message = dialog.window_text()
        try:
            static = dialog.child_window(class_name="Static")
            extracted = static.window_text()
            if extracted:
                message = extracted
        except Exception:
            pass
        send_keys("{ENTER}")
        time.sleep(0.5)
        return message

    def get_summary_text(self) -> str:
        self.focus()
        try:
            texts = self.window.texts()
            for text in texts:
                if text.startswith("Total:"):
                    return text
        except Exception:
            pass
        raise ElementNotFoundError("No fue posible leer el resumen de la ventana.")

    def wait_until_ready(self) -> None:
        self.focus()
        time.sleep(0.8)
