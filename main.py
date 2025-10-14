
from dotenv import load_dotenv
import time
import os
import cv2
import numpy as np


try:
    from disparidad.generar import calcular_mapa_disparidad
    from preparacion.preparar import preparar
except ImportError:
    from .disparidad.generar import calcular_mapa_disparidad
    from .preparacion.preparar import preparar
    

if __name__ == "__main__":
    # ---- 1. Carga de Configuración y Preparación de Imágenes ----
    load_dotenv()
    RUTA_VIDEOS = os.getenv("RUTA_VIDEOS")
    RUTA_RESULTADOS = os.getenv("RUTA_RESULTADOS")
    RUTA_IMAGENES = os.path.join(RUTA_RESULTADOS, "imagenes")
    
    # Directorio para guardar los resultados de disparidad
    RUTA_DISPARIDAD = os.path.join(RUTA_RESULTADOS, "disparidad")

    CUADROS_A_PROCESAR = int(os.getenv("CUADROS_A_PROCESAR"))
    ESCALA = float(os.getenv("ESCALA_DE_PROCESAMIENTO"))
    SUAVIZADO = os.getenv("SUAVIZADO_GAUSS").lower() in ('true', '1', 't')
    KERNEL = tuple(int(x) for x in os.getenv("KERNEL_SUAVIZADO").split(","))
    
    # Parámetros para el cálculo de disparidad (puedes moverlos al .env si lo prefieres)
    RADIO_VENTANA = int(os.getenv("RADIO_VENTANA", 15))
    RADIO_BUSQUEDA = int(os.getenv("RADIO_BUSQUEDA", 55))

    print(f"Procesando {CUADROS_A_PROCESAR} cuadros con escala {ESCALA} y suavizado {SUAVIZADO} con kernel {KERNEL}")

    # Ejecuta la preparación de imágenes
    start_preparacion = time.time()
    preparar(RUTA_VIDEOS, RUTA_IMAGENES, CUADROS_A_PROCESAR, ESCALA, SUAVIZADO, KERNEL)
    end_preparacion = time.time()
    print(f"Tiempo de preparación de imágenes: {end_preparacion - start_preparacion:.2f} segundos")
    print("-" * 50)

    # ---- 2. Cálculo de Disparidad por Pares ----
    print("Iniciando cálculo de mapas de disparidad...")
    start_disparidad = time.time()

    # Crear el directorio de resultados si no existe
    os.makedirs(RUTA_DISPARIDAD, exist_ok=True)

    # Obtener y ordenar la lista de imágenes preparadas
    try:
        lista_imagenes = sorted(os.listdir(RUTA_IMAGENES))
    except FileNotFoundError:
        print(f"Error: El directorio de imágenes '{RUTA_IMAGENES}' no fue encontrado. Asegúrate de que la preparación se completó correctamente.")
        exit()

    # Iterar sobre la lista de imágenes en pares (0,1), (2,3), (4,5), ...
    for i in range(0, len(lista_imagenes) - 1, 2):
        img_nombre_izq = lista_imagenes[i]
        img_nombre_der = lista_imagenes[i+1]

        # Construir las rutas completas
        ruta_img_izq = os.path.join(RUTA_IMAGENES, img_nombre_izq)
        ruta_img_der = os.path.join(RUTA_IMAGENES, img_nombre_der)

        print(f"Procesando par: {img_nombre_izq} y {img_nombre_der}")

        # Cargar las imágenes en escala de grises
        img_i = cv2.imread(ruta_img_izq, cv2.IMREAD_GRAYSCALE)
        img_d = cv2.imread(ruta_img_der, cv2.IMREAD_GRAYSCALE)
        
        if img_i is None or img_d is None:
            print(f"  -> Advertencia: No se pudo cargar una o ambas imágenes del par. Saltando.")
            continue

        # Calcular el mapa de disparidad
        mapa_disparidad, mapa_error = calcular_mapa_disparidad(img_i, img_d, RADIO_VENTANA, RADIO_BUSQUEDA)

        # Generar nombres para los archivos de salida
        base_nombre_izq = os.path.splitext(img_nombre_izq)[0]
        base_nombre_der = os.path.splitext(img_nombre_der)[0]
        nombre_salida_base = f"{base_nombre_izq}-{base_nombre_der}"
        
        ruta_salida_disparidad = os.path.join(RUTA_DISPARIDAD, f"{nombre_salida_base}.disparidad.npy")
        ruta_salida_error = os.path.join(RUTA_DISPARIDAD, f"{nombre_salida_base}.error.npy")

        # Guardar los arrays de numpy
        np.save(ruta_salida_disparidad, mapa_disparidad)
        np.save(ruta_salida_error, mapa_error)
        print(f"  -> Resultados guardados en '{RUTA_DISPARIDAD}'")

    end_disparidad = time.time()
    print("-" * 50)
    print(f"Tiempo total de cálculo de disparidad: {end_disparidad - start_disparidad:.2f} segundos")
    print("Proceso completado.")