# Convertify - Project Context

## Descripción
Convertify es un script diseñado para correr en segundo plano en sistemas Windows (ejecutado por un servicio `.vbs`), monitoreando carpetas en red para buscar archivos de video `.avi` y envolverlos (stream copy) en un contenedor `.mp4`.

## Decisiones Técnicas Actuales
- **Sin CLI / UI:** El proyecto corre en modo silencioso (sin interacción por consola). La ejecución principal se hace desde `main.py` + `src/container.py`, con compatibilidad para `.vbs`.
- **Rutas de Red por IP (UNC):** Para evitar problemas en servicios (desautenticación o cambios de sesión), se usan rutas UNC directas con IP `192.168.1.200` (hardcodeadas en `main.py`).
- **Velocidad de Conversión:** La conversión usa stream copy (`codec="copy"` y audio `copy` por defecto), envolviendo AVI→MP4 sin recodificar.
- **Sin `.env` Files:** El diseño evita dependencia de `.env` para facilitar compilación con PyInstaller.
- **Arquitectura Limpia:** Arquitectura en capas (Domain, Application, Infrastructure) con DI desde `src/container.py`.

## Historial Reciente (Hito de Background Service)
- Se eliminaron las librerías `typer` y `rich`.
- Se removió código y vistas de UI que frenaban o hacían ruido para su uso desatendido.
- Se implementaron rutas de UNC `\\192.168.1.200\Team-design\...`.
- Se corrigió el uso de pydantic-settings para que ignore buscar `.env`.
- Limpieza general de scripts y directorios en desuso (`src/helpers`, `Captures`, `test_lab_dirs.py`, `.env`).

## Historial Reciente (Correcciones)
- Se ajustó/limpió logging y tests relacionados con Loguru para evitar problemas en Windows.
- Se mejoró la limpieza de handlers en tests para evitar bloqueos al borrar temporales.
- Se mantiene el pipeline: `pytest` pasa **36/36** con cobertura total ~**89%**.
- Se eliminó `stdout`/`print()` del repositorio de filesystem para mantener el concern en infraestructura:
  - `chore: remove stdout prints from FileSystemRepository` (último commit en el repo).
