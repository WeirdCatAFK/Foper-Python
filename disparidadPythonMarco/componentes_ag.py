
import numpy as np

def inicializacion(tam_pob: int, w: int, max_disp: int) -> np.ndarray:
    """
    Crea la población inicial de individuos (cromosomas).

    Args:
        tam_pob: Tamaño de la población (número de individuos).
        w: Ancho de la franja de la imagen (longitud del cromosoma).
        max_disp: Disparidad máxima, para definir el rango de los genes.

    Returns:
        Una matriz de numpy (población) donde cada fila es un cromosoma
        con valores de disparidad enteros aleatorios.
    """
    return np.random.randint(0, max_disp + 1, size=(tam_pob, w), dtype=np.int16)

def seleccion(pob: np.ndarray, ev: np.ndarray, tam_padres: int) -> tuple[np.ndarray, np.ndarray]:
    """
    Selecciona los mejores individuos de la población para ser padres.
    Utiliza una estrategia de selección por elitismo (truncamiento).

    Args:
        pob: La población actual.
        ev: El vector de evaluación (fitness) para la población.
        tam_padres: El número de padres a seleccionar.

    Returns:
        Una tupla conteniendo la sub-población de padres y sus evaluaciones.
    """
    # Ordena las evaluaciones de menor a mayor (mejor a peor) y obtiene los índices
    indices_ordenados = np.argsort(ev)
    
    # Selecciona los mejores 'tam_padres' individuos
    indices_padres = indices_ordenados[:tam_padres]
    
    padres = pob[indices_padres]
    ev_padres = ev[indices_padres]
    
    return padres, ev_padres

def cruzamiento(padres: np.ndarray, tam_hijos: int) -> np.ndarray:
    """
    Crea hijos a partir de la población de padres usando cruce de un solo punto.

    Args:
        padres: La población de padres seleccionados.
        tam_hijos: El número de hijos a crear.

    Returns:
        La nueva población de hijos.
    """
    num_padres, w = padres.shape
    hijos = np.empty((tam_hijos, w), dtype=np.int16)
    
    # Puntos de cruce aleatorios para todos los hijos a la vez
    puntos_cruce = np.random.randint(1, w, size=tam_hijos)
    
    # Índices de padres aleatorios para todos los hijos
    idx_padre1 = np.random.randint(0, num_padres, size=tam_hijos)
    idx_padre2 = np.random.randint(0, num_padres, size=tam_hijos)
    
    for i in range(tam_hijos):
        padre1 = padres[idx_padre1[i]]
        padre2 = padres[idx_padre2[i]]
        pto = puntos_cruce[i]
        hijos[i, :pto] = padre1[:pto]
        hijos[i, pto:] = padre2[pto:]
        
    return hijos

def mutacion(hijos: np.ndarray, max_disp: int, prob_mut: float) -> np.ndarray:
    """
    Aplica una mutación a la población de hijos.
    Cada gen tiene una probabilidad `prob_mut` de ser reemplazado por un
    valor aleatorio.

    Args:
        hijos: La población de hijos.
        max_disp: Disparidad máxima para generar nuevos genes.
        prob_mut: Probabilidad de mutación de un gen.

    Returns:
        La población de hijos mutada.
    """
    # Crea una máscara booleana donde la mutación debe ocurrir
    mascara_mutacion = np.random.rand(*hijos.shape) < prob_mut
    
    # Genera nuevos valores aleatorios solo para los genes que van a mutar
    num_mutaciones = np.sum(mascara_mutacion)
    nuevos_genes = np.random.randint(0, max_disp + 1, size=num_mutaciones, dtype=np.int16)
    
    # Aplica la mutación usando la máscara
    hijos[mascara_mutacion] = nuevos_genes
    
    return hijos
