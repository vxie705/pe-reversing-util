#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <filesystem>
#include <cstdint>
#include <algorithm>

namespace fs = std::filesystem;

/**
 * @brief Extrae archivos de un contenedor binario basándose en un índice pattern-matched.
 * @param indexFile El archivo que contiene la estructura/nombres (ej: index.bin)
 * @param archiveFile El contenedor de datos masivo (ej: wolf.xfs)
 * @param outputDir Directorio donde se volcarán los archivos
 */
void generic_extract(const std::string& indexFile, const std::string& archiveFile, const std::string& outputDir) {
    std::ifstream idx(indexFile, std::ios::binary);
    std::ifstream arc(archiveFile, std::ios::binary);

    if (!idx.is_open() || !arc.is_open()) {
        std::cerr << "[!] Error crítico: No se pudieron abrir los archivos de entrada." << std::endl;
        return;
    }

    // Cargar mapa de memoria del índice
    std::vector<char> catalog((std::istreambuf_iterator<char>(idx)), std::istreambuf_iterator<char>());
    idx.close();
    
    size_t count = 0;
    std::cout << "[*] Iniciando Extracción Universal en: " << outputDir << std::endl;

    for (size_t i = 0; i < catalog.size() - 20; ++i) {
        // Buscamos extensiones comunes de forma dinámica (Heurística de patrones)
        if (catalog[i] == '.' && (i + 4 < catalog.size())) {
            
            // Verificamos extensiones conocidas (puedes añadir más aquí)
            std::string ext = "";
            ext += (char)tolower(catalog[i+1]);
            ext += (char)tolower(catalog[i+2]);
            ext += (char)tolower(catalog[i+3]);

            if (ext == "xml" || ext == "ula" || ext == "dat" || ext == "spr" || ext == "dds") {
                
                // Estos offsets son específicos para ciertos motores (Wolfteam/Softnyx)
                // En una versión 100% universal, esto podría ser un parámetro.
                uint32_t offset = *reinterpret_cast<uint32_t*>(&catalog[i + 4]);
                uint32_t size = *reinterpret_cast<uint32_t*>(&catalog[i + 10]);

                // Validación de integridad básica del asset
                if (offset > 0 && size > 0 && size < 50000000) { // Límite de 50MB por asset
                    
                    // Reconstrucción del nombre del archivo (hacia atrás desde el punto)
                    std::string filename = "";
                    for (int b = -1; b > -255 && (i+b) >= 0; b--) {
                        unsigned char c = catalog[i+b];
                        if (isalnum(c) || c == '_' || c == '-') {
                            filename += c;
                        } else {
                            break;
                        }
                    }
                    
                    if (!filename.empty()) {
                        std::reverse(filename.begin(), filename.end());
                        filename += "." + ext;

                        fs::path filePath = fs::path(outputDir) / filename;
                        fs::create_directories(filePath.parent_path());

                        std::vector<char> buffer(size);
                        arc.seekg(offset, std::ios::beg);
                        arc.read(buffer.data(), size);

                        std::ofstream out(filePath, std::ios::binary);
                        if (out.write(buffer.data(), size)) {
                            count++;
                            if (count % 500 == 0) std::cout << "[+] Extraídos " << count << " archivos..." << std::endl;
                        }
                    }
                }
            }
        }
    }

    std::cout << "\n[SUCCESS] Proceso finalizado. Total: " << count << " archivos extraídos." << std::endl;
}

int main(int argc, char* argv[]) {
    
    if (argc < 4) {
        std::cout << "Universal Asset Unpacker v1.0" << std::endl;
        std::cout << "Uso: " << argv[0] << " <index_bin> <data_container> <output_folder>" << std::endl;
        std::cout << "Ejemplo: " << argv[0] << " index.bin game.xfs ./extracted" << std::endl;
        return 0;
    }

    generic_extract(argv[1], argv[2], argv[3]);
    return 0;
}
