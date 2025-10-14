import numpy as np
from numba import njit

@njit
def bilinear_interp(image, x, y):
    """
    Interpolación bilineal manual para ser compilada con Numba.
    """
    h, w = image.shape
    x1, y1 = int(x), int(y)
    x2, y2 = x1 + 1, y1 + 1

    # Comprobar límites
    if x1 < 0 or x2 >= w or y1 < 0 or y2 >= h:
        return 0.0

    # Píxeles circundantes
    q11 = image[y1, x1]
    q21 = image[y1, x2]
    q12 = image[y2, x1]
    q22 = image[y2, x2]

    # Pesos de interpolación
    dx1, dy1 = x - x1, y - y1
    dx2, dy2 = 1.0 - dx1, 1.0 - dy1

    # Interpolar
    return q11 * dx2 * dy2 + q21 * dx1 * dy2 + q12 * dx2 * dy1 + q22 * dx1 * dy1

@njit
def fn_evaluacion(desplazamiento, imi, imd, X_coords, Y_coords, It_plantilla):
    """
    Función de fitness, optimizada con Numba.
    Ya no usa el diccionario 'datos'.
    """
    dx, dy = desplazamiento
    h, w = imi.shape
    
    error_total = 0.0
    
    for i in range(len(X_coords)):
        # Coordenadas desplazadas
        xd = X_coords[i] + dx
        yd = Y_coords[i] + dy
        
        # Validación de límites
        if xd < 0 or xd >= w or yd < 0 or yd >= h:
            return np.inf  # Penalización alta si está fuera

        # Obtener intensidad con interpolación y calcular error
        intensidad_desplazada = bilinear_interp(imd, xd, yd)
        error_total += np.abs(It_plantilla[i] - intensidad_desplazada)
        
    return error_total / len(X_coords)

@njit
def evaluacion_poblacion(puntos_reales, imi, imd, X_coords, Y_coords, It_plantilla):
    """
    Evalúa una población completa. (Compilado con Numba)
    """
    fitness = np.zeros(puntos_reales.shape[0])
    for i in range(puntos_reales.shape[0]):
        fitness[i] = fn_evaluacion(puntos_reales[i], imi, imd, X_coords, Y_coords, It_plantilla)
    return fitness