import numpy as np
from numba import njit, prange
from dataclasses import dataclass
import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv
# --- NUEVAS IMPORTACIONES ---
# Importar las funciones necesarias de 'rectify.py'
# Usamos importación relativa .rectify
try:
    from .rectify import load_calibration_data, scale_camera_matrix
except ImportError:
    # Fallback para si se ejecuta como script principal
    from rectify import load_calibration_data, scale_camera_matrix

@dataclass
class CameraConfig:
    """Intrinsic and extrinsic parameters of a stereo camera."""
    fx: float
    fy: float
    cx: float
    cy: float
    baseline: float

@njit(parallel=True, fastmath=True)
def reconstruct_3d_from_disparity_numba(disparity_map, fx, fy, cx, cy, baseline):
    """
    Parallelized calculation of 3D coordinates from the disparity map.

    Args:
        disparity_map : 2D matrix with disparity values (>0)
        fx, fy, cx, cy, baseline : Camera parameters

    Returns:
        np.ndarray : (N, 3) matrix with 3D coordinates (X, Y, Z)
    """
    h, w = disparity_map.shape
    count = 0

    for v in prange(h):
        for u in range(w):
            if disparity_map[v, u] > 0:
                count += 1

    points = np.zeros((count, 3), dtype=np.float64)
    idx = 0

    for v in prange(h):
        for u in range(w):
            d = disparity_map[v, u]
            if d > 0:
                Z = (fx * baseline) / d
                X = (u - cx) * Z / fx
                Y = (v - cy) * Z / fy
                points[idx, 0] = X
                points[idx, 1] = Y
                points[idx, 2] = Z
                idx += 1

    return points


def reconstruct_3d_from_disparity(disparity_map: np.ndarray, config: CameraConfig) -> np.ndarray:
    """
    Reconstructs a 3D point cloud from a disparity map.
    """
    points = reconstruct_3d_from_disparity_numba(
        disparity_map,
        config.fx, config.fy,
        config.cx, config.cy,
        config.baseline
    )

    if points.size == 0:
        # Changed to return empty array instead of raising error,
        # to allow main loop to continue.
        return np.array([], dtype=np.float64).reshape(0, 3)
        
    points = points[~np.isnan(points).any(axis=1)]
    points = points[~np.isinf(points).any(axis=1)]

    return points

def save_point_cloud_to_ply(points, filename):
    """
    Saves a set of XYZ points in PLY format (ASCII).
    If colors do not exist, they are assigned based on normalized Z height.
    """
    points = np.asarray(points, dtype=np.float64)

    # --- Color Generation (based on normalized Z) ---
    # Centering and normalization is *only* for color calculation.
    centroid = points.mean(axis=0)
    points_centered = points - centroid
    max_range = np.abs(points_centered).max()
    # Add epsilon to avoid division by zero if max_range is 0 (e.g., single point)
    points_norm = points_centered / (max_range + 1e-8)

    z_norm = (points_norm[:, 2] - points_norm[:, 2].min()) / (np.ptp(points_norm[:, 2]) + 1e-8)
    colors = (z_norm * 255).astype(np.uint8)
    colors_rgb = np.stack([colors, 255 - colors, (colors // 2)], axis=1)
    
    # --- PLY Header ---
    n_points = points.shape[0]
    header = [
        "ply",
        "format ascii 1.0",
        f"element vertex {n_points}",
        "property float x",
        "property float y",
        "property float z",
        "property uchar red",
        "property uchar green",
        "property uchar blue",
        "end_header\n"
    ]

    # --- Write Data ---
    # **CRITICAL FIX**: We write the original 'points', not 'points_norm'.
    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(header))
        # Zip the *original* 3D points with the calculated colors
        for (x, y, z), (r, g, b) in zip(points, colors_rgb):
            f.write(f"{x:.6f} {y:.6f} {z:.6f} {r} {g} {b}\n")

    print(f"File saved successfully to '{filename}' with {n_points} points.")


if __name__ == '__main__':
    print("Este script ('reconstruction.py') no está pensado para ser ejecutado directamente.")
    print("Ejecutando bloque de PRUEBA...")
    
    # Kept the old test code logic just in case, but walled it off.
    run_test = True
    if run_test:
        load_dotenv()
        ESCALA = float(os.getenv("ESCALA_DE_PROCESAMIENTO", 1.0)) 

        # --- MODIFICACIÓN ---
        # Cargar desde RUTA_CALIBRACION y BASELINE_METERS en .env
        RUTA_CALIBRACION = os.getenv("RUTA_CALIBRACION")
        # Usar 0.5 como fallback si no está definido
        BASELINE_METERS = float(os.getenv("BASELINE_METERS", 0.5)) 

        try:
            if not RUTA_CALIBRACION or not os.path.exists(RUTA_CALIBRACION):
                raise FileNotFoundError(f"No se encontró RUTA_CALIBRACION ('{RUTA_CALIBRACION}') en .env o el archivo no existe.")
            
            print(f"Cargando calibración desde: {RUTA_CALIBRACION}")
            K_orig, D_orig = load_calibration_data(RUTA_CALIBRACION)
            K_scaled = scale_camera_matrix(K_orig, ESCALA)

            config = CameraConfig(
                fx = K_scaled[0, 0],
                fy = K_scaled[1, 1],
                cx = K_scaled[0, 2],
                cy = K_scaled[1, 2],
                baseline = BASELINE_METERS 
            )
            print("✓ Configuración de cámara de prueba cargada desde JSON y .env.")
            
        except Exception as e:
            print(f"❌ ERROR: No se pudieron cargar los parámetros: {e}")
            print("   Asegúrate de que RUTA_CALIBRACION y BASELINE_METERS estén en tu .env")
            print("   Usando configuración de fallback...")
            config = CameraConfig(fx=1000, fy=1000, cx=500, cy=500, baseline=0.5)

        # Corregido el typo de 'dispararidad' a 'disparidad'
        testPath = "./resultados/disparidad/TomaA-TomaB.error.npy"
        if testPath and os.path.exists(testPath):
            disparity_map = np.load(testPath)
            print(f"Disparity map loaded from: {testPath} ({disparity_map.shape})")
        else:
            print(f"⚠ Warning: Disparity file not found: {testPath}")
            # Usar valores de K_scaled para un mapa sintético más realista
            image_height = int(config.cy * 2) 
            image_width = int(config.cx * 2)
            print(f"Creating synthetic disparity map... ({image_height}, {image_width})")
            disparity_map = np.zeros((image_height, image_width), dtype=np.float32)
            gradient = np.linspace(64, 16, image_width)
            disparity_map[:, :] = gradient
            cx, cy = int(config.cx), int(config.cy)
            disparity_map[cy-50:cy+50, cx-50:cx+50] = 96.0

        print("Starting 3D reconstruction...")
        point_cloud = reconstruct_3d_from_disparity(disparity_map, config)
        print(f"Reconstruction complete. {len(point_cloud)} 3D points generated.")

        output_filename = 'nube_de_puntos_TEST.ply'
        save_point_cloud_to_ply(point_cloud, output_filename)