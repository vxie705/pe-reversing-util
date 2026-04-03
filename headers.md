Script de reconocimiento estadístico para identificar tipos de archivos ocultos dentro de contenedores binarios masivos.

- Escanea patrones de extensiones de hasta 4 caracteres.
- Genera un conteo estadístico de archivos internos.
- Identifica recursos como `.xml`, `.lua`, `.dtx`, `.ltb`, etc.
- Ideal para el análisis inicial de archivos `.bin` o `.dat`.

### Uso

```bash
python check_headers.py <archivo.bin>
```
