import os

try:
    from .estimacionFondo import estimar_fondo
except ImportError:
    from estimacionFondo import estimar_fondo


def preparar(
    ruta_videos: str,
    ruta_imagenes: str,
    cuadros_a_procesar: int,
    escala: float = 1.0,
    aplicar_suavizado: bool = False,
    kernel_suavizado: tuple = (5, 5),
):
    """
    Estima el fondo de un video y si se le da una ruta guarda el resultado.

    Args:
        ruta_videos (str): Ruta al directorio que contiene los videos.
        ruta_imagenes (str): Ruta donde se guardaran las imagenes procesadas
        cuadros_a_procesar (int): Los frames por video
        escala (float): The scale factor to resize the frames (1.0 means original size).
        aplicar_suavizado (bool): Activa o desactiva el suavizado Gaussiano.
        kernel_suavizado (tuple): El tamaño del kernel para el suavizado.
    """
    os.makedirs(ruta_imagenes, exist_ok=True)
    videos_a_procesar = [
        video
        for video in os.listdir(ruta_videos)
        if (video.endswith(".MP4") or video.endswith(".mp4"))
    ]

    print(
        f"Se procesarán {cuadros_a_procesar} cuadros de {len(videos_a_procesar)} videos encontrados."
    )

    for nombre_video in videos_a_procesar:
        print(f"\nProcesando el video: {nombre_video}")

        ruta_completa_video = os.path.join(ruta_videos, nombre_video)
        ruta_salida_imagen = os.path.join(ruta_imagenes, f"{nombre_video.split('.')[0]}.jpg")

        try:
            estimar_fondo(
                ruta_completa_video,
                cuadros_a_procesar,
                ruta_salida_imagen,
                escala,
                aplicar_suavizado,
                kernel_suavizado,
            )

            print(
                f"Modelo de fondo para '{nombre_video}' guardado en '{ruta_salida_imagen}'"
            )
        except Exception as e:
            print(f"Error al procesar el video '{nombre_video}': {e}")


if __name__ == "__main__":
    ruta_videos = "./entradas"
    ruta_imagenes = "./resultados/imagenes"
    cuadros_a_procesar = 200
    escala = 1.0

    preparar(
        ruta_videos,
        ruta_imagenes,
        cuadros_a_procesar,
        escala,
        aplicar_suavizado=True,
        kernel_suavizado=(15, 15),
    )
