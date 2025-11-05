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
        return 0.0 # Devuelve 0 si está fuera de los límites

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

@njit(fastmath=True)
def fn_evaluacion(desplazamiento, imd, X_coords, Y_coords, It_plantilla):
    """
    Función de fitness, optimizada con Numba.
    Ya no usa el diccionario 'datos', recibe los arrays directamente.
    """
    dx, dy = desplazamiento
    h, w = imd.shape
    
    error_total = 0.0
    
    for i in range(len(X_coords)):
        # Coordenadas desplazadas
        xd = X_coords[i] + dx
        yd = Y_coords[i] + dy
        
        # Validación de límites (reemplaza la interpolación con fill_value=0)
        if xd < 0 or xd >= w-1 or yd < 0 or yd >= h-1:
            intensidad_desplazada = 0.0
        else:
            # Obtener intensidad con interpolación
            intensidad_desplazada = bilinear_interp(imd, xd, yd)
        
        error_total += np.abs(It_plantilla[i] - intensidad_desplazada)
        
    return error_total / len(X_coords)

@njit(fastmath=True)
def evaluacion_poblacion(puntos_reales, imi, imd, X_coords, Y_coords, It_plantilla):
    """
    Evalúa una población completa. (Compilado con Numba)
    """
    fitness = np.zeros(puntos_reales.shape[0])
    for i in range(puntos_reales.shape[0]):
        fitness[i] = fn_evaluacion(puntos_reales[i], imd, X_coords, Y_coords, It_plantilla)
    return fitness