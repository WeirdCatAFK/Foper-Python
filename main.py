from preparacion.preparar import preparar
from dotenv import load_dotenv
import os


if __name__ == "__main__":
    # Cargamos los videos
    load_dotenv()
    ruta_videos = os.getenv("RUTA_VIDEOS")
    ruta_resultados = os.getenv("RUTA_RESULTADOS")
    ruta_imagenes = os.path.join(ruta_resultados, "imagenes")
    cuadros_a_procesar = int(os.getenv("CUADROS_A_PROCESAR"))
    escala = float(os.getenv("ESCALA_DE_PROCESAMIENTO"))

    preparar(ruta_videos, ruta_imagenes, cuadros_a_procesar, escala)
