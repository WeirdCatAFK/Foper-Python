
import numpy as np

def fitness(pob: np.ndarray, franja1: np.ndarray, franja2: np.ndarray, tam_ventana: int, peso_suavidad: float) -> np.ndarray:
    """
    Calcula la aptitud (fitness) para cada individuo en la población.
    Una puntuación más baja es mejor.

    Args:
        pob: La población de individuos (cromosomas de disparidad).
        franja1: La franja de la imagen izquierda.
        franja2: La franja de la imagen derecha.
        tam_ventana: El radio de la ventana de comparación (SAD).
        peso_suavidad: Factor de ponderación para el coste de suavidad.

    Returns:
        Un array de numpy con la puntuación de fitness para cada individuo.
    """
    tam_pob, w = pob.shape
    h_franja = franja1.shape[0]
    evaluacion = np.zeros(tam_pob)

    # --- Vectorización del Coste de Suavidad (coste2) ---
    # Calcula la diferencia absoluta entre genes adyacentes para toda la población
    coste_suavidad = np.sum(np.abs(pob[:, 1:] - pob[:, :-1]), axis=1)

    # --- Cálculo semi-vectorizado del Coste Fotométrico (coste1) ---
    # Convertir franjas a float32 para cálculos de SAD para evitar overflow de uint8
    franja1_f = franja1.astype(np.float32)
    franja2_f = franja2.astype(np.float32)
    
    # El bucle externo sobre la población es difícil de vectorizar sin un uso masivo de memoria.
    # El bucle interno sobre los píxeles de la fila está optimizado.
    for i in range(tam_pob):
        d = pob[i, :] # Vector de disparidad para el individuo i
        coste_foto_total = 0.0
        
        # Itera a lo largo del cromosoma (fila de la imagen)
        for j in range(tam_ventana, w - tam_ventana - np.max(d)):
            # Extrae la ventana de la imagen izquierda
            ventana1 = franja1_f[:, j - tam_ventana : j + tam_ventana + 1]
            
            # Calcula la posición de la ventana en la imagen derecha
            disp = d[j]
            j_derecha = j + disp
            
            # Extrae la ventana de la imagen derecha
            ventana2 = franja2_f[:, j_derecha - tam_ventana : j_derecha + tam_ventana + 1]
            
            # Suma de Diferencias Absolutas (SAD)
            sad = np.sum(np.abs(ventana1 - ventana2))
            coste_foto_total += sad
            
        evaluacion[i] = coste_foto_total + peso_suavidad * coste_suavidad[i]

    return evaluacion
