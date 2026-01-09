# Convertify - Instrucciones de Uso del Ejecutable

## Uso Básico

### Opción 1: Usar el directorio actual (MÁS SIMPLE)

Simplemente coloca `convertify.exe` en la carpeta que contiene los archivos AVI y ejecútalo:

```bash
convertify.exe convert
```

El programa buscará automáticamente todos los archivos `.avi` en el directorio actual y los convertirá a `.mp4`.

### Opción 2: Especificar directorios personalizados

```bash
convertify.exe convert --dir "C:\Videos" --dir "D:\Peliculas"
```

### Opción 3: Usar archivo de configuración .env

1. Copia el archivo `.env.dist` a `.env` en la misma carpeta que el ejecutable
2. Edita `.env` y configura los directorios:
   ```env
   CONVERSION_DIRECTORIES=C:\Videos,D:\Peliculas
   ```
3. Ejecuta:
   ```bash
   convertify.exe convert
   ```

## Opciones Disponibles

### Mantener archivos originales

Por defecto, los archivos AVI se eliminan después de la conversión. Para mantenerlos:

```bash
convertify.exe convert --keep-source
```

### Sobrescribir archivos existentes

Por defecto, si ya existe un MP4, se omite. Para sobrescribir:

```bash
convertify.exe convert --overwrite
```

### Ver versión

```bash
convertify.exe version
```

### Ver ayuda

```bash
convertify.exe --help
convertify.exe convert --help
```

## Configuración Avanzada (archivo .env)

Crea un archivo `.env` junto al ejecutable con estas opciones:

```env
# Directorios a escanear (separados por comas)
# Dejar vacío para usar el directorio actual
CONVERSION_DIRECTORIES=

# Configuración de video
VIDEO_CODEC=libx264
AUDIO_CODEC=aac
PRESET=medium
CRF=23
AUDIO_BITRATE=128k
THREADS=0

# Comportamiento
REMOVE_SOURCE=true
SKIP_IF_EXISTS=true
MAX_RETRIES=3
RETRY_DELAY_SECONDS=1.0

# Rendimiento
MAX_WORKERS=4

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/convertify.log
LOG_ROTATION=10 MB
LOG_RETENTION=1 week
```

## Ejemplos de Uso

### Ejemplo 1: Convertir todos los AVI en la carpeta actual

```bash
# Coloca convertify.exe en la carpeta con videos
convertify.exe convert
```

### Ejemplo 2: Convertir y mantener originales

```bash
convertify.exe convert --keep-source
```

### Ejemplo 3: Convertir múltiples carpetas

```bash
convertify.exe convert --dir "C:\Videos\Vacaciones" --dir "C:\Videos\Familia"
```

### Ejemplo 4: Usar con archivo .bat para doble clic

Crea un archivo `convertir.bat` con:

```batch
@echo off
convertify.exe convert
pause
```

## Notas Importantes

- El ejecutable requiere ffmpeg (incluido con moviepy)
- Los archivos de log se guardan en `logs/convertify.log`
- La conversión puede tardar dependiendo del tamaño y cantidad de videos
- Se muestra una barra de progreso durante la conversión

## Solución de Problemas

### "No se encuentra ffmpeg"

El ejecutable incluye ffmpeg, pero si hay problemas, asegúrate de tener permisos de ejecución.

### "No se encontraron archivos AVI"

Verifica que:

- Estás en el directorio correcto
- Los archivos tienen extensión `.avi`
- No están en carpetas ocultas

### "Error de permisos"

Ejecuta como administrador si los archivos están en carpetas del sistema.
