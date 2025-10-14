import numpy as np
import math

try:
    from .operadores_geneticos import inicializacion, seleccion, cruzamiento, mutar
    from .codificacion import cod_inv_pts, cod_inv
    from .evaluacion import evaluacion_poblacion
except ImportError:
    from operadores_geneticos import inicializacion, seleccion, cruzamiento, mutar
    from codificacion import cod_inv_pts, cod_inv
    from evaluacion import evaluacion_poblacion



def genetico(a, b, epsilon, n_generaciones, n_individuos, prob_mutacion, r_paciencia, imi, imd, X_coords, Y_coords, It_plantilla):
    """
    Algoritmo genético. Ahora recibe los arrays de datos directamente.
    """
    m = [0, 0]
    m[0] = math.ceil(math.log2((b[0] - a[0]) / epsilon)) if (b[0] - a[0]) > 0 else 1
    m[1] = math.ceil(math.log2((b[1] - a[1]) / epsilon)) if (b[1] - a[1]) > 0 else 1
    
    # Se asegura que pot1 y pot2 tengan el mismo dtype que los puntos (int32)
    # Sin embargo, para evitar overflows en np.dot, los mantenemos en int64 y
    # hacemos la conversión dentro de la función `cod_inv`
    pot1 = 2**np.arange(m[0] - 1, -1, -1, dtype=np.int64)
    pot2 = 2**np.arange(m[1] - 1, -1, -1, dtype=np.int64)

    # Inicialización
    puntos = inicializacion(np.array(a), np.array(b), epsilon, np.array(m), n_individuos)
    
    mejor_sol_global = np.inf
    mejor_individuo_coords = [0.0, 0.0]
    generaciones_sin_mejora = 0

    # Bucle principal
    for i in range(n_generaciones):
        # Decodificar y Evaluar
        pts_reales = cod_inv_pts(puntos, np.array(a), np.array(b), epsilon, np.array(m), pot1, pot2)
        fitness = evaluacion_poblacion(pts_reales, imi, imd, X_coords, Y_coords, It_plantilla)
        
        mejor_sol_gen = np.nanmin(fitness)
        mejor_individuo_idx = np.nanargmin(fitness)

        # Actualizar mejor solución
        if mejor_sol_gen < mejor_sol_global:
            mejor_sol_global = mejor_sol_gen
            mejor_individuo_coords[0] = pts_reales[mejor_individuo_idx, 0]
            mejor_individuo_coords[1] = pts_reales[mejor_individuo_idx, 1]
            generaciones_sin_mejora = 0
        else:
            generaciones_sin_mejora += 1
            
        # Reiniciar si se estanca
        if generaciones_sin_mejora > r_paciencia:
            puntos = inicializacion(np.array(a), np.array(b), epsilon, np.array(m), n_individuos)
            generaciones_sin_mejora = 0
            
        # Operadores genéticos
        indices_seleccionados = seleccion(puntos, fitness)
        puntos = puntos[indices_seleccionados, :]
        puntos = cruzamiento(puntos)
        puntos = mutar(puntos, prob_mutacion)

    return [mejor_individuo_coords[0], mejor_individuo_coords[1], mejor_sol_global]