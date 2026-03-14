# 🧪 Automatización Desktop - Gestor de Tareas Diarias

Este proyecto implementa pruebas automatizadas de tipo **End-to-End (E2E)** para una aplicación de escritorio desarrollada en Python (Tkinter), utilizando:

- 🧪 **Pytest** → framework de pruebas  
- 🖥️ **Pywinauto** → automatización de interfaces Windows  
- 🧩 **Page Object Model (POM)** → organización escalable de pruebas  

---

## 🎯 Objetivo

Validar el comportamiento funcional de la aplicación **Gestor de Tareas Diarias**, incluyendo:

- Creación de tareas
- Persistencia en archivo JSON
- Marcado como completadas
- Eliminación de tareas
- Validaciones de entrada
- Manejo de advertencias

---

## 🧱 Estructura del Proyecto

```
daily_tasks_app_pywinauto/
├── pages/
│   └── main_window.py
├── tests/
│   ├── conftest.py
│   ├── test_create_task_desktop.py
│   ├── test_complete_task_desktop.py
│   ├── test_delete_task_desktop.py
│   ├── test_validation_desktop.py
│   └── test_warning_desktop.py
├── pytest.ini
├── requirements.txt
└── README.md
```

---

## ⚙️ Requisitos

- Windows 10 o Windows 11
- Python 3.10 o superior
- Aplicación base (`daily_tasks_app`) disponible localmente

---

## 📦 Instalación

```bash
git clone <repo>
cd daily_tasks_app_pywinauto
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

---

## ▶️ Ejecución

```bash
python -m pytest -v
```

---

## 🧪 Pruebas incluidas

- Crear tarea
- Completar tarea
- Eliminar tarea
- Validación de fecha
- Advertencias de selección

---

## 📌 Notas técnicas

- `CTRL + TAB` para salir del campo descripción  
- `SPACE` para activar botones  
- Uso de backend `uia` en pywinauto  

---

## 🚀 Futuro

- Reportes HTML
- CI/CD
- Screenshots automáticos

---

## 👨‍💻 Autor

Proyecto académico de automatización de pruebas desktop
