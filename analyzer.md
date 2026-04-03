Herramienta de análisis estático universal para archivos ejecutables de Windows (PE). Extrae información técnica crítica y la exporta en un formato JSON estructurado.

- Identifica la firma `MZ` y `PE`.
- Detecta arquitectura (**x86** vs **x64**).
- Mapea la tabla de secciones con sus tamaños virtuales y físicos.
- Salida en JSON legible para integración con otras herramientas.

### Uso

```bash
python pe_analyzer.py <archivo.exe>
```
