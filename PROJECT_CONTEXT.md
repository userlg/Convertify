# Convertify - Project Context

## Descripción
Convertify es un script diseñado para correr en segundo plano en sistemas Windows (ejecutado por un servicio `.vbs`), monitoreando carpetas en red para buscar archivos de video `.avi` y envolverlos (stream copy) en un contenedor `.mp4`.

## Decisiones Técnicas Actuales
- **Sin CLI / UI:** El proyecto operaba originalmente con `typer` y `rich` para mostrar progreso. Todo eso ha sido retirado. Ahora el script procesa de manera silenciosa, utilizando `argparse` para retrocompatibilidad con la flag `--lab`.
- **Rutas de Red por IP (UNC):** Para evitar los problemas de desconexión o desautenticación de unidades mapeadas (`Z:\`) cuando corre como un proceso de fondo en Windows, el script utiliza estrictamente rutas UNC directas con la IP `192.168.1.200`.
- **Velocidad de Conversión:** Para evitar cuellos de botella de recodificación (que antes usaban `libx264` con preset `ultrafast`), el convertidor ahora está instruido a usar el codec de video y audio `copy`. Esto hace que el proceso sea instantáneo y no consuma ciclos pesados de CPU, simplemente envolviendo las pistas existentes del AVI al MP4.
- **Sin `.env` Files:** Para evitar errores al ser compilado mediante PyInstaller a un archivo `.exe`, se ha retirado el uso obligatorio o dependencia de un archivo `.env`.
- **Arquitectura Limpia:** La aplicación utiliza arquitectura en capas (Domain, Application, Infrastructure). Todo el código "helper" que no pertenecía ha sido limpiado y deprecado.

## Historial Reciente (Hito de Background Service)
- Se eliminaron las librerías `typer` y `rich`.
- Se removió código y vistas de UI que frenaban o hacían ruido para su uso desatendido.
- Se implementaron rutas de UNC `\\192.168.1.200\Team-design\...`.
- Se corrigió el uso de pydantic-settings para que ignore buscar `.env`.
- Limpieza general de scripts y directorios en desuso (`src/helpers`, `Captures`, `test_lab_dirs.py`, `.env`).

## Historial Reciente (Correcciones 2026-07-06)
- Se corrigió `Container.convert_videos_use_case` que referenciaba `self.settings.max_workers` (atributo eliminado con pydantic-settings). Ahora usa valor fijo `4`.
- Se corrigieron tests del logger que referenciaban `logger.logger` en lugar de `logger._logger`.
- Se añadió limpieza de handlers de loguru en test para evitar `PermissionError` en Windows al borrar temp dirs con archivos abiertos.
- 36/36 tests passing.
