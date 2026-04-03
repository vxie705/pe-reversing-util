import re
import sys
import os

def ext_summary(filename):
    if not os.path.exists(filename):
        print(f"[!] Error: El archivo '{filename}' no existe.")
        return

    with open(filename, 'rb') as f:
        data = f.read()

    extensions = {}
    # Busca patrones .ext seguidos de un carácter de control
    for match in re.finditer(rb'\.([a-zA-Z0-9]{3,4})[\x00-\x20]', data):
        try:
            ext = match.group(1).decode('ascii', 'ignore').lower()
            if ext.startswith('dtx') or ext == 'ltb':
                continue
            extensions[ext] = extensions.get(ext, 0) + 1
        except:
            continue

    sorted_exts = sorted(extensions.items(), key=lambda x: x[1], reverse=True)
    
    print(f"--- RESUMEN DE EXTENSIONES: {os.path.basename(filename)} ---")
    for ext, count in sorted_exts[:30]:
        if count >= 2:
            print(f" .{ext:<5} -> {count} archivos")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        ext_summary(sys.argv[1])
    else:
        print("[-] Uso: python check_headers.py <archivo.bin>")
