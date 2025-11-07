import cv2
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
import multiprocessing
import os
from dotenv import load_dotenv
try:
    from .genetico import genetico
except ImportError:
    from genetico import genetico

load_dotenv()
NUCLEOS = int(os.getenv("NUCLEOS")) 

GENERACIONES = int(os.getenv("GENERACIONES"))
POBLACION = int(os.getenv("POBLACION"))

# ----------------------------------------------------------------------------
# PASO 1: Definir variables globales para los workers y la función init
# ----------------------------------------------------------------------------

# Estas variables serán 'None' en el proceso principal,
# pero contendrán las imágenes dentro de cada proceso del pool.
g_imi = None
g_imd = None

def init_worker(imi_compartida, imd_compartida):
    """
    Función de inicialización para cada proceso del pool.
    Guarda las imágenes en variables globales para ESE proceso.
    """
    global g_imi, g_imd
    g_imi = imi_compartida
    g_imd = imd_compartida


# ----------------------------------------------------------------------------
# PASO 2: Modificar la función "worker"
# ----------------------------------------------------------------------------
def _worker_procesar_ventana(args):
    """
    Función de trabajo para ser ejecutada en paralelo.
    Procesa una sola ventana (y, x).
    """
    # --- MODIFICADO ---
    # Accede a las imágenes desde las variables globales del worker
    global g_imi, g_imd

    # --- MODIFICADO ---
    # Desempaqueta los nuevos argumentos (más ligeros)
    (y, x, radio_ventana, radio_busqueda, ga_params) = args

    # Comprobación de seguridad
    if g_imi is None or g_imd is None:
        print("Error: Worker no inicializado correctamente.")
        return (y, x, np.nan, np.nan)

    try:
        # Lógica de cálculo (sin cambios)
        ry = np.arange(y - radio_ventana, y + radio_ventana + 1)
        rx = np.arange(x - radio_ventana, x + radio_ventana + 1)
        grid_x, grid_y = np.meshgrid(rx, ry)

        X_coords = grid_x.flatten().astype(np.float32)
        Y_coords = grid_y.flatten().astype(np.float32)
        
        # --- MODIFICADO ---
        # Usa la imagen global 'g_imi'
        It_plantilla = g_imi[Y_coords.astype(int), X_coords.astype(int)]

        sol = genetico(
            a=[-radio_busqueda, -radio_busqueda],
            b=[+radio_busqueda, +radio_busqueda],
            epsilon=1,
            **ga_params,
            # --- MODIFICADO ---
            # Pasa las imágenes globales a la función 'genetico'
            imi=g_imi,
            imd=g_imd,
            X_coords=X_coords,
            Y_coords=Y_coords,
            It_plantilla=It_plantilla,
        )

        return (y, x, sol[0], sol[2])

    except Exception as e:
        print(f"Error en worker (y={y}, x={x}): {e}")
        return (y, x, np.nan, np.nan)


def calcular_mapa_disparidad(img_izquierda, img_derecha, radio_ventana, radio_busqueda):
    """
    Calcula el mapa de disparidad horizontal (dx) llamando al pipeline optimizado
    utilizando multiprocessing.
    """
    print("Iniciando cálculo del mapa de disparidad (Paralelizado con Multiprocessing)...")

    imi = img_izquierda.astype(np.float32) / 255.0
    imd = img_derecha.astype(np.float32) / 255.0

    h, w = imi.shape
    mapa_disparidad_dx = np.full((h, w), np.nan)
    E = np.full((h, w), np.nan)

    y_range = range(radio_ventana, h - radio_ventana)
    x_range = range(radio_ventana, w - radio_ventana)

    ga_params = {
        'n_generaciones': GENERACIONES,
        'n_individuos': POBLACION,
        'prob_mutacion': 0.01,
        'r_paciencia': 5
    }
    print(f"Parámetros GA: {ga_params}")

    # ----------------------------------------------------------------------------
    # PASO 3: Preparar la lista de tareas (AHORA MUY LIGERA)
    # ----------------------------------------------------------------------------
    tasks = []
    for y in y_range:
        for x in x_range:
            # --- MODIFICADO ---
            # El 'task_args' ya NO contiene 'imi' e 'imd'
            # Es solo una tupla de números pequeños
            task_args = (
                y, x, radio_ventana, radio_busqueda, ga_params
            )
            tasks.append(task_args) # <-- Esta línea ahora es segura y no consume memoria

    if not tasks:
        print("No hay tareas para procesar.")
        return mapa_disparidad_dx, E

    total_tasks = len(tasks)
    print(f"Total de {total_tasks} ventanas a procesar en paralelo.")

    # ----------------------------------------------------------------------------
    # PASO 4: Crear el Pool con el 'initializer'
    # ----------------------------------------------------------------------------
    num_cores = NUCLEOS
    print(f"Creando un Pool con {num_cores} procesos...")
    
    results = []
    
    with multiprocessing.Pool(
        processes=num_cores,
        # --- ¡NUEVO! ---
        # Llama a 'init_worker' al crear cada proceso...
        initializer=init_worker,
        # ...y pásale estas imágenes como argumentos.
        initargs=(imi, imd)
    ) as pool:
        
        results = list(tqdm(
            pool.imap(
                _worker_procesar_ventana, 
                tasks, 
                chunksize=100
            ), 
            total=total_tasks, 
            desc="Procesando ventanas"
        ))

    # ----------------------------------------------------------------------------
    # PASO 5: Ensamblar resultados 
    # ----------------------------------------------------------------------------
    print("\nProcesamiento paralelo completado. Ensamblando mapas...")
    for y, x, dx, error in results:
        if (y >= 0 and y < h and x >= 0 and x < w):
            mapa_disparidad_dx[y, x] = dx
            E[y, x] = error

    print("Cálculo finalizado.")
    return mapa_disparidad_dx, E


# ---- Bloque de Pruebas ----
if __name__ == "__main__":
    try:
        img_i = cv2.imread("./resultados/imagenes/toma0.jpg", cv2.IMREAD_GRAYSCALE)
        img_d = cv2.imread("./resultados/imagenes/toma1.jpg", cv2.IMREAD_GRAYSCALE)
        if img_i is None or img_d is None:
            raise FileNotFoundError("Una o ambas imágenes de prueba no se encontraron.")
    except FileNotFoundError as e:
        print(f"Error: {e}")
    else:
        mapa_disparidad, mapa_error = calcular_mapa_disparidad(img_i, img_d, 15, 55)
        
        plt.figure(figsize=(12, 4))
        plt.subplot(1, 2, 1)
        plt.title("Mapa de Disparidad (Horizontal 'dx')")
        plt.imshow(mapa_disparidad, cmap="jet")
        plt.colorbar()
        plt.subplot(1, 2, 2)
        plt.title("Mapa de Error ")
        plt.imshow(mapa_error, cmap="jet")
        plt.colorbar()
        plt.show()