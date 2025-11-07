import cv2
import numpy as np
import json
import os

def load_calibration_data(json_path):
    """
    Loads calibration data from the specified JSON file.
    """
    try:
        with open(json_path, 'r') as f:
            data = json.load(f)
        
        # Convert lists to NumPy arrays
        K = np.array(data['K'])
        D = np.array(data['dist'])
        
        # We only need K and D for SfM. R and t will be ignored.
        print(f"✓ Calibration data (K, D) loaded from '{json_path}'")
        return K, D

    except FileNotFoundError:
        print(f"❌ ERROR: Calibration file not found: '{json_path}'")
        exit(1)
    except KeyError as e:
        print(f"❌ ERROR: Calibration file is missing required key: {e}")
        exit(1)

def scale_camera_matrix(K, scale_factor):
    """
    Scales the intrinsic camera matrix (K) based on a scaling factor.
    This is crucial if processing is done on resized images.
    """
    if scale_factor == 1.0:
        return K
        
    # Create a scaling matrix
    S = np.array([
        [scale_factor, 0, 0],
        [0, scale_factor, 0],
        [0, 0, 1]
    ])
    
    # Scale K: K_new = S @ K
    K_scaled = S @ K
    
    print(f"✓ Camera matrix 'K' scaled by {scale_factor}")
    return K_scaled

# --- MODIFICACIÓN ---
# Esta función ahora toma las imágenes escaladas y los parámetros
# directamente, en lugar de cargar desde la ruta del archivo.
def rectify_images(img_left_scaled, img_right_scaled, K_scaled, D, R_pair, t_pair):
    """
    Performs stereo rectification on a pair of already-loaded, scaled images.
    
    Args:
        img_left_scaled: The first scaled, grayscale image.
        img_right_scaled: The second scaled, grayscale image.
        K_scaled: The scaled intrinsic matrix (K).
        D: The distortion coefficients.
        R_pair: The RELATIVE rotation matrix for this pair.
        t_pair: The RELATIVE translation vector for this pair.
        
    Returns:
        (img_left_rectified, img_right_rectified, new_params) or None
    """
    
    if img_left_scaled.shape != img_right_scaled.shape:
        print(f"❌ ERROR: Image dimensions do not match.")
        print(f"   Left: {img_left_scaled.shape} | Right: {img_right_scaled.shape}")
        return None

    h, w = img_left_scaled.shape
    image_size_rect = (w, h)
        
    # --- 1. Perform Stereo Rectification ---
    # We assume K1=K2 and D1=D2 as it's the same camera
    print("   -> Rectificando (cv2.stereoRectify)...")
    try:
        R1, R2, P1, P2, Q, roi1, roi2 = cv2.stereoRectify(
            cameraMatrix1=K_scaled,
            distCoeffs1=D,
            cameraMatrix2=K_scaled,
            distCoeffs2=D,
            imageSize=image_size_rect,
            R=R_pair,
            T=t_pair,
            flags=cv2.CALIB_ZERO_DISPARITY, # Aligns principal points
            alpha=-1 # Default, zooms to show all valid pixels
        )
    except cv2.error as e:
        print(f"    -> ⚠ Advertencia: cv2.stereoRectify falló: {e}")
        return None
    
    print("   -> Rectificación calculada.")

    # --- 2. Create and apply rectification maps ---
    print("   -> Generando mapas de rectificación...")
    map_left_x, map_left_y = cv2.initUndistortRectifyMap(
        K_scaled, D, R1, P1, image_size_rect, cv2.CV_32FC1
    )
    map_right_x, map_right_y = cv2.initUndistortRectifyMap(
        K_scaled, D, R2, P2, image_size_rect, cv2.CV_32FC1
    )
    
    print("   -> Aplicando mapas (remapping)...")
    img_left_rectified = cv2.remap(
        img_left_scaled, map_left_x, map_left_y, cv2.INTER_LINEAR
    )
    img_right_rectified = cv2.remap(
        img_right_scaled, map_right_x, map_right_y, cv2.INTER_LINEAR
    )
    
    print("   -> Remapping completo.")
    
    # Store new parameters for reconstruction
    new_params = {
        'P1': P1,
        'P2': P2,
        'Q': Q,
        'roi1': roi1,
        'roi2': roi2
    }
    
    return img_left_rectified, img_right_rectified, new_params