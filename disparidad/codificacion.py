import numpy as np
from numba import njit

@njit
def cod(a, b, epsilon, nc, n):
    """
    Codifica un número real en una representación binaria. (Compilado con Numba)
    """
    num = round((nc - a) / epsilon)
    r = np.zeros(n, dtype=np.int32)
    for i in range(n - 1, -1, -1):
        r[i] = num % 2
        num = num // 2
    return r

@njit
def cod_inv(a, b, epsilon, n, p):
    """
    Decodifica una representación binaria a un valor real. (Compilado con Numba)
    """
    decimal_val = 0
    for i in range(len(n)):
        decimal_val += n[i] * p[i]
        
    return a + epsilon * float(decimal_val)

@njit
def cod_inv_pts(puntos, a, b, epsilon, m, pot1, pot2):
    """
    Decodifica una población completa de puntos binarios a coordenadas reales. (Compilado con Numba)
    """
    n_puntos = puntos.shape[0]
    pts_reales = np.zeros((n_puntos, 2), dtype=np.float64)
    
    X_bits = puntos[:, :m[0]]
    Y_bits = puntos[:, m[0]:m[0] + m[1]]
    
    for i in range(n_puntos):
        pts_reales[i, 0] = cod_inv(a[0], b[0], epsilon, X_bits[i, :], pot1)
        pts_reales[i, 1] = cod_inv(a[1], b[1], epsilon, Y_bits[i, :], pot2)
        
    return pts_reales