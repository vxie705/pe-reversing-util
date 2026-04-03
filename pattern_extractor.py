import re
import sys
import os

def list_extensions(filename):
    if not os.path.exists(filename):
        print(f"[!] Error: El archivo '{filename}' no existe.")
        return

    with open(filename, 'rb') as f:
        data = f.read()

    extensions = set()
    print(f"--- ESCANEANDO PATRONES EN: {os.path.basename(filename)} ---")
    for match in re.finditer(rb'\.([a-zA-Z0-9]{3,4})[\x00-\x20]', data):
        try:
            ext = match.group(1).decode('ascii', 'ignore').lower()
            extensions.add(ext)
            if ext in ['xml', 'ula', 'lua', 'json', 'txt']:
                start = match.start()
                end = match.end()
                snippet = data[max(0, start-20):min(len(data), end+20)]
                print(f"[+] Hallazgo en offset {hex(start)}: {snippet}")
        except:
            continue

    print("-" * 40)
    print("Extensiones únicas encontradas:", len(extensions))
    print(sorted(list(extensions))[:50])

if __name__ == '__main__':
    if len(sys.argv) > 1:
        list_extensions(sys.argv[1])
    else:
        print("[-] Uso: pattern_extractor.py <archivo.bin>")

