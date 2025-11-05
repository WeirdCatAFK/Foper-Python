import numpy as np
import math

# Importa las funciones optimizadas
try:
    from .operadores_geneticos import inicializacion, seleccion, cruzamiento, mutar
    from .codificacion import cod_inv_pts
    from .evaluacion import evaluacion_poblacion
except ImportError:
    from operadores_geneticos import inicializacion, seleccion, cruzamiento, mutar
    from codificacion import cod_inv_pts
    from evaluacion import evaluacion_poblacion

def genetico(a, b, epsilon, n_generaciones, n_individuos, prob_mutacion, r_paciencia,
             # Ya no se usa 'datos', se pasan los arrays directamente
             imi, imd, X_coords, Y_coords, It_plantilla):
    """
    Algoritmo genético. Llama a las funciones optimizadas con Numba.
    """
    m = [0, 0]
    m[0] = math.ceil(math.log2((b[0] - a[0]) / epsilon)) if (b[0] - a[0]) > 0 else 1
    m[1] = math.ceil(math.log2((b[1] - a[1]) / epsilon)) if (b[1] - a[1]) > 0 else 1
    
    # Asegura que potencias sean int64 para el bucle en cod_inv
    pot1 = 2**np.arange(m[0] - 1, -1, -1, dtype=np.int64)
    pot2 = 2**np.arange(m[1] - 1, -1, -1, dtype=np.int64)

    # 1. Inicialización (llama a la función JIT)
    puntos = inicializacion(np.array(a), np.array(b), epsilon, np.array(m), n_individuos)
    
    mejor_sol_global = np.inf
    mejor_individuo_coords = [0.0, 0.0]
    generaciones_sin_mejora = 0

    # 2. Bucle principal
    for i in range(n_generaciones):
        # Decodificar (llama a la función JIT)
        pts_reales = cod_inv_pts(puntos, np.array(a), np.array(b), epsilon, np.array(m), pot1, pot2)
        
        # Evaluar (llama a la función JIT)
        fitness = evaluacion_poblacion(pts_reales, imi, imd, X_coords, Y_coords, It_plantilla)
        
        mejor_sol_gen = np.nanmin(fitness)
        mejor_individuo_idx = np.nanargmin(fitness)

        # 3. Actualizar mejor solución
        if mejor_sol_gen < mejor_sol_global:
            mejor_sol_global = mejor_sol_gen
            mejor_individuo_coords[0] = pts_reales[mejor_individuo_idx, 0]
            mejor_individuo_coords[1] = pts_reales[mejor_individuo_idx, 1]
            generaciones_sin_mejora = 0
        else:
            generaciones_sin_mejora += 1
            
        # 4. Reiniciar si se estanca
        if generaciones_sin_mejora > r_paciencia:
            puntos = inicializacion(np.array(a), np.array(b), epsilon, np.array(m), n_individuos)
            generaciones_sin_mejora = 0
            
        # 5. Operadores genéticos (llaman a funciones JIT internas)
        indices_seleccionados = seleccion(puntos, fitness)
        puntos = puntos[indices_seleccionados, :]
        puntos = cruzamiento(puntos)
        puntos = mutar(puntos, prob_mutacion)

    return [mejor_individuo_coords[0], mejor_individuo_coords[1], mejor_sol_global]