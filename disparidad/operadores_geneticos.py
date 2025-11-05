import numpy as np
from numba import njit

# Importa la función 'cod' ya optimizada
try:
    from .codificacion import cod
except ImportError:
    from codificacion import cod

@njit
def inicializacion(a, b, epsilon, m, n_individuos):
    """
    Genera una población inicial. (Compilado con Numba)
    """
    pts = np.zeros((n_individuos, m[0] + m[1]), dtype=np.int32)
    
    # Coordenadas aleatorias
    pts_reales_x = np.random.rand(n_individuos) * (b[0] - a[0]) + a[0]
    pts_reales_y = np.random.rand(n_individuos) * (b[1] - a[1]) + a[1]
    
    for i in range(n_individuos):
        dna_x = cod(a[0], b[0], epsilon, pts_reales_x[i], m[0])
        dna_y = cod(a[1], b[1], epsilon, pts_reales_y[i], m[1])
        pts[i, :] = np.concatenate((dna_x, dna_y))
        
    return pts

def seleccion(puntos, fitness):
    """
    Selecciona los mejores individuos. (np.argsort es rápido, no necesita Numba)
    """
    indices_ordenados = np.argsort(fitness)
    n_seleccionados = puntos.shape[0] // 2
    return indices_ordenados[:n_seleccionados]

@njit
def cruza(padre1, padre2):
    """ Operador de cruce. (Compilado con Numba) """
    hijo1 = np.zeros_like(padre1)
    for i in range(len(padre1)):
        if i % 2 == 0:
            hijo1[i] = padre2[i]
        else:
            hijo1[i] = padre1[i]
    return hijo1

def cruzamiento(puntos):
    """ Aplica cruce a la población. (Función envoltorio, no necesita Numba) """
    n_padres = puntos.shape[0]
    hijos = np.zeros_like(puntos)
    
    for i in range(n_padres - 1):
        hijos[i, :] = cruza(puntos[i, :], puntos[i + 1, :])
    hijos[-1, :] = cruza(puntos[-1, :], puntos[0, :])
    
    return np.vstack((puntos, hijos))

@njit
def mutacion(individuo, n_genes_a_mutar):
    """ Muta N genes en un individuo. (Compilado con Numba) """
    n_genes = len(individuo)
    indices = np.random.choice(n_genes, n_genes_a_mutar, replace=False)
    for i in indices:
        individuo[i] = 1 - individuo[i]
    return individuo

def mutar(puntos, prob_mutacion):
    """ Aplica mutación a la población. (Función envoltorio, no necesita Numba) """
    n_individuos = puntos.shape[0]
    n_a_mutar = int(n_individuos * prob_mutacion)
    indices_mut = np.random.choice(n_individuos, n_a_mutar, replace=False)
    
    for i in indices_mut:
        puntos[i, :] = mutacion(puntos[i, :], 4)
    return puntos