## Convertify 2.0 - Mejoras pendientes

- [x] 1) main.py: loggear excepciones con logger.exception en vez de `sys.exit(1)` silencioso
- [x] 2) Semántica SKIPPED vs FAILED:
  - [x] Ajustar `VideoConversionService` para que “locked/skip” no cuente como FAILED (definir success=True o que main.py discrimine SKIPPED)
- [x] 3) (Siguiente) Timeout configurable para FFmpeg en `MoviePyVideoConverter`
- [x] 4) (Siguiente) Paralelismo real respetando `max_workers`
- [ ] 5) (Siguiente) Optimizar locked-check (psutil fallback/caching)
- [ ] 6) (Siguiente) Centralizar configuración de rutas UNC
- [ ] 7) (Siguiente) Tests adicionales para semántica SKIPPED y timeout
