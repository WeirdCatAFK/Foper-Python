import os
import numpy as np
import matplotlib.pyplot as plt
from dotenv import load_dotenv

def visualizar_resultados():
    """
    Carga y visualiza todos los pares de mapas de disparidad y error
    encontrados en el directorio de resultados.
    """
    # ---- 1. Cargar Rutas desde el Archivo .env ----
    load_dotenv()
    RUTA_RESULTADOS = os.getenv("RUTA_RESULTADOS")
    
    if not RUTA_RESULTADOS:
        print("Error: La variable RUTA_RESULTADOS no está definida en el archivo .env")
        return

    RUTA_DISPARIDAD = os.path.join(RUTA_RESULTADOS, "disparidad")

    if not os.path.isdir(RUTA_DISPARIDAD):
        print(f"Error: El directorio de resultados '{RUTA_DISPARIDAD}' no existe.")
        return

    # ---- 2. Encontrar todos los Archivos de Disparidad ----
    archivos_disparidad = [f for f in os.listdir(RUTA_DISPARIDAD) if f.endswith(".disparidad.npy")]

    if not archivos_disparidad:
        print(f"No se encontraron archivos de disparidad en '{RUTA_DISPARIDAD}'.")
        return

    print(f"Se encontraron {len(archivos_disparidad)} archivos de disparidad. Visualizando...")

    # ---- 3. Iterar, Cargar y Visualizar cada Par ----
    for archivo_disp in sorted(archivos_disparidad):
        nombre_base = archivo_disp.replace(".disparidad.npy", "")
        archivo_error = f"{nombre_base}.error.npy"
        
        # Construir rutas completas
        ruta_disp = os.path.join(RUTA_DISPARIDAD, archivo_disp)
        ruta_error = os.path.join(RUTA_DISPARIDAD, archivo_error)

        try:
            # Cargar los datos desde los archivos .npy
            mapa_disparidad = np.load(ruta_disp)
            mapa_error = np.load(ruta_error)

            # Crear la visualización
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
            fig.suptitle(f"Resultados para: {nombre_base}", fontsize=16)

            # Gráfica del Mapa de Disparidad
            im1 = ax1.imshow(mapa_disparidad, cmap='jet')
            ax1.set_title("Mapa de Disparidad")
            ax1.axis('off') # Ocultar ejes
            fig.colorbar(im1, ax=ax1, orientation='vertical', fraction=0.046, pad=0.04)

            # Gráfica del Mapa de Error
            im2 = ax2.imshow(mapa_error, cmap='jet')
            ax2.set_title("Mapa de Error de Coincidencia")
            ax2.axis('off') # Ocultar ejes
            fig.colorbar(im2, ax=ax2, orientation='vertical', fraction=0.046, pad=0.04)

            plt.tight_layout(rect=[0, 0, 1, 0.96])
            plt.show()

        except FileNotFoundError:
            print(f"Advertencia: Se encontró '{archivo_disp}' pero no su par de error '{archivo_error}'. Saltando.")
        except Exception as e:
            print(f"Ocurrió un error al procesar el archivo '{archivo_disp}': {e}")


if __name__ == '__main__':
    visualizar_resultados()