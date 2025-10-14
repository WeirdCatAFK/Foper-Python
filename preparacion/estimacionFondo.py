import cv2
import numpy as np
import numba

@numba.njit(fastmath=True, parallel=True)
def _actualizar_modelo_jit(modelo_actual, imagen_gris, contador):
    """
    Función auxiliar compilada por Numba para actualizar el modelo de fondo.
    """
    alpha = 1.0 / contador
    nuevo_modelo = (1.0 - alpha) * modelo_actual + alpha * imagen_gris
    return nuevo_modelo

def estimar_fondo(
    ruta_video: str,
    cuadros_a_procesar: int,
    ruta_guardado: str = None,
    escala: float = 1.0,
    aplicar_suavizado: bool = False, 
    kernel_size: tuple = (5, 5)     
):
    """
    Estima el modelo de fondo de un video y si se le da una ruta guarda el resultado.

    Args:
        ruta_video (str): La ruta al archivo de video.
        cuadros_a_procesar (int): El número de cuadros a promediar.
        ruta_guardado (str, optional): La ruta del archivo donde se guardará
                                       la imagen del fondo. Si es None, no se
                                       guarda nada. Default a None.
        escala (float, optional): Factor para redimensionar los cuadros
                                  (1.0 = sin cambios). Default a 1.0.
        aplicar_suavizado (bool, optional): Si es True, aplica un filtro Gaussiano
                                            a cada cuadro. Default a False.
        kernel_size (tuple, optional): El tamaño del kernel para el filtro
                                       Gaussiano, e.g., (5, 5). Default a (5, 5).

    Returns:
        np.ndarray: Matriz de NumPy con el modelo de fondo estimado,
                    o None si el video no se pudo abrir.
    """
    print("Cargando video...")
    cap = cv2.VideoCapture(ruta_video)

    if not cap.isOpened():
        print(f"Error: No se pudo abrir el video en la ruta: {ruta_video}")
        return None

    print("Estimando el modelo de fondo...")

    modelo_fondo = None
    contador = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Se alcanzó el final del video o hubo un error de lectura.")
            break

        if escala != 1.0:
            frame = cv2.resize(frame, (0, 0), fx=escala, fy=escala, interpolation=cv2.INTER_AREA)
        if aplicar_suavizado:
            frame = cv2.GaussianBlur(frame, kernel_size, 0)

        imagen_gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY).astype(np.float64)

        contador += 1

        if modelo_fondo is None:
            modelo_fondo = imagen_gris
        else:
            modelo_fondo = _actualizar_modelo_jit(modelo_fondo, imagen_gris, contador)

        print(f"Procesando cuadro: {contador}/{cuadros_a_procesar}")

        if contador >= cuadros_a_procesar:
            break

    cap.release()
    print("Estimación finalizada.")

    if ruta_guardado and modelo_fondo is not None:
        try:
            print(f"Guardando el modelo de fondo en: {ruta_guardado}")
            fondo_para_guardar = modelo_fondo.astype(np.uint8)
            cv2.imwrite(ruta_guardado, fondo_para_guardar)
            print("Imagen guardada exitosamente")
        except Exception as e:
            print(f"Error al guardar el archivo: {e}")

    return modelo_fondo


# Pruebas del modulo
if __name__ == '__main__':
    ruta_del_video = './entradas/DJI_20250815114314_0028_D.MP4'
    numero_de_cuadros = 200
    ruta_de_salida = './resultados/video1_con_suavizado.jpg' # Nuevo nombre de archivo

    # Llamada a la función con el suavizado activado
    modelo = estimar_fondo(
        ruta_video=ruta_del_video,
        cuadros_a_procesar=numero_de_cuadros,
        ruta_guardado=ruta_de_salida,
        aplicar_suavizado=True, # Activamos el suavizado
        kernel_size=(21, 21)    # Usamos un kernel más grande para que sea notorio
    )

    if modelo is not None:
        fondo_visualizable = modelo.astype(np.uint8)

        cv2.imshow('Modelo de Fondo Estimado (con Suavizado)', fondo_visualizable)
        print("\nMostrando imagen. Presiona cualquier tecla para cerrar la ventana.")

        cv2.waitKey(0)
        cv2.destroyAllWindows()