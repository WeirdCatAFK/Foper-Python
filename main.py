from dotenv import load_dotenv
import time
import os
import cv2
import numpy as np
import sys

try:
    from disparidad.generar import calcular_mapa_disparidad
    from preparacion.preparar import preparar
    from reconstruccion.reconstruction import (
        CameraConfig,
        reconstruct_3d_from_disparity,
        save_point_cloud_to_ply,
    )
    # --- MODIFICACIÓN ---
    # Importar las funciones actualizadas
    from reconstruccion.rectify import (
        load_calibration_data,
        scale_camera_matrix,
        rectify_images # <-- Nombre de función actualizado
    )
    # Importar el nuevo módulo de estimación de pose
    from reconstruccion.pose_estimator import estimate_pose

except ImportError as e:
    print(f"Error al importar módulos: {e}")
    print("Asegúrate de que los archivos .py estén en las carpetas correctas.")
    print("Asegúrate de que 'reconstruccion/rectify.py', 'reconstruccion/reconstruction.py' y 'reconstruccion/pose_estimator.py' existen.")
    sys.exit(1)


# --- MODIFICACIÓN ---
# Esta función sigue siendo correcta y necesaria
def create_config_from_rectify_params(new_params):
    """
    Crea un objeto CameraConfig a partir de los nuevos parámetros de rectificación.
    """
    P1 = new_params['P1']
    P2 = new_params['P2']
    
    fx = P1[0, 0]
    fy = P1[1, 1]
    cx = P1[0, 2]
    cy = P1[1, 2]
    
    Tx = P2[0, 3]
    
    if fx == 0:
        print("❌ ERROR: El parámetro 'fx' rectificado es 0. No se puede calcular el baseline.")
        return None
        
    baseline = abs(-Tx / fx)
    
    config = CameraConfig(
        fx=fx,
        fy=fy,
        cx=cx,
        cy=cy,
        baseline=baseline
    )
    
    if baseline <= 0:
        print(f"❌ ERROR: El baseline calculado es {baseline}, pero debe ser positivo.")
        print("   La estimación de pose (R, t) puede haber fallado o ser incorrecta.")
        return None
        
    return config


