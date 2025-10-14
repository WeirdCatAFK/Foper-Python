import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from dotenv import load_dotenv

def visualizar_un_resultado(nombre_base):
    """
    Carga y visualiza un par específico de mapas de disparidad y error.

    Args:
        nombre_base (str): El nombre base del par de resultados a visualizar
                           (ej: 'toma0-toma1').
    """
    load_dotenv()
    RUTA_RESULTADOS = os.getenv("RUTA_RESULTADOS")
    
    if not RUTA_RESULTADOS:
        print("Error: La variable RUTA_RESULTADOS no está definida en el archivo .env")
        return

    RUTA_DISPARIDAD = os.path.join(RUTA_RESULTADOS, "disparidad")

    ruta_disp = os.path.join(RUTA_DISPARIDAD, f"{nombre_base}.disparidad.npy")
    ruta_error = os.path.join(RUTA_DISPARIDAD, f"{nombre_base}.error.npy")

    try:
        print(f"Cargando archivos para '{nombre_base}'...")
        mapa_disparidad = np.load(ruta_disp)
        mapa_error = np.load(ruta_error)

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        fig.suptitle(f"Resultados para: {nombre_base}", fontsize=16)

        im1 = ax1.imshow(mapa_disparidad, cmap='jet')
        ax1.set_title("Mapa de Disparidad")
        ax1.axis('off')
        fig.colorbar(im1, ax=ax1, orientation='vertical', fraction=0.046, pad=0.04)

        im2 = ax2.imshow(mapa_error, cmap='jet')
        ax2.set_title("Mapa de Error de Coincidencia")
        ax2.axis('off')
        fig.colorbar(im2, ax=ax2, orientation='vertical', fraction=0.046, pad=0.04)

        plt.tight_layout(rect=[0, 0, 1, 0.96])
        print("Mostrando visualización. Cierra la ventana para terminar.")
        plt.show()

    except FileNotFoundError:
        print(f"Error: No se pudieron encontrar los archivos para '{nombre_base}'.")
        print(f"Verifica que existan los siguientes archivos:")
        print(f"  - {ruta_disp}")
        print(f"  - {ruta_error}")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")


if __name__ == '__main__':
    # Verificar que se haya pasado un argumento desde la línea de comandos
    if len(sys.argv) < 2:
        print("Error: Debes proporcionar el nombre base del resultado a visualizar.")
        print("Uso: python visualizar_individual.py <nombre_base>")
        print("Ejemplo: python visualizar_individual.py toma0-toma1")
    else:
        nombre_base_resultado = sys.argv[1]
        visualizar_un_resultado(nombre_base_resultado)