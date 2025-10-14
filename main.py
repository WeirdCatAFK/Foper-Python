from preparacion.preparar import preparar
from dotenv import load_dotenv
import time
import os


if __name__ == "__main__":
    # Cargamos los videos
    load_dotenv()
    RUTA_VIDEOS = os.getenv("RUTA_VIDEOS")
    RUTA_RESULTADOS = os.getenv("RUTA_RESULTADOS")
    RUTA_IMAGENES = os.path.join(RUTA_RESULTADOS, "imagenes")
    CUADROS_A_PROCESAR = int(os.getenv("CUADROS_A_PROCESAR"))
    ESCALA = float(os.getenv("ESCALA_DE_PROCESAMIENTO"))
    SUAVIZADO = bool(os.getenv("SUAVIZADO_GAUSS"))
    KERNEL = tuple(int(x) for x in os.getenv("KERNEL_SUAVIZADO").split(","))
    print(f"Procesando {CUADROS_A_PROCESAR} cuadros con escala {ESCALA} y suavizado {SUAVIZADO} con kernel {KERNEL}")

    # Vamos a contar cuanto se demora en procesar los videos
    start = time.time()
    preparar(RUTA_VIDEOS, RUTA_IMAGENES, CUADROS_A_PROCESAR, ESCALA, SUAVIZADO, KERNEL)
    end = time.time()
    print(f"Tiempo de procesamiento de las imagenes: {end - start} segundos")
