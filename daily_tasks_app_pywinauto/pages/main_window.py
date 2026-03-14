from __future__ import annotations

import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Optional

from pywinauto import Desktop
from pywinauto.keyboard import send_keys


class MainWindowPage:
    WINDOW_TITLE_RE = r".*Gestor de Tareas Diarias.*"

    def __init__(self, project_root: Path, python_executable: Optional[str] = None) -> None:
        self.project_root = Path(project_root)
        self.python_executable = python_executable or sys.executable
        self.proc: Optional[subprocess.Popen] = None
        self.window = None

    def start(self) -> "MainWindowPage":
        app_path = self.project_root / "app.py"

        if not app_path.exists():
            raise FileNotFoundError(
                f"No se encontró app.py en: {app_path}\n"
                "Ajusta la fixture original_project_path en tests/conftest.py."
            )

        self.proc = subprocess.Popen(
            [self.python_executable, str(app_path)],
            cwd=str(self.project_root),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        deadline = time.time() + 20
        last_error = None

        while time.time() < deadline:
            if self.proc.poll() is not None:
                stdout, stderr = self.proc.communicate()
                raise RuntimeError(
                    "La aplicación se cerró antes de mostrar la ventana.\n\n"
                    f"STDOUT:\n{stdout or '(vacío)'}\n\n"
                    f"STDERR:\n{stderr or '(vacío)'}"
                )

            try:
                self.window = Desktop(backend="uia").window(title_re=self.WINDOW_TITLE_RE)
                self.window.wait("visible", timeout=2)
                self.window.set_focus()
                time.sleep(1.0)
                return self
            except Exception as exc:
                last_error = exc
                time.sleep(0.5)

        raise RuntimeError(
            "No se encontró la ventana principal.\n"
            f"Patrón buscado: {self.WINDOW_TITLE_RE}\n"
            f"Último error: {last_error}"
        )

    def stop(self) -> None:
        try:
            if self.window is not None:
                self.window.close()
                time.sleep(0.5)
        except Exception:
            pass

        try:
            if self.proc and self.proc.poll() is None:
                self.proc.terminate()
                time.sleep(0.5)
        except Exception:
            pass

    def wait_until_ready(self) -> None:
        if self.window is None:
            raise RuntimeError("La ventana no está inicializada.")
        self.window.wait("visible", timeout=10)
        self.window.set_focus()
        time.sleep(0.5)

    def focus(self) -> None:
        if self.window is None:
            raise RuntimeError("La aplicación no está iniciada.")
        self.window.set_focus()
        time.sleep(0.4)

    def debug_identifiers(self) -> None:
        if self.window is None:
            raise RuntimeError("La ventana no está inicializada.")
        self.window.print_control_identifiers()

    def get_all_window_text(self) -> str:
        if self.window is None:
            return ""
        try:
            texts = self.window.texts()
            return " | ".join(t.strip() for t in texts if t and t.strip())
        except Exception:
            return ""

    def _click_button(self, title: str) -> bool:
        if self.window is None:
            return False

        candidates = [
            {"title": title, "control_type": "Button"},
            {"title_re": f".*{title}.*", "control_type": "Button"},
        ]

        for kwargs in candidates:
            try:
                btn = self.window.child_window(**kwargs)
                btn.wait("enabled visible", timeout=2)
                btn.click_input()
                time.sleep(1.0)
                return True
            except Exception:
                continue

        return False

    def create_task(
        self,
        title: str,
        description: str,
        due_date: str,
        priority: str = "Media",
        priority_steps: int = 0
    ) -> None:
        """
        Flujo ajustado a la UI actual de Tkinter:
        Título -> Descripción -> Ctrl+Tab -> Fecha -> Prioridad -> Estado -> Guardar
        """
        self.focus()

        # Ir a Título
        send_keys("{TAB}")
        time.sleep(0.2)

        # Título
        send_keys("^a{BACKSPACE}")
        send_keys(title, with_spaces=True)
        time.sleep(0.2)

        # Descripción
        send_keys("{TAB}")
        time.sleep(0.2)
        send_keys("^a{BACKSPACE}")
        send_keys(description, with_spaces=True)
        time.sleep(0.2)

        # Salir del Text de descripción
        send_keys("^({TAB})")
        time.sleep(0.3)

        # Fecha
        send_keys("^a{BACKSPACE}")
        send_keys(due_date, with_spaces=True)
        time.sleep(0.2)

        # Prioridad
        send_keys("{TAB}")
        time.sleep(0.2)

        priority_normalized = priority.strip().lower()

        if priority_steps > 0:
            for _ in range(priority_steps):
                send_keys("{DOWN}")
                time.sleep(0.1)
        else:
            # En la app actual el valor por defecto suele ser "Media"
            if priority_normalized == "alta":
                send_keys("{HOME}")
            elif priority_normalized == "media":
                pass
            elif priority_normalized == "baja":
                send_keys("{DOWN}")

        time.sleep(0.2)

        # Estado
        send_keys("{TAB}")
        time.sleep(0.2)

        # Intentar click directo en Guardar
        if self._click_button("Guardar"):
            return

        # Respaldo por teclado
        send_keys("{TAB}")
        time.sleep(0.2)
        send_keys("{SPACE}")
        time.sleep(1.2)

    def mark_completed(self) -> None:
        self.focus()

        if self._click_button("Marcar Completada"):
            return

        if self._click_button("Marcar completada"):
            return

        # Respaldo por teclado
        send_keys("{TAB 3}")
        time.sleep(0.3)
        send_keys("{SPACE}")
        time.sleep(1.0)

    def delete_task(self) -> None:
        self.focus()

        if self._click_button("Eliminar"):
            return

        # Respaldo por teclado
        send_keys("{TAB 4}")
        time.sleep(0.3)
        send_keys("{SPACE}")
        time.sleep(1.0)

    def _collect_dialog_text_and_close(self, keywords: tuple[str, ...]) -> str:
        time.sleep(0.8)

        try:
            windows = Desktop(backend="uia").windows()
        except Exception:
            return ""

        for win in windows:
            try:
                if self.window is not None and win.handle == self.window.handle:
                    continue

                if not win.is_visible():
                    continue

                title = (win.window_text() or "").strip().lower()
                text = self._safe_collect_text(win).strip()
                haystack = f"{title} {text}".lower()

                if any(keyword in haystack for keyword in keywords):
                    try:
                        win.set_focus()
                        time.sleep(0.2)
                        send_keys("{ENTER}")
                    except Exception:
                        pass
                    return text or title
            except Exception:
                continue

        # Si no encontró por keyword, intenta cerrar cualquier diálogo visible distinto a la principal
        for win in windows:
            try:
                if self.window is not None and win.handle == self.window.handle:
                    continue

                if not win.is_visible():
                    continue

                text = self._safe_collect_text(win).strip()
                try:
                    win.set_focus()
                    time.sleep(0.2)
                    send_keys("{ENTER}")
                except Exception:
                    pass
                return text
            except Exception:
                continue

        return ""

    def dismiss_warning_dialog(self) -> str:
        return self._collect_dialog_text_and_close(
            ("advertencia", "warning", "seleccione", "selecciona")
        )

    def dismiss_error_dialog(self) -> str:
        return self._collect_dialog_text_and_close(
            ("error", "fecha", "yyyy-mm-dd", "validación", "validation")
        )

    def _safe_collect_text(self, win) -> str:
        try:
            texts = win.texts()
            cleaned = [t.strip() for t in texts if t and t.strip()]
            return " ".join(cleaned)
        except Exception:
            return ""

    def find_tasks_file(self) -> Path:
        candidates = [
            self.project_root / "data" / "tasks.json",
            self.project_root / "tasks.json",
            self.project_root / "src" / "data" / "tasks.json",
        ]

        for candidate in candidates:
            if candidate.exists():
                return candidate

        return self.project_root / "data" / "tasks.json"

    def read_tasks_from_disk(self) -> list[dict]:
        json_file = self.find_tasks_file()

        if not json_file.exists():
            return []

        content = json_file.read_text(encoding="utf-8").strip()
        if not content:
            return []

        data = json.loads(content)
        if isinstance(data, dict) and "tasks" in data:
            return data["tasks"]
        if isinstance(data, list):
            return data
        return []