import cv2
import numpy as np
def estimate_pose(img1_gray, img2_gray, K_scaled, D_coeffs):
    """
    Estimates the relative rotation (R) and translation (t) between two images
    using feature matching.

    Args:
        img1_gray: First image (scaled, grayscale).
        img2_gray: Second image (scaled, grayscale).
        K_scaled: The scaled intrinsic camera matrix.
        D_coeffs: The distortion coefficients.

    Returns:
        (R, t) tuple if successful, (None, None) otherwise.
    """
    
    # --- 1. Detect and Match Features ---
    # Use ORB (an efficient and free alternative to SIFT)
    orb = cv2.ORB_create(nfeatures=2000, fastThreshold=20)
    kp1, des1 = orb.detectAndCompute(img1_gray, None)
    kp2, des2 = orb.detectAndCompute(img2_gray, None)

    if des1 is None or des2 is None or len(des1) < 50 or len(des2) < 50:
        print("    -> ⚠ Advertencia: No se detectaron suficientes features. Saltando.")
        return None, None

    # Use BFMatcher (Brute-Force) with Hamming distance for ORB
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(des1, des2)
    
    # Sort them in the order of their distance
    matches = sorted(matches, key=lambda x: x.distance)
    
    # Keep top 100 matches (or fewer if not many found)
    good_matches = matches[:min(100, len(matches))]

    if len(good_matches) < 20: # Need at least 8 points for E matrix, but more is better
        print("    -> ⚠ Advertencia: No hay suficientes 'good matches'. Saltando.")
        return None, None

    # Extract location of good matches
    pts1 = np.float32([kp1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
    pts2 = np.float32([kp2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)

    # --- 2. Undistort Keypoints ---
    # We must use undistorted points to find the Essential Matrix
    if D_coeffs is not None and np.any(D_coeffs != 0):
        pts1 = cv2.undistortPoints(pts1, K_scaled, D_coeffs, None, K_scaled)
        pts2 = cv2.undistortPoints(pts2, K_scaled, D_coeffs, None, K_scaled)
        
    # --- 3. Find Essential Matrix ---
    # The K_scaled is crucial here.
    E, mask = cv2.findEssentialMat(
        pts1, 
        pts2, 
        K_scaled, 
        method=cv2.RANSAC, 
        prob=0.999, 
        threshold=1.0
    )

    if E is None:
        print("    -> ⚠ Advertencia: No se pudo encontrar la Matriz Esencial. Saltando.")
        return None, None

    # --- 4. Recover Pose (R and t) ---
    # This function finds the R and t that are physically plausible
    _, R, t, mask = cv2.recoverPose(E, pts1, pts2, K_scaled, mask=mask)

    if R is None or t is None:
        print("    -> ⚠ Advertencia: No se pudo recuperar la pose (R, t). Saltando.")
        return None, None

    # --- **NUEVA VALIDACIÓN** ---
    # Contar los inliers (puntos que se ajustan al modelo R, t)
    inlier_count = np.sum(mask)
    
    # Definir un umbral mínimo. 20 inliers es un número razonable.
    # Si tenemos menos que esto, la pose estimada es basura.
    MIN_INLIERS = 20 
    
    if inlier_count < MIN_INLIERS:
        print(f"    -> ⚠ Advertencia: Pose rechazada. Muy pocos inliers: {inlier_count} (se necesitan > {MIN_INLIERS})")
        return None, None
        
    # --- **FIX APLICADO** ---
    # (El fix de invertir 't' se mantiene, pero solo se ejecuta
    # si la pose es válida)
    if t[0] < 0:
        print("    -> ℹ Info: El vector 't' de la pose apunta a X-negativo. Invirtiendo t.")
        t = abs(t)
    
    print(f"    -> ✓ Pose estimada: {len(good_matches)} matches -> {inlier_count} inliers.")
    return R, t