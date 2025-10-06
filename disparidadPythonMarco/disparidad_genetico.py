
import numpy as np
from tqdm import tqdm
from genetico import motor_genetico

def calcular_disparidad_genetico(i1: np.ndarray, i2: np.ndarray, tam_ventana: int, max_disp: int) -> np.ndarray:
    """
    Orquestador principal para calcular el mapa de disparidad usando el algoritmo genético.

    Args:
        i1: Imagen izquierda completa (matriz numpy 2D, uint8).
        i2: Imagen derecha completa (matriz numpy 2D, uint8).
        tam_ventana: Radio de la ventana de comparación.
        max_disp: Disparidad máxima.

    Returns:
        El mapa de disparidad completo (matriz numpy 2D).
    """
    h, w = i1.shape
    d_map = np.zeros_like(i1, dtype=np.int16)
    
    # Parámetros del Algoritmo Genético (pueden ser ajustados)
    TAM_POB = 50
    NUM_GEN = 100
    PROB_MUT = 0.1
    PESO_SUAVIDAD = 10.0 # Equivalente al 10*coste2 en el código MATLAB
    
    # Altura de la franja a procesar
    h_franja = 2 * tam_ventana + 1

    # tqdm proporciona una barra de progreso visualmente agradable
    print("Calculando mapa de disparidad con Algoritmo Genético...")
    for i in tqdm(range(tam_ventana, h - tam_ventana)):
        # Definir los límites de la franja actual
        fila_inicio = i - tam_ventana
        fila_fin = i + tam_ventana + 1
        
        # Extraer las franjas de las imágenes
        franja1 = i1[fila_inicio:fila_fin, :]
        franja2 = i2[fila_inicio:fila_fin, :]
        
        # Ejecutar el motor genético para esta franja
        vector_disparidad = motor_genetico(
            franja1, franja2, max_disp, 
            tam_pob=TAM_POB, num_gen=NUM_GEN, 
            tam_ventana=tam_ventana, prob_mut=PROB_MUT, 
            peso_suavidad=PESO_SUAVIDAD
        )
        
        # Asignar el vector resultante a la fila correspondiente en el mapa de disparidad
        d_map[i, :] = vector_disparidad

    return d_map
