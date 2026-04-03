import struct
import json
import sys
import os

def read_uint16(f):
    return struct.unpack('<H', f.read(2))[0]
def read_uint32(f):
    return struct.unpack('<I', f.read(4))[0]

def analyze_pe(filename):
    if not os.path.exists(filename):
        print(json.dumps({"error": f"Archivo '{filename}' no encontrado"}))
        return

    out = {}
    with open(filename, 'rb') as f:
        if f.read(2) != b'MZ':
            print(json.dumps({"error": "No es un ejecutable MZ (DOS)"}))
            return
        f.seek(0x3C)
        pe_offset = read_uint32(f)
        f.seek(pe_offset)
        if f.read(4) != b'PE\x00\x00':
            print(json.dumps({"error": "No es un ejecutable PE (Windows)"}))
            return
        
        machine = read_uint16(f)
        num_sections = read_uint16(f)
        f.seek(12, 1)
        opt_hdr_size = read_uint16(f)
        characteristics = read_uint16(f)
        
        out['filename'] = os.path.basename(filename)
        out['is_64_bit'] = (machine == 0x8664)
        out['num_sections'] = num_sections
        out['sections'] = []
        
        opt_hdr_offset = pe_offset + 24
        f.seek(opt_hdr_offset + opt_hdr_size)
        
        for i in range(num_sections):
            b_name = f.read(8)
            name = b_name.split(b'\x00')[0].decode('ascii', errors='replace').strip()
            v_size = read_uint32(f)
            v_addr = read_uint32(f)
            r_size = read_uint32(f)
            r_addr = read_uint32(f)
            f.seek(16, 1)
            out['sections'].append({
                'name': name, 
                'virtual_size': hex(v_size), 
                'virtual_address': hex(v_addr),
                'raw_size': hex(r_size),
                'raw_address': hex(r_addr)
            })
            
    print(json.dumps(out, indent=4))

if __name__ == '__main__':
    if len(sys.argv) > 1:
        analyze_pe(sys.argv[1])
    else:
        print(json.dumps({"error": "Uso: python analyze_pe_json.py <archivo.exe>"}))

