# Proyecto de pruebas desktop con Pywinauto para `daily_tasks_app`

Este proyecto automatiza la aplicación actual construida con **Tkinter** usando **Pywinauto**, que es la herramienta adecuada para una interfaz nativa de Windows. Aquí no se usa Selenium porque la aplicación no es web.

## 1. Qué incluye

- Automatización de la ventana principal de la app.
- Ejecución aislada contra una copia temporal del proyecto original.
- Casos de prueba con `pytest`.
- Validación de resultados leyendo el archivo `data/tasks.json` del entorno temporal.

## 2. Estructura

```text
project/
├── README.md
├── pytest.ini
├── requirements.txt
├── pages/
│   └── main_window.py
├── tests/
│   ├── conftest.py
│   ├── test_create_task_desktop.py
│   ├── test_validation_desktop.py
│   ├── test_complete_task_desktop.py
│   ├── test_delete_task_desktop.py
│   └── test_warning_desktop.py
└── utils/
    └── project_clone.py
```

## 3. Requisitos

- Windows 10 u 11
- Python 3.11+ preferiblemente
- La carpeta del proyecto original `daily_tasks_app` al mismo nivel que este proyecto de pruebas

Estructura esperada:

```text
workspace/
├── daily_tasks_app/
└── daily_tasks_app_pywinauto/
```

## 4. Instalación

### Crear entorno virtual

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

### Instalar dependencias

```powershell
pip install -r requirements.txt
```

## 5. Ejecución

```powershell
pytest
```

Para generar reporte HTML:

```powershell
pytest --html=reports/desktop_report.html --self-contained-html
```

## 6. Casos incluidos

1. Crear tarea y validar persistencia.
2. Mostrar error por fecha inválida.
3. Marcar una tarea como completada.
4. Eliminar una tarea.
5. Mostrar advertencia cuando no hay selección.

## 7. Cómo funciona la automatización

El archivo `pages/main_window.py` usa esta estrategia:

- Arranca la app con `pywinauto.Application`.
- Se conecta a la ventana `Gestor de Tareas Diarias`.
- Navega por el formulario con `TAB` y escribe usando `send_keys`.
- Para verificar los resultados, los tests leen el `tasks.json` de la copia temporal.

Esto hace que las pruebas no alteren los datos reales del proyecto.

## 8. Limitaciones reales

Tkinter no siempre expone controles tan cómodamente como WinForms o WPF. Por eso la automatización se apoya en navegación por teclado. En algunos equipos puede variar levemente el orden de foco o el comportamiento de los diálogos.

Si alguna prueba falla por diferencias del entorno, ajusta estos puntos:

- Cantidad de `TAB` usada en `pages/main_window.py`
- Tiempos de espera (`time.sleep`)
- Títulos de diálogos como `Validación`, `Selección` o `Confirmar`

## 9. Recomendación para calibración inicial

Antes de correr la suite completa:

1. Ejecuta la app manualmente.
2. Verifica que el foco inicial quede en el campo **Título**.
3. Confirma que con `TAB` se recorra el formulario en este orden:
   - Título
   - Descripción
   - Fecha
   - Prioridad
   - Estado
   - Guardar
   - Nueva tarea
   - Marcar completada
   - Eliminar
   - Tabla de tareas

Si eso cambia en tu Windows, ajusta el page object.

## 10. Guía de construcción del proyecto

### Paso 1. Crear el proyecto de automatización

```powershell
mkdir daily_tasks_app_pywinauto
cd daily_tasks_app_pywinauto
```

### Paso 2. Crear las carpetas

```powershell
mkdir pages, tests, utils
```

### Paso 3. Crear `requirements.txt`

```txt
pywinauto
pytest
pytest-html
psutil
```

### Paso 4. Crear `pytest.ini`

```ini
[pytest]
pythonpath = .
testpaths = tests
addopts = -v --tb=short
```

### Paso 5. Crear `utils/project_clone.py`

Este archivo hace una copia temporal del proyecto real para que las pruebas no modifiquen tus datos.

### Paso 6. Crear `pages/main_window.py`

Aquí va la lógica de automatización de la ventana principal:

- abrir la app
- escribir campos
- guardar
- abrir una tarea desde la tabla
- completar
- eliminar
- cerrar diálogos

### Paso 7. Crear `tests/conftest.py`

Aquí se definen los fixtures:

- `isolated_project`
- `desktop_app`
- `data_file`
- `read_tasks`

### Paso 8. Crear los tests

Empieza en este orden:

- `test_create_task_desktop.py`
- `test_validation_desktop.py`
- `test_complete_task_desktop.py`
- `test_delete_task_desktop.py`
- `test_warning_desktop.py`

### Paso 9. Ejecutar la suite

```powershell
pytest
```

### Paso 10. Ajustar si el foco cambia

Si el recorrido por `TAB` no coincide exactamente en tu equipo, modifica los bloques como:

```python
send_keys("{TAB 6}")
send_keys(" ")
```

## 11. Siguiente mejora recomendada

La evolución natural de este proyecto sería agregar:

- screenshots al fallar
- logs por caso
- un script `run_tests.bat`
- pruebas de edición de tarea
- soporte para `Inspect.exe` y localizadores más finos si tu Windows expone mejor los controles
