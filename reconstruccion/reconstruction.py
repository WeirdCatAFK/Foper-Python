import numpy as np
from numba import njit, prange
from dataclasses import dataclass
import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv

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
        raise ValueError("No valid points were generated.")
    points = points[~np.isnan(points).any(axis=1)]
    points = points[~np.isinf(points).any(axis=1)]

    return points

def save_point_cloud_to_ply(points, filename):
    """
    Saves a set of XYZ points in PLY format (ASCII).
    If colors do not exist, they are assigned based on normalized Z height.
    """
    points = np.asarray(points, dtype=np.float64)

    centroid = points.mean(axis=0)
    points_centered = points - centroid
    max_range = np.abs(points_centered).max()
    points_norm = points_centered / (max_range + 1e-8)

    z_norm = (points_norm[:, 2] - points_norm[:, 2].min()) / (np.ptp(points_norm[:, 2]) + 1e-8)
    colors = (z_norm * 255).astype(np.uint8)
    colors_rgb = np.stack([colors, 255 - colors, (colors // 2)], axis=1)

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

    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(header))
        for (x, y, z), (r, g, b) in zip(points, colors_rgb):
            f.write(f"{x:.6f} {y:.6f} {z:.6f} {r} {g} {b}\n")

    print(f"File saved successfully to '{filename}' with {n_points} points.")


if __name__ == '__main__':
    load_dotenv()
    ESCALA = float(os.getenv("ESCALA_DE_PROCESAMIENTO")) # Get the same scale

    config = CameraConfig(
        fx = 5963.9 * ESCALA,
        fy = 5952.8 * ESCALA,
        cx = 3808.0 * ESCALA,
        cy = 2139.4 * ESCALA,
        baseline = 0.12 
    )

    testPath = "./resultados/disparidad/TestEscala1a1A.npy"
    if testPath and os.path.exists(testPath):
        disparity_map = np.load(testPath)
        print(f"Disparity map loaded from: {testPath} ({disparity_map.shape})")
    else:
        image_height, image_width = 480, 640
        disparity_map = np.zeros((image_height, image_width), dtype=np.float32)

        gradient = np.linspace(64, 16, image_width)
        disparity_map[:, :] = gradient

        cx, cy = image_width // 2, image_height // 2
        disparity_map[cy-50:cy+50, cx-50:cx+50] = 96.0
        print(f"Example disparity map created with dimensions: {disparity_map.shape}")

    print("Starting 3D reconstruction...")
    point_cloud = reconstruct_3d_from_disparity(disparity_map, config)
    print(f"Reconstruction complete. {len(point_cloud)} 3D points generated.")

    output_filename = 'nube_de_puntos.ply'
    save_point_cloud_to_ply(point_cloud, output_filename)
    print(f"Point cloud saved to: {output_filename}")