import numpy as np
from dataclasses import dataclass

@dataclass
class StereoPairConfig:
    """
    Almacena la configuración completa para un par de cámaras estéreo en el caso general.
    """
    K1: np.ndarray  # Matriz intrínseca de la cámara 1
    K2: np.ndarray  # Matriz intrínseca de la cámara 2
    R: np.ndarray   # Matriz de rotación que transforma puntos del sistema de la cámara 1 al 2
    T: np.ndarray   # Vector de traslación que transforma puntos del sistema de la cámara 1 al 2

def save_point_cloud_to_ply(points: np.ndarray, filename: str):
    """
    Guarda una nube de puntos en un archivo de formato PLY.
    """
    # Asegurarse de que points es una lista de listas o una matriz 2D
    if points.ndim == 1:
        points = np.array([points])
        
    with open(filename, 'w') as f:
        f.write("ply\n")
        f.write("format ascii 1.0\n")
        f.write(f"element vertex {len(points)}\n")
        f.write("property float x\n")
        f.write("property float y\n")
        f.write("property float z\n")
        f.write("end_header\n")
        np.savetxt(f, points, fmt='%f %f %f')
    print(f"Nube de puntos guardada en '{filename}'")

def triangulate_point_vectorial(pt1: np.ndarray, pt2: np.ndarray, config: StereoPairConfig) -> np.ndarray:
    """
    Triangula un punto 3D a partir de dos correspondencias de puntos 2D y los parámetros de las cámaras.

    Este método implementa la "triangulación pura" encontrando el punto medio del segmento
    de línea más corto que conecta los dos rayos de proyección en el espacio 3D.

    Args:
        pt1: Coordenada del punto en la imagen 1 (Forma: [u1, v1]).
        pt2: Coordenada del punto en la imagen 2 (Forma: [u2, v2]).
        config: Objeto StereoPairConfig con todos los parámetros de las cámaras.

    Returns:
        El punto 3D triangulado en el sistema de coordenadas de la cámara 1.
    """
    # --- Paso 1: Definir los rayos de proyección en el sistema de coordenadas del mundo (cámara 1) ---

    # La cámara 1 es el origen del mundo. Su centro es C1 = [0, 0, 0].
    # El rayo se obtiene al retroproyectar el punto de la imagen al espacio 3D.
    pt1_h = np.array([*pt1, 1.0])  # Punto en coordenadas homogéneas
    ray1_dir = np.linalg.inv(config.K1) @ pt1_h
    ray1_dir /= np.linalg.norm(ray1_dir) # Normalizar el vector director

    # La cámara 2 está rotada y trasladada. Su centro C2 se calcula a partir de R y T.
    # La transformación de mundo a cámara 2 es: X_c2 = R @ X_c1 + T
    # El centro de la cámara 2 (en su propio sistema) es [0,0,0]. Para encontrarlo en el sistema
    # del mundo (cámara 1), resolvemos: 0 = R @ C2_w + T  => C2_w = -R.T @ T
    C2 = -config.R.T @ config.T
    
    # El rayo de la cámara 2 también se retroproyecta, pero luego debe ser rotado
    # de vuelta al sistema de coordenadas del mundo (cámara 1).
    pt2_h = np.array([*pt2, 1.0])
    ray2_dir_cam2 = np.linalg.inv(config.K2) @ pt2_h
    ray2_dir = config.R.T @ ray2_dir_cam2 # Rotar el rayo al sistema del mundo
    ray2_dir /= np.linalg.norm(ray2_dir)

    # --- Paso 2: Encontrar los puntos más cercanos en cada rayo ---
    # Tenemos dos líneas en 3D: L1(s) = C1 + s*ray1_dir y L2(t) = C2 + t*ray2_dir
    # (donde C1 es el origen [0,0,0]).
    # Se resuelve un sistema de ecuaciones para encontrar s y t que minimizan la distancia.
    
    w0 = -C2 # Vector que conecta los orígenes de los rayos (C1 - C2)
    
    a = np.dot(ray1_dir, ray1_dir)
    b = np.dot(ray1_dir, ray2_dir)
    c = np.dot(ray2_dir, ray2_dir)
    d = np.dot(ray1_dir, w0)
    e = np.dot(ray2_dir, w0)
    
    denominator = a * c - b * b
    
    # Si el denominador es casi cero, los rayos son paralelos.
    if np.abs(denominator) < 1e-6:
        return None # No se puede triangular de forma única

    s = (b * e - c * d) / denominator
    t = (a * e - b * d) / denominator

    # --- Paso 3: Calcular el punto 3D como el punto medio del segmento más corto ---
    p1_on_ray = s * ray1_dir # C1 es el origen
    p2_on_ray = C2 + t * ray2_dir
    
    point_3d = (p1_on_ray + p2_on_ray) / 2.0
    
    return point_3d.flatten()


if __name__ == '__main__':
    # --- 1. Configuración de Cámaras (Caso General) ---
    # Se instancia el objeto de configuración con todos los parámetros necesarios.
    angle = np.deg2rad(10)
    config = StereoPairConfig(
        K1 = np.array([
            [800, 0, 320],
            [0, 800, 240],
            [0, 0, 1]
        ]),
        K2 = np.array([
            [810, 0, 330],
            [0, 810, 250],
            [0, 0, 1]
        ]),
        R = np.array([
            [np.cos(angle), 0, np.sin(angle)],
            [0, 1, 0],
            [-np.sin(angle), 0, np.cos(angle)]
        ]),
        T = np.array([[0.2], [0.05], [0.1]]) # Traslación de (20cm, 5cm, 10cm)
    )

    # --- 2. Puntos 2D Correspondientes (Ejemplo) ---
    # Para generar un ejemplo realista, definimos un punto 3D en el mundo
    # y lo proyectamos en ambas cámaras para encontrar sus correspondencias 2D.
    
    P_world = np.array([[0.5], [0.2], [2.0]]) # Punto 3D a 2m de distancia

    # Proyección en Cámara 1 (es el origen del mundo)
    p1_proj = config.K1 @ P_world
    p1 = (p1_proj / p1_proj[2])[:2].flatten() # Dividir por Z y tomar (u,v)
    
    # Proyección en Cámara 2
    P_cam2 = config.R @ P_world + config.T
    p2_proj = config.K2 @ P_cam2
    p2 = (p2_proj / p2_proj[2])[:2].flatten()

    print(f"Punto 3D de prueba (Ground Truth): {P_world.flatten()}")
    print(f"Punto 2D correspondiente en Imagen 1: {p1}")
    print(f"Punto 2D correspondiente en Imagen 2: {p2}")
    print("-" * 20)

    # --- 3. Triangulación del Punto 3D ---
    print("Iniciando triangulación vectorial...")
    triangulated_point = triangulate_point_vectorial(p1, p2, config)
    
    if triangulated_point is not None:
        print(f"Punto 3D Triangulado: {triangulated_point}")
        
        # Calcular el error de reconstrucción
        error = np.linalg.norm(P_world.flatten() - triangulated_point)
        print(f"Error de reconstrucción: {error:.6f} metros")

        # --- 4. Guardado del Punto 3D ---
        # (Se guarda un solo punto en este ejemplo)
        save_point_cloud_to_ply(triangulated_point, 'punto_triangulado.ply')
    else:
        print("No se pudo triangular el punto (rayos paralelos).")
