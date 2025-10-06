
import numpy as np
from componentes_ag import inicializacion, seleccion, cruzamiento, mutacion
from evaluacion import fitness

def motor_genetico(franja1: np.ndarray, franja2: np.ndarray, max_disp: int, 
                   tam_pob: int, num_gen: int, tam_ventana: int, 
                   prob_mut: float, peso_suavidad: float) -> np.ndarray:
    """
    Motor principal del algoritmo genético que opera sobre una única franja de imagen.

    Args:
        franja1: Franja de la imagen izquierda.
        franja2: Franja de la imagen derecha.
        max_disp: Disparidad máxima.
        tam_pob: Tamaño de la población.
        num_gen: Número de generaciones.
        tam_ventana: Radio de la ventana de comparación.
        prob_mut: Probabilidad de mutación.
        peso_suavidad: Factor de ponderación para el coste de suavidad.

    Returns:
        El mejor cromosoma (vector de disparidad) encontrado después de todas las generaciones.
    """
    h, w = franja1.shape
    
    # Definir cuántos padres e hijos habrá
    num_padres = tam_pob // 2
    num_hijos = tam_pob - num_padres

    # 1. Inicialización
    pob = inicializacion(tam_pob, w, max_disp)

    # Bucle principal de generaciones
    for generacion in range(num_gen):
        # 2. Evaluación
        ev = fitness(pob, franja1, franja2, tam_ventana, peso_suavidad)

        # 3. Selección (Elitismo)
        padres, ev_padres = seleccion(pob, ev, num_padres)

        # 4. Cruzamiento
        hijos = cruzamiento(padres, num_hijos)

        # 5. Mutación
        hijos = mutacion(hijos, max_disp, prob_mut)
        
        # 6. Nueva población
        # Evaluar solo a los nuevos hijos
        ev_hijos = fitness(hijos, franja1, franja2, tam_ventana, peso_suavidad)
        
        # La nueva población se compone de los mejores padres y los nuevos hijos
        pob = np.vstack((padres, hijos))
        ev = np.concatenate((ev_padres, ev_hijos))

    # Al final de todas las generaciones, encontrar el mejor individuo de la población final
    indice_mejor = np.argmin(ev)
    mejor_individuo = pob[indice_mejor]
    
    return mejor_individuo
