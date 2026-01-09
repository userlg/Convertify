# Guía de Optimización de Velocidad - Convertify

## 🚀 Configuración Actual: MÁXIMA VELOCIDAD

Tu ejecutable ahora está configurado para **conversión ultra-rápida** con las siguientes optimizaciones:

### Configuración Aplicada

```env
PRESET=ultrafast          # 5-10x más rápido que "medium"
CRF=28                    # Calidad optimizada para velocidad
AUDIO_BITRATE=96k         # Audio comprimido eficientemente
```

### Mejoras Esperadas

| Métrica                  | Antes      | Ahora           | Mejora               |
| ------------------------ | ---------- | --------------- | -------------------- |
| **Tiempo de conversión** | ~5 minutos | ~30-60 segundos | **5-10x más rápido** |
| **Calidad visual**       | Excelente  | Muy buena       | Ligeramente menor    |
| **Tamaño de archivo**    | Base       | +15-20%         | Archivos más grandes |

## 📊 Perfiles de Velocidad Disponibles

### Perfil 1: MÁXIMA VELOCIDAD ⚡ (ACTUAL)

```env
PRESET=ultrafast
CRF=28
AUDIO_BITRATE=96k
```

- ✅ **Mejor para**: Conversiones rápidas, archivos de trabajo
- ⏱️ **Velocidad**: 5-10x más rápido
- 📦 **Tamaño**: +15-20% más grande
- 🎬 **Calidad**: Muy buena (aceptable para la mayoría de usos)

### Perfil 2: BALANCE ⚖️

```env
PRESET=veryfast
CRF=26
AUDIO_BITRATE=128k
```

- ✅ **Mejor para**: Balance entre velocidad y calidad
- ⏱️ **Velocidad**: 3-5x más rápido
- 📦 **Tamaño**: +10-15% más grande
- 🎬 **Calidad**: Excelente

### Perfil 3: CALIDAD 🎯

```env
PRESET=medium
CRF=23
AUDIO_BITRATE=128k
```

- ✅ **Mejor para**: Archivos finales, distribución
- ⏱️ **Velocidad**: Configuración original
- 📦 **Tamaño**: Óptimo
- 🎬 **Calidad**: Máxima

## 🔧 Cómo Cambiar de Perfil

### Opción 1: Editar archivo .env

1. Abre el archivo `.env` junto al ejecutable
2. Modifica las líneas:
   ```env
   PRESET=ultrafast  # Cambia a: veryfast, faster, medium, etc.
   CRF=28           # Cambia a: 23-28 (menor = mejor calidad)
   ```
3. Guarda y ejecuta `convertify.exe convert`

### Opción 2: Usar argumentos CLI (próximamente)

```bash
convertify.exe convert --preset veryfast --crf 26
```

## 📈 Benchmarks de Velocidad

### Presets Disponibles (de más rápido a más lento):

1. **ultrafast** - Máxima velocidad
2. **superfast** - Muy rápido
3. **veryfast** - Bastante rápido
4. **faster** - Rápido
5. **fast** - Moderadamente rápido
6. **medium** - Balance (default anterior)
7. **slow** - Lento pero mejor compresión
8. **slower** - Muy lento
9. **veryslow** - Extremadamente lento

### CRF (Constant Rate Factor)

- **0-17**: Calidad casi sin pérdida (muy lento, archivos grandes)
- **18-23**: Calidad alta (lento, archivos medianos)
- **24-28**: Calidad buena (rápido, archivos pequeños) ← **Recomendado para velocidad**
- **29-51**: Calidad baja (muy rápido, archivos muy pequeños)

## 💡 Consejos de Optimización

### Para Máxima Velocidad

1. ✅ Usa `PRESET=ultrafast`
2. ✅ Aumenta `CRF` a 28-30
3. ✅ Reduce `AUDIO_BITRATE` a 96k o menos
4. ✅ Asegúrate de tener espacio en disco (archivos más grandes)

### Para Mejor Calidad

1. ✅ Usa `PRESET=medium` o `slow`
2. ✅ Reduce `CRF` a 20-23
3. ✅ Aumenta `AUDIO_BITRATE` a 128k-192k
4. ⏱️ Acepta tiempos de conversión más largos

### Para Balance Óptimo

1. ✅ Usa `PRESET=veryfast` o `faster`
2. ✅ Mantén `CRF` en 25-26
3. ✅ Usa `AUDIO_BITRATE=128k`

## 🧪 Prueba de Velocidad

Para verificar la mejora:

1. **Antes de optimizar**: Anota el tiempo de conversión
2. **Después de optimizar**: Compara el nuevo tiempo
3. **Verifica calidad**: Reproduce el video convertido

## ❓ Preguntas Frecuentes

### ¿Por qué los archivos son más grandes?

El preset `ultrafast` prioriza velocidad sobre compresión, resultando en archivos ~15-20% más grandes.

### ¿La calidad es notablemente peor?

No. Con CRF=28, la calidad es muy buena para la mayoría de usos. La diferencia es mínima en pantallas normales.

### ¿Puedo hacerlo aún más rápido?

Sí, puedes:

- Aumentar CRF a 30 (menor calidad)
- Usar `AUDIO_CODEC=copy` para copiar audio sin re-encodear
- Reducir resolución del video (requiere modificación del código)

### ¿Cómo vuelvo a la configuración original?

Cambia en `.env`:

```env
PRESET=medium
CRF=23
AUDIO_BITRATE=128k
```

## 📞 Soporte

Si necesitas ayuda para ajustar la configuración, revisa:

- `README.md` - Documentación general
- `INSTRUCCIONES_EXE.md` - Guía de uso del ejecutable
- `.env.example` - Ejemplos de configuración
