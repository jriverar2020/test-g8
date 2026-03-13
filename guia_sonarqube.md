# Guía paso a paso: aplicar pruebas con SonarQube al Gestor de Tareas Diarias

## 1. Objetivo
Analizar la calidad estática del software para identificar bugs, code smells y posibles vulnerabilidades en el proyecto `daily_tasks_app`.

## 2. Qué vas a evaluar
SonarQube revisará principalmente:
- complejidad de métodos
- duplicación de código
- funciones muy largas
- posibles errores de validación
- mantenibilidad

## 3. Requisitos previos
- Java 17 instalado
- SonarQube Community Edition instalado localmente
- Sonar Scanner instalado y agregado al PATH
- Proyecto descargado y funcional

## 4. Levantar SonarQube localmente
1. Descarga SonarQube Community Edition.
2. Descomprime el archivo.
3. En Windows ejecuta `StartSonar.bat` dentro de `bin/windows-x86-64`.
4. En Linux ejecuta `./sonar.sh start` dentro de `bin/linux-x86-64`.
5. Abre `http://localhost:9000`.
6. Ingresa con `admin / admin` y cambia la contraseña si el sistema lo solicita.

## 5. Verificar la configuración del proyecto
En la raíz del proyecto ya existe el archivo `sonar-project.properties`.

Puntos importantes:
- `sonar.sources=src,app.py` indica qué código analizar.
- `sonar.tests=tests,assert_tests.py` indica dónde están las pruebas.
- `sonar.exclusions` evita analizar cachés y datos temporales.

## 6. Ejecutar el análisis
1. Abre una terminal en la raíz del proyecto.
2. Ejecuta:

```bash
sonar-scanner
```

## 7. Revisar resultados
1. Abre SonarQube en el navegador.
2. Busca el proyecto `Daily Tasks App`.
3. Revisa las pestañas:
   - Issues
   - Measures
   - Code
   - Activity

## 8. Qué observar en clase
### 8.1 Bugs
Errores potenciales en el código.

### 8.2 Code Smells
Secciones de código que funcionan, pero podrían mejorarse.

### 8.3 Maintainability
Calidad para facilitar cambios futuros.

### 8.4 Complexity
Cantidad de lógica acumulada en una función o clase.

## 9. Actividad sugerida
1. Ejecutar el análisis inicial.
2. Registrar al menos 5 hallazgos.
3. Elegir 2 hallazgos y corregirlos.
4. Ejecutar nuevamente `sonar-scanner`.
5. Comparar resultados antes y después.

## 10. Ejemplos de mejoras que puedes aplicar
- Extraer funciones si un método crece demasiado.
- Reemplazar cadenas repetidas por constantes.
- Agregar validaciones explícitas.
- Reducir bloques `if` anidados.
- Mejorar nombres de variables y métodos.

## 11. Evidencia esperada del estudiante
- Captura del tablero de SonarQube
- Lista de hallazgos detectados
- Código corregido
- Comparación antes/después
