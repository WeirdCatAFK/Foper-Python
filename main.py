from dotenv import load_dotenv
import time
import os
import cv2
import numpy as np
import sys

# --- MODIFICACIÓN ---
# load_dotenv() y ESCALA se eliminan de aquí
# Se cargarán solo dentro del bloque __name__ == "__main__"

# --- Importaciones de módulos del proyecto ---
try:
    from disparidad.generar import calcular_mapa_disparidad
    from preparacion.preparar import preparar
    from reconstruccion.reconstruction import (
        CameraConfig,
        reconstruct_3d_from_disparity,
        save_point_cloud_to_ply,
    )
except ImportError as e:
    print(f"Error al importar módulos: {e}")
    print("Asegúrate de que los archivos .py estén en las carpetas correctas.")
    sys.exit(1)


# --- MODIFICACIÓN ---
# La función ahora acepta 'escala' como argumento
def cargar_configuracion_camara(escala):
    """
    Carga los parámetros de la cámara desde las variables de entorno.
    """
    try:
        config = CameraConfig(
            # Usa el argumento 'escala' en lugar de la global 'ESCALA'
            fx=float(os.getenv("FX")) * escala,
            fy=float(os.getenv("FY")) * escala,
            cy=float(os.getenv("CY")) * escala,
            cx=float(os.getenv("CX")) * escala,
            baseline=float(os.getenv("BASELINE")),
        )

        if config.baseline <= 0:
            print(
                "Error: El valor 'BASELINE' en el archivo .env debe ser un número positivo (en metros)."
            )
            sys.exit(1)

        print("Configuración de cámara cargada exitosamente.")
        return config

    except (TypeError, ValueError) as e:
        print(
            f"Error: No se pudieron cargar los parámetros de la cámara desde el archivo .env."
        )
        print(
            "Asegúrate de que FX, FY, CX, CY, y BASELINE estén definidos y sean números válidos."
        )
        print(f"Error específico: {e}")
        sys.exit(1)


