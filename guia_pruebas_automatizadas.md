# Guía paso a paso: pruebas automatizadas con pytest sobre el Gestor de Tareas Diarias

## 1. Objetivo
Automatizar la validación de la lógica de negocio del software usando `pytest`.

## 2. Qué se va a probar
Las pruebas del proyecto verifican:
- creación de tareas
- actualización de tareas
- cambio de estado a completada
- eliminación de tareas
- validación de fechas

## 3. Instalar dependencias
Con el entorno virtual activo, ejecuta:

```bash
pip install -r requirements.txt
```

## 4. Estructura relevante
- `tests/test_task_manager_pytest.py`: archivo principal de pruebas automatizadas
- `src/services/task_manager.py`: lógica bajo prueba
- `src/models/task.py`: reglas de validación

## 5. Ejecutar pruebas básicas
Desde la raíz del proyecto:

```bash
pytest
```

## 6. Ejecutar con reporte HTML
```bash
pytest --html=reports/pytest_report.html --self-contained-html
```

## 7. Leer los resultados
### Si todo sale bien
Verás `PASSED` en cada caso.

### Si una prueba falla
Verás:
- nombre de la prueba
- línea del fallo
- diferencia entre resultado esperado y real

## 8. Explicación de las pruebas incluidas
### 8.1 `test_add_task_creates_task`
Verifica que al crear una tarea:
- se asigna id
- se guarda el título
- aparece en el listado

### 8.2 `test_mark_completed_changes_status`
Verifica que una tarea cambie correctamente a `Completada`.

### 8.3 `test_update_task_validates_due_date`
Comprueba que una fecha con formato incorrecto lance error.

### 8.4 `test_remove_task_deletes_record`
Confirma que una tarea eliminada desaparezca del sistema.

## 9. Cómo construir una nueva prueba
Ejemplo:

```python
from pathlib import Path
from src.services.task_manager import TaskManager
from src.storage.json_storage import JsonStorage


def build_manager(tmp_path: Path) -> TaskManager:
    return TaskManager(JsonStorage(str(tmp_path / "tasks.json")))


def test_summary_counts_pending_tasks(tmp_path: Path):
    manager = build_manager(tmp_path)
    manager.add_task("Clase", "", "2026-03-25", "Alta")
    summary = manager.summary()
    assert summary["pendientes"] == 1
```

## 10. Actividad sugerida para clase
1. Ejecutar las pruebas existentes.
2. Identificar qué comportamiento valida cada prueba.
3. Agregar una nueva prueba propia.
4. Forzar un defecto en `TaskManager`.
5. Volver a ejecutar y observar qué prueba lo detecta.

## 11. Buenas prácticas
- Una prueba debe validar una sola idea.
- El nombre de la prueba debe describir claramente el comportamiento.
- Usa datos simples y controlados.
- Evita depender de archivos reales del usuario; usa rutas temporales.

## 12. Evidencia esperada del estudiante
- Captura del resultado de pytest
- Código de una nueva prueba añadida
- Explicación del comportamiento validado
