import numpy as np
from dataclasses import dataclass
from reconstruction import CameraConfig, reconstruct_3d_from_disparity, save_point_cloud_to_ply

"""
Este módulo proporciona funciones para reconstruir una nube de puntos 3D a partir de un mapa de disparidad utilizando los parámetros de una cámara estéreo.

Para utilizar este módulo en otro script, primero debes importar el objeto de configuración `CameraConfig` y definir los parámetros de tu cámara. Luego, sigue este orden de llamadas:

1. Crea una instancia de `CameraConfig` con los parámetros intrínsecos y extrínsecos de tu cámara.
2. Obtén o genera un mapa de disparidad (matriz 2D de tipo float).
3. Llama a la función `reconstruct_3d_from_disparity(disparity_map, config)` para obtener la nube de puntos 3D.
4. Llama a la función `save_point_cloud_to_ply(points, filename)` para guardar la nube de puntos en un archivo PLY.

Ejemplo de uso:

    config = CameraConfig(fx=..., fy=..., cx=..., cy=..., baseline=...)
    disparity_map = ...  # Cargar o calcular el mapa de disparidad
    points_3d = reconstruct_3d_from_disparity(disparity_map, config)
    save_point_cloud_to_ply(points_3d, 'output.ply')
"""

@dataclass
class CameraConfig:
    """
    Almacena los parámetros intrínsecos y extrínsecos de una configuración de cámara estéreo.
    """
    # Matriz intrínseca (K)
    fx: float  # Distancia focal en el eje x (en píxeles)
    fy: float  # Distancia focal en el eje y (en píxeles)
    cx: float  # Punto principal en x (centro óptico)
    cy: float  # Punto principal en y (centro óptico)

    # Parámetro extrínseco principal para estéreo
    baseline: float  # Distancia entre los centros de las dos cámaras (en metros)

def reconstruct_3d_from_disparity(disparity_map: np.ndarray, config: CameraConfig) -> np.ndarray:
    """
    Reconstruye una nube de puntos 3D a partir de un mapa de disparidad utilizando el método de triangulación.

    Args:
        disparity_map: Matriz 2D (H, W) de NumPy con los valores de disparidad.
        config: Objeto CameraConfig con los parámetros de la cámara.

    Returns:
        Una matriz de NumPy de forma (N, 3) que representa la nube de puntos 3D,
        donde N es el número de puntos válidos.
    """
    h, w = disparity_map.shape
    
    # Crear una máscara para ignorar disparidades inválidas (cero o negativas)
    valid_mask = disparity_map > 0

    # Calcular la profundidad (coordenada Z) para todos los píxeles válidos a la vez.
    # La fórmula fundamental es: Z = (focal_length * baseline) / disparity
    Z = np.zeros_like(disparity_map, dtype=float)
    Z[valid_mask] = (config.fx * config.baseline) / disparity_map[valid_mask]

    # Crear una malla de coordenadas de píxeles (u, v)
    u_coords = np.arange(w)
    v_coords = np.arange(h)
    u_grid, v_grid = np.meshgrid(u_coords, v_coords)

    # Calcular las coordenadas X e Y usando las ecuaciones del modelo de cámara estenopeica (pinhole)
    # X = (u - cx) * Z / fx
    # Y = (v - cy) * Z / fy
    X = (u_grid - config.cx) * Z / config.fx
    Y = (v_grid - config.cy) * Z / config.fy

    # Apilar las coordenadas (X, Y, Z) en una sola matriz
    points_3d = np.stack((X, Y, Z), axis=-1)

    # Filtrar solo los puntos 3D que corresponden a disparidades válidas
    valid_points = points_3d[valid_mask]

    return valid_points

def save_point_cloud_to_ply(points: np.ndarray, filename: str):
    """
    Guarda una nube de puntos en un archivo de formato PLY.

    Args:
        points: Matriz de NumPy de forma (N, 3) con los puntos 3D.
        filename: Nombre del archivo de salida (ej. 'nube_de_puntos.ply').
    """
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


if __name__ == '__main__':
    # --- 1. Configuración de Parámetros ---
    # Estos son valores de ejemplo. Debes reemplazarlos con los parámetros
    # reales de tu cámara, obtenidos a través de un proceso de calibración.
    config = CameraConfig(
        fx=800.0,
        fy=800.0,
        cx=320.0,
        cy=240.0,
        baseline=0.12  # 12 cm
    )

    # --- 2. Creación de una Matriz de Disparidad de Ejemplo ---
    # En un caso real, esta matriz sería la salida de un algoritmo de correspondencia estéreo
    # (ej. SGBM de OpenCV). Aquí, creamos un gradiente simple para la demostración.
    image_height, image_width = 480, 640
    disparity_map_example = np.zeros((image_height, image_width), dtype=np.float32)
    
    # Simula un plano inclinado: la disparidad disminuye con la distancia (mayor u)
    gradient = np.linspace(64, 16, image_width)
    disparity_map_example[:, :] = gradient
    
    # Simula un objeto más cercano en el centro
    center_x, center_y = image_width // 2, image_height // 2
    disparity_map_example[center_y-50:center_y+50, center_x-50:center_x+50] = 96.0
    
    print(f"Mapa de disparidad de ejemplo creado con dimensiones: {disparity_map_example.shape}")

    # --- 3. Reconstrucción 3D ---
    print("Iniciando reconstrucción 3D...")
    point_cloud = reconstruct_3d_from_disparity(disparity_map_example, config)
    print(f"Reconstrucción completa. Se generaron {len(point_cloud)} puntos 3D.")

    # --- 4. Guardado de la Nube de Puntos ---
    output_filename = 'nube_de_puntos.ply'
    save_point_cloud_to_ply(point_cloud, output_filename)