if __name__ == "__main__":
    # ---- 1. Carga de Configuración y Preparación de Imágenes ----
    
    # --- MODIFICACIÓN ---
    # load_dotenv() se llama aquí, una sola vez.
    load_dotenv() 
    
    RUTA_VIDEOS = os.getenv("RUTA_VIDEOS")
    RUTA_RESULTADOS = os.getenv("RUTA_RESULTADOS")
    RUTA_IMAGENES = os.path.join(RUTA_RESULTADOS, "imagenes")

    # Directorios para guardar los resultados
    RUTA_DISPARIDAD = os.path.join(RUTA_RESULTADOS, "disparidad")
    RUTA_RECONSTRUCCION = os.path.join(
        RUTA_RESULTADOS, "reconstructions"
    )  # Nueva carpeta

    CUADROS_A_PROCESAR = int(os.getenv("CUADROS_A_PROCESAR"))
    
    # --- MODIFICACIÓN ---
    # ESCALA se define aquí, una sola vez.
    ESCALA = float(os.getenv("ESCALA_DE_PROCESAMIENTO")) 
    
    SUAVIZADO = os.getenv("SUAVIZADO_GAUSS").lower() in ("true", "1", "t")
    KERNEL = tuple(int(x) for x in os.getenv("KERNEL_SUAVIZADO").split(","))

    RADIO_VENTANA = int(os.getenv("RADIO_VENTANA", 15))
    RADIO_BUSQUEDA = int(os.getenv("RADIO_BUSQUEDA", 55))

    # --- MODIFICACIÓN ---
    # Cargar la configuración de la cámara pasando ESCALA explícitamente
    config_camara = cargar_configuracion_camara(ESCALA)

    print(
        f"Procesando {CUADROS_A_PROCESAR} cuadros con escala {ESCALA} y suavizado {SUAVIZADO} con kernel {KERNEL}"
    )

    # Ejecuta la preparación de imágenes
    start_preparacion = time.time()
    preparar(RUTA_VIDEOS, RUTA_IMAGENES, CUADROS_A_PROCESAR, ESCALA, SUAVIZADO, KERNEL)
    end_preparacion = time.time()
    print(
        f"Tiempo de preparación de imágenes: {end_preparacion - start_preparacion:.2f} segundos"
    )
    print("-" * 50)

    # ---- 2. Cálculo de Disparidad y Reconstrucción 3D ----
    print("Iniciando cálculo de mapas de disparidad y reconstrucción 3D...")
    start_disparidad = time.time()

    # Crear los directorios de resultados si no existen
    os.makedirs(RUTA_DISPARIDAD, exist_ok=True)
    os.makedirs(RUTA_RECONSTRUCCION, exist_ok=True)  # Crear nueva carpeta

    # Obtener y ordenar la lista de imágenes preparadas
    try:
        lista_imagenes = sorted(os.listdir(RUTA_IMAGENES))
    except FileNotFoundError:
        print(
            f"Error: El directorio de imágenes '{RUTA_IMAGENES}' no fue encontrado. Asegúrate de que la preparación se completó correctamente."
        )
        sys.exit(1) # <-- MODIFICACIÓN (consistencia)

    # Iterar sobre la lista de imágenes en pares (0,1), (2,3), (4,5), ...
    for i in range(0, len(lista_imagenes) - 1, 2):
        img_nombre_izq = lista_imagenes[i]
        img_nombre_der = lista_imagenes[i + 1]

        ruta_img_izq = os.path.join(RUTA_IMAGENES, img_nombre_izq)
        ruta_img_der = os.path.join(RUTA_IMAGENES, img_nombre_der)

        print(f"Procesando par: {img_nombre_izq} y {img_nombre_der}")

        img_i = cv2.imread(ruta_img_izq, cv2.IMREAD_GRAYSCALE)
        img_d = cv2.imread(ruta_img_der, cv2.IMREAD_GRAYSCALE)

        if img_i is None or img_d is None:
            print(
                f"  -> Advertencia: No se pudo cargar una o ambas imágenes del par. Saltando."
            )
            continue

        # --- PASO 2.A: Calcular el mapa de disparidad ---
        # Esta función AHORA usará multiprocessing internamente
        mapa_disparidad, mapa_error = calcular_mapa_disparidad(
            img_i, img_d, RADIO_VENTANA, RADIO_BUSQUEDA
        )

        base_nombre_izq = os.path.splitext(img_nombre_izq)[0]
        base_nombre_der = os.path.splitext(img_nombre_der)[0]
        nombre_salida_base = f"{base_nombre_izq}-{base_nombre_der}"

        ruta_salida_disparidad = os.path.join(
            RUTA_DISPARIDAD, f"{nombre_salida_base}.disparidad.npy"
        )
        ruta_salida_error = os.path.join(
            RUTA_DISPARIDAD, f"{nombre_salida_base}.error.npy"
        )

        np.save(ruta_salida_disparidad, mapa_disparidad)
        np.save(ruta_salida_error, mapa_error)
        print(f"  -> Mapas de disparidad y error guardados en '{RUTA_DISPARIDAD}'")

        # --- PASO 2.B: Reconstrucción 3D ---
        print(f"  -> Iniciando reconstrucción 3D para '{nombre_salida_base}'...")

        # Usar el mapa de disparidad (norma) para la reconstrucción
        point_cloud = reconstruct_3d_from_disparity(mapa_disparidad, config_camara)

        if point_cloud.size == 0:
            print(
                "    -> Advertencia: La reconstrucción no generó puntos. (¿Mapa de disparidad vacío?)"
            )
            continue

        ruta_salida_ply = os.path.join(RUTA_RECONSTRUCCION, f"{nombre_salida_base}.ply")

        save_point_cloud_to_ply(point_cloud, ruta_salida_ply)
        print(f"  -> Nube de puntos 3D guardada en '{ruta_salida_ply}'")

    end_disparidad = time.time()
    print("-" * 50)
    print(
        f"Tiempo total de cálculo y reconstrucción: {end_disparidad - start_disparidad:.2f} segundos"
    )
    print("Proceso completado.")