if __name__ == "__main__":
    # ---- 1. Carga de Configuración y Preparación de Imágenes ----
    
    load_dotenv() 
    
    RUTA_VIDEOS = os.getenv("RUTA_VIDEOS")
    RUTA_RESULTADOS = os.getenv("RUTA_RESULTADOS")
    RUTA_IMAGENES = os.path.join(RUTA_RESULTADOS, "imagenes")

    RUTA_DISPARIDAD = os.path.join(RUTA_RESULTADOS, "disparidad")
    RUTA_RECONSTRUCCION = os.path.join(
        RUTA_RESULTADOS, "reconstructions"
    )

    RUTA_CALIBRACION = os.getenv("RUTA_CALIBRACION", "calibration.json")

    CUADROS_A_PROCESAR = int(os.getenv("CUADROS_A_PROCESAR"))
    
    # --- CORRECCIÓN DE BUG ---
    # El .env original tiene "ESCALA_DE_PROCESAMIENTO"
    # El script anterior tenía "ESCALA_DE_PROCESO"
    # Esta línea ahora coincide con el .env original.
    ESCALA = float(os.getenv("ESCALA_DE_PROCESAMIENTO"))
    
    SUAVIZADO = os.getenv("SUAVIZADO_GAUSS").lower() in ("true", "1", "t")
    KERNEL = tuple(int(x) for x in os.getenv("KERNEL_SUAVIZADO").split(","))

    RADIO_VENTANA = int(os.getenv("RADIO_VENTANA", 15))
    RADIO_BUSQUEDA = int(os.getenv("RADIO_BUSQUEDA", 55))

    # --- NUEVO (LÍNEA 101) ---
    # Cargar la distancia real de la "pasada" para dar escala al modelo
    try:
        BASELINE_METERS = float(os.getenv("BASELINE_METERS"))
        if BASELINE_METERS <= 0:
            raise ValueError("BASELINE_METERS debe ser un número positivo.")
        print(f"✓ Distancia de línea de base (escala) cargada: {BASELINE_METERS}m")
    except (TypeError, ValueError) as e:
        print(f"Error fatal al cargar 'BASELINE_METERS' desde .env: {e}")
        print("Asegúrate de que 'BASELINE_METERS=5.0' (o tu distancia) esté en .env")
        sys.exit(1)

    # --- MODIFICACIÓN ---
    # Cargamos solo K (intrínsecos) y D (distorsión) de 'calibration.json'
    # Ignoramos R y t porque son para "Case B" (un par por toma)
    try:
        K_orig, D_orig = load_calibration_data(RUTA_CALIBRACION)
        print("Datos de calibración (K, D) cargados exitosamente.")
    except Exception as e:
        print(f"Error fatal al cargar '{RUTA_CALIBRACION}': {e}")
        print("Asegúrate de que el archivo existe y RUTA_CALIBRACION está en .env")
        sys.exit(1)

    # Escalamos la matriz K *una vez* al inicio
    K_scaled = scale_camera_matrix(K_orig, ESCALA)


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

    # ---- 2. Estimación de Pose, Rectificación, Disparidad y Reconstrucción ----
    print("Iniciando bucle de procesamiento: Estimación de Pose -> Rectificación -> Disparidad -> Reconstrucción 3D...")
    start_proceso = time.time()

    os.makedirs(RUTA_DISPARIDAD, exist_ok=True)
    os.makedirs(RUTA_RECONSTRUCCION, exist_ok=True)

    try:
        lista_imagenes = sorted(os.listdir(RUTA_IMAGENES))
    except FileNotFoundError:
        print(
            f"Error: El directorio de imágenes '{RUTA_IMAGENES}' no fue encontrado. Asegúrate de que la preparación se completó correctamente."
        )
        sys.exit(1)

    # Iterar sobre la lista de imágenes en pares (0,1), (2,3), (4,5), ...
    for i in range(0, len(lista_imagenes) - 1, 2):
        img_nombre_izq = lista_imagenes[i]
        img_nombre_der = lista_imagenes[i + 1]

        ruta_img_izq = os.path.join(RUTA_IMAGENES, img_nombre_izq)
        ruta_img_der = os.path.join(RUTA_IMAGENES, img_nombre_der)

        print(f"\nProcesando par: {img_nombre_izq} y {img_nombre_der}")

        # --- PASO 2.A: Cargar y escalar imágenes ---
        # Cargamos las imágenes *preparadas* (escaladas y suavizadas)
        img_i_scaled = cv2.imread(ruta_img_izq, cv2.IMREAD_GRAYSCALE)
        img_d_scaled = cv2.imread(ruta_img_der, cv2.IMREAD_GRAYSCALE)

        if img_i_scaled is None or img_d_scaled is None:
            print(f"   -> Advertencia: No se pudo cargar una o ambas imágenes del par. Saltando.")
            continue
            
        if img_i_scaled.shape != img_d_scaled.shape:
            print(f"   -> Advertencia: Las imágenes no tienen el mismo tamaño. Saltando.")
            continue
            
        # --- PASO 2.B: Estimar la Pose (R y t) para ESTE PAR ---
        print("   -> Estimando pose (R, t) con feature matching...")
        R_pair, t_pair_unit = estimate_pose(img_i_scaled, img_d_scaled, K_scaled, D_orig)
        
        if R_pair is None or t_pair_unit is None:
            print("   -> Advertencia: Falló la estimación de pose. Saltando par.")
            continue
            
        # --- NUEVO (LÍNEA 174) ---
        # Dar escala al vector de traslación 't' (unitario) usando la distancia real
        t_pair_scaled = t_pair_unit * BASELINE_METERS

        # --- PASO 2.C: Rectificar el par de imágenes ---
        # Usamos las imágenes escaladas, K escalada, D, y el R, t que acabamos de encontrar
        rectify_result = rectify_images(
            img_i_scaled, 
            img_d_scaled, 
            K_scaled, 
            D_orig, 
            R_pair, 
            t_pair_scaled # <-- Usamos el vector 't' escalado
        )
        
        if not rectify_result:
            print("   -> Advertencia: Falló la rectificación. Saltando par.")
            continue
            
        img_i_rect, img_d_rect, new_params = rectify_result
        
        # --- PASO 2.D: Crear la configuración de cámara RECTIFICADA ---
        config_camara_rect = create_config_from_rectify_params(new_params)
        
        if not config_camara_rect:
            print("   -> Advertencia: Falló el cálculo de parámetros rectificados (baseline negativo?). Saltando par.")
            continue
            
        print(f"   -> Parámetros rectificados (Baseline: {config_camara_rect.baseline:.4f}m, Fx: {config_camara_rect.fx:.2f})")

        # --- PASO 2.E: Calcular el mapa de disparidad ---
        print("   -> Calculando mapa de disparidad...")
        mapa_disparidad, mapa_error = calcular_mapa_disparidad(
            img_i_rect, img_d_rect, RADIO_VENTANA, RADIO_BUSQUEDA
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
        print(f"   -> Mapas de disparidad y error guardados en '{RUTA_DISPARIDAD}'")

        # --- PASO 2.F: Reconstrucción 3D ---
        print(f"   -> Iniciando reconstrucción 3D para '{nombre_salida_base}'...")
        point_cloud = reconstruct_3d_from_disparity(mapa_disparidad, config_camara_rect)

        if point_cloud.size == 0:
            print(
                "    -> Advertencia: La reconstrucción no generó puntos. (¿Mapa de disparidad vacío?)"
            )
            continue

        ruta_salida_ply = os.path.join(RUTA_RECONSTRUCCION, f"{nombre_salida_base}.ply")

        save_point_cloud_to_ply(point_cloud, ruta_salida_ply)
        print(f" {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}:   -> Nube de puntos 3D guardada en '{ruta_salida_ply}'")

    end_proceso = time.time()
    print("-" * 50)
    print(
        f"Tiempo total de procesamiento: {end_proceso - start_proceso:.2f} segundos"
    )
    print("Proceso completado.")