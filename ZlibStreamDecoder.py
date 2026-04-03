import os
import zlib
import argparse
import glob

def decompress_assets(source_dir, target_dir):
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    print(f"[*] Decoding ZLIB streams from: {source_dir}")
    files = glob.glob(os.path.join(source_dir, '*.*'))
    success_count = 0
    
    for filepath in files:
        filename = os.path.basename(filepath)
        out_path = os.path.join(target_dir, filename)
        
        try:
            with open(filepath, 'rb') as f:
                data = f.read()
            
            # Buscamos la firma ZLIB (0x78 0x9C) en los primeros 32 bytes
            header_idx = data.find(b'\x78\x9c')
            
            if header_idx != -1 and header_idx < 32:
                # Extraemos el stream y lo descomprimimos
                decoded_data = zlib.decompress(data[header_idx:])
                with open(out_path, 'wb') as out_f:
                    out_f.write(decoded_data)
                success_count += 1
            else:
                # Si no tiene firma ZLIB, lo copiamos tal cual
                with open(out_path, 'wb') as out_f:
                    out_f.write(data)
        except Exception:
            # En caso de error de descompresión, mantenemos el original
            with open(out_path, 'wb') as out_f:
                out_f.write(data)

    print(f"\n[SUCCESS] Decoded {success_count} assets into: {target_dir}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Zlib Stream Decoder Pro v1.0")
    parser.add_argument("source", help="Directorio con archivos extraídos (brutos)")
    parser.add_argument("target", help="Directorio para archivos legibles (decodificados)")
    
    args = parser.parse_args()
    decompress_assets(args.source, args.target)
