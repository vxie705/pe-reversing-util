# Zlib Stream Decoder (ZSD)

**Automated Post-Extraction Asset Decoder**

`ZlibStreamDecoder.py` es una utilidad de Python diseñada para procesar activos extraídos que aún se encuentran comprimidos o empaquetados bajo el estándar **ZLIB (RFC 1950)**.

---

## ¿Qué resuelve esta herramienta?

Muchos motores de juegos (como el de Wolfteam) utilizan una doble capa de empaquetado. Mientras que el extractor de C++ rompe el contenedor `.xfs`, esta herramienta rompe la compresión individual de cada archivo `.xml`, `.ula` o `.dat`.

### Capacidades:

- **Detección Automática:** Localiza la firma `0x78 0x9C` incluso si hay basura o cabeceras adicionales antes del stream.
- **Modo Pass-Through:** Si el archivo ya es legible (texto plano), la herramienta lo transfiere intacto al destino.
- **Batch Processing:** Procesa miles de archivos en segundos.

---

## Modo de Uso

Se ejecuta mediante la línea de comandos de Python, indicando el origen (la salida de UAX) y el destino final:

```powershell
python ZlibStreamDecoder.py <directorio_bruto> <directorio_legible>
```

**Ejemplo:**

```powershell
python ZlibStreamDecoder.py ./ssa/final_cpp_extracted ./ssa/final_unpacked
```

---

## Integración en el Workflow

Esta herramienta es el **paso final** de la cadena de análisis:

1. **PrepareIndex.py** (Parser de índices).
2. **UAX.exe** (Extractor de alta velocidad).
3. **ZSD.py** (Decodificador de archivos legibles).

---
