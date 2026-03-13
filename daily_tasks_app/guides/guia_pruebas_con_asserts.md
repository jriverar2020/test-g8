# Guía paso a paso: aplicar pruebas con `assert` puro al Gestor de Tareas Diarias

## 1. Objetivo
Validar el comportamiento del software usando `assert` nativo de Python, sin frameworks externos.

## 2. Archivo de trabajo
El proyecto incluye el archivo:
- `assert_tests.py`

Este archivo contiene funciones que ejecutan validaciones básicas del sistema.

## 3. Ejecutar las pruebas
Desde la raíz del proyecto:

```bash
python assert_tests.py
```

## 4. Qué hace cada prueba
### 4.1 `test_crear_tarea`
Valida que:
- una tarea se cree correctamente
- el estado inicial sea `Pendiente`

### 4.2 `test_resumen_tareas`
Valida que:
- el resumen refleje el total de tareas
- una tarea marcada como completada se cuente bien

### 4.3 `test_fecha_invalida`
Valida que:
- el sistema rechace fechas con formato incorrecto

## 5. Cómo funciona `assert`
Ejemplo simple:

```python
resultado = 2 + 2
assert resultado == 4
```

Si la condición es verdadera, no pasa nada.
Si es falsa, Python lanza un `AssertionError`.

## 6. Cómo crear una nueva prueba con assert
Ejemplo:

```python
from pathlib import Path
from src.services.task_manager import TaskManager
from src.storage.json_storage import JsonStorage

TEST_FILE = Path("data/assert_tmp.json")

if TEST_FILE.exists():
    TEST_FILE.unlink()

manager = TaskManager(JsonStorage(str(TEST_FILE)))
manager.add_task("Estudiar", "", "2026-03-30", "Alta")
summary = manager.summary()
assert summary["total"] == 1
```

## 7. Actividad sugerida
1. Ejecutar `assert_tests.py`.
2. Leer cada función de prueba.
3. Explicar qué comportamiento valida.
4. Agregar una nueva función con `assert`.
5. Modificar el código para provocar un fallo.
6. Ejecutar de nuevo y revisar el error.

## 8. Diferencia entre assert y pytest
### Assert puro
- simple
- rápido
- útil para aprendizaje inicial

### Pytest
- mejor reporte
- más opciones
- fixtures y utilidades avanzadas

## 9. Evidencia esperada del estudiante
- ejecución correcta de `assert_tests.py`
- una nueva prueba creada con `assert`
- breve explicación del caso validado
