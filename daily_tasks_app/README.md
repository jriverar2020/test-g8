# Gestor de Tareas Diarias

Aplicación de escritorio en Python (Tkinter) para registrar, actualizar, completar y eliminar tareas diarias.

## Ejecución

```bash
python -m venv venv
# Activar entorno virtual
pip install -r requirements.txt
python app.py
```

## Pruebas automatizadas con pytest

```bash
pytest --html=reports/pytest_report.html --self-contained-html
```

## Pruebas con assert puro

```bash
python assert_tests.py
```

## SonarQube

1. Instala SonarQube Community Edition y Sonar Scanner.
2. Inicia SonarQube localmente.
3. Ejecuta:

```bash
sonar-scanner
```
