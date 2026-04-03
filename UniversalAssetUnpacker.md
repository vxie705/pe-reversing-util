**High-Performance Heuristic Static Analysis Tool**

`UniversalAssetUnpacker.cpp` es una herramienta de extracción masiva diseñada para perforar contenedores binarios (archivos de datos de juegos, firmwares, etc.) basándose en un catálogo de índices previamente reconstruido.

---

## ¿Cómo funciona?

A diferencia de los extractores convencionales que dependen de una estructura de archivos fija, **UAX** utiliza una **Heurística de Escaneo por Patrones**:

1. **Detección de Patrones:** Escanea el índice (`index.bin`) byte a byte buscando extensiones específicas (`.xml`, `.ula`, `.dat`, `.spr`, `.dds`).
2. **Reconstrucción Inversa de Nombres:** Una vez que encuentra una extensión, retrocede desde el punto para reconstruir el nombre original del archivo.
3. **Mapeo de Offsets Pro:** Salta dinámicamente al contenedor de datos (`.xfs` o similar) para extraer el archivo exacto.

---

## Instalación y Compilación

Para obtener el máximo rendimiento (velocidad nativa), se recomienda compilar con optimización:

### Con Visual Studio (cl.exe):

```powershell
cl.exe /O2 /EHsc UniversalAssetUnpacker.cpp /FeUAX.exe
```

### Con GCC (g++):

```bash
g++ -O3 UniversalAssetUnpacker.cpp -o UAX.exe -static-libgcc -static-libstdc++
```

---

## Modo de Uso

UAX es ahora **modular**. Solo tienes que pasarle los archivos como argumentos en tu terminal:

```powershell
./UAX.exe <archivo_indice> <contenedor_datos> <directorio_salida>
```

**Ejemplo real con Wolfteam:**

```powershell
./UAX.exe index.bin xfs/wolf.xfs ./extracted_data
```

---

## Flujo de Trabajo (Pipeline)

Para un éxito total en la extracción, el flujo recomendado es:

1. **`PrepareIndex.py`**: Descomprime los bloques ZLIB del juego para generar el mapa `index.bin`.
2. **`UniversalAssetUnpacker.exe`**: Extrae los activos reales usando el mapa generado.
3. **`MassDecompressor.py`** (Opcional): Si los archivos extraídos están en formato ZLIB (como algunos `.dat`), este script los vuelve legibles al 100%.

---

## Límites de Seguridad

- **Límetro de Peso:** No extraerá archivos que pesen más de 50MB (protección contra offsets corruptos).
- **Validación Alfanumérica:** Solo captura nombres con caracteres válidos para evitar basura en el sistema de archivos.

---

_Herramienta desarrollada para el Toolkit de Análisis Binario de Ciberseguridad._
