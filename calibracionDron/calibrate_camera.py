import numpy as np
import cv2
import glob
import os
import pickle

class CameraCalibrator:
    """
    Clase para calibrar una cámara usando imágenes de tablero de ajedrez.
    """
    
    def __init__(self, chessboard_size=(12, 19), square_size=25.0):
        """
        Inicializa el calibrador.
        
        Args:
            chessboard_size: Tupla (cols, rows) de esquinas INTERNAS del tablero
                            Por ejemplo, un tablero de 10x7 casillas tiene 9x6 esquinas internas
            square_size: Tamaño de cada casilla en mm (o la unidad que prefieras)
        """
        self.chessboard_size = chessboard_size
        self.square_size = square_size
        
        # Criterio de terminación para refinamiento sub-pixel
        self.criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
        
        # Preparar puntos del objeto (coordenadas 3D del tablero en el mundo real)
        self.objp = np.zeros((chessboard_size[0] * chessboard_size[1], 3), np.float32)
        self.objp[:, :2] = np.mgrid[0:chessboard_size[0], 0:chessboard_size[1]].T.reshape(-1, 2)
        self.objp *= square_size  # Escalar por el tamaño real de las casillas
        
        # Arrays para almacenar puntos de todas las imágenes
        self.objpoints = []  # Puntos 3D en el mundo real
        self.imgpoints = []  # Puntos 2D en el plano de la imagen
        
        self.images_used = []
        self.img_shape = None
        
    def add_image(self, image_path, visualize=False):
        """
        Procesa una imagen del tablero de ajedrez.
        
        Args:
            image_path: Ruta a la imagen
            visualize: Si True, muestra la imagen con las esquinas detectadas
            
        Returns:
            True si se detectaron las esquinas, False en caso contrario
        """
        img = cv2.imread(image_path)
        if img is None:
            print(f"❌ Error al cargar: {image_path}")
            return False
        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        self.img_shape = gray.shape[::-1]  # (width, height)
        
        # Buscar esquinas del tablero
        ret, corners = cv2.findChessboardCorners(
            gray, 
            self.chessboard_size, 
            cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_NORMALIZE_IMAGE
        )
        
        if ret:
            # Refinar posición de esquinas con precisión sub-pixel
            corners_refined = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), self.criteria)
            
            self.objpoints.append(self.objp)
            self.imgpoints.append(corners_refined)
            self.images_used.append(os.path.basename(image_path))
            
            print(f"✓ Esquinas detectadas en: {os.path.basename(image_path)}")
            
            # Visualización opcional
            if visualize:
                img_with_corners = cv2.drawChessboardCorners(
                    img.copy(), 
                    self.chessboard_size, 
                    corners_refined, 
                    ret
                )
                cv2.imshow('Esquinas Detectadas', img_with_corners)
                cv2.waitKey(500)
            
            return True
        else:
            print(f"⚠ No se detectaron esquinas en: {os.path.basename(image_path)}")
            return False
    
    def calibrate(self):
        """
        Ejecuta la calibración de la cámara.
        
        Returns:
            Diccionario con los resultados de la calibración
        """
        if len(self.objpoints) < 3:
            raise ValueError("Se necesitan al menos 3 imágenes con esquinas detectadas. "
                           f"Solo se encontraron {len(self.objpoints)}.")
        
        print(f"\n🔧 Calibrando con {len(self.objpoints)} imágenes...")
        
        # CALIBRACIÓN - Aquí es donde ocurre la magia
        ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(
            self.objpoints,
            self.imgpoints,
            self.img_shape,
            None,
            None
        )
        
        print(f"✅ Calibración completada!")
        print(f"📊 Error RMS de reproyección: {ret:.4f} píxeles")
        
        # Calcular matriz óptima para undistort
        h, w = self.img_shape[1], self.img_shape[0]
        new_mtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))
        
        # Calcular error de reproyección para cada imagen
        mean_error = 0
        errors = []
        for i in range(len(self.objpoints)):
            imgpoints2, _ = cv2.projectPoints(self.objpoints[i], rvecs[i], tvecs[i], mtx, dist)
            error = cv2.norm(self.imgpoints[i], imgpoints2, cv2.NORM_L2) / len(imgpoints2)
            errors.append(error)
            mean_error += error
        
        mean_error /= len(self.objpoints)
        print(f"📉 Error medio por imagen: {mean_error:.4f} píxeles")
        
        results = {
            'camera_matrix': mtx,           # Matriz K de parámetros intrínsecos
            'dist_coeffs': dist,             # Coeficientes de distorsión
            'rvecs': rvecs,                  # Vectores de rotación (extrínsecos)
            'tvecs': tvecs,                  # Vectores de traslación (extrínsecos)
            'new_camera_matrix': new_mtx,   # Matriz K optimizada
            'roi': roi,                      # Región de interés para recortar
            'rms_error': ret,                # Error RMS global
            'mean_error': mean_error,        # Error medio por imagen
            'image_errors': errors,          # Errores individuales
            'images_used': self.images_used,
            'image_size': self.img_shape,
            'chessboard_size': self.chessboard_size,
            'square_size': self.square_size
        }
        
        return results
    
    def save_calibration(self, results, filename='camera_calibration.pkl'):
        """Guarda los resultados de calibración en un archivo."""
        with open(filename, 'wb') as f:
            pickle.dump(results, f)
        print(f"💾 Calibración guardada en: {filename}")
    
    def print_results(self, results):
        """Imprime los resultados de forma legible."""
        print("\n" + "="*60)
        print("📷 RESULTADOS DE CALIBRACIÓN")
        print("="*60)
        
        print("\n🔍 Matriz de Cámara (K) - Parámetros Intrínsecos:")
        print(results['camera_matrix'])
        print(f"\n  • Distancia focal (fx): {results['camera_matrix'][0, 0]:.2f} px")
        print(f"  • Distancia focal (fy): {results['camera_matrix'][1, 1]:.2f} px")
        print(f"  • Centro óptico (cx): {results['camera_matrix'][0, 2]:.2f} px")
        print(f"  • Centro óptico (cy): {results['camera_matrix'][1, 2]:.2f} px")
        
        print("\n🌀 Coeficientes de Distorsión:")
        print(results['dist_coeffs'].ravel())
        print(f"  • k1 (radial): {results['dist_coeffs'][0, 0]:.6f}")
        print(f"  • k2 (radial): {results['dist_coeffs'][0, 1]:.6f}")
        print(f"  • p1 (tangencial): {results['dist_coeffs'][0, 2]:.6f}")
        print(f"  • p2 (tangencial): {results['dist_coeffs'][0, 3]:.6f}")
        print(f"  • k3 (radial): {results['dist_coeffs'][0, 4]:.6f}")
        
        print(f"\n📊 Estadísticas:")
        print(f"  • Imágenes usadas: {len(results['images_used'])}")
        print(f"  • Error RMS: {results['rms_error']:.4f} px")
        print(f"  • Error medio: {results['mean_error']:.4f} px")
        print(f"  • Tamaño imagen: {results['image_size']}")
        
        print("\n" + "="*60)

def undistort_image(image_path, calibration_file='camera_calibration.pkl', output_path=None):
    """
    Corrige la distorsión de una imagen usando una calibración guardada.
    
    Args:
        image_path: Ruta a la imagen a corregir
        calibration_file: Archivo con los parámetros de calibración
        output_path: Ruta donde guardar la imagen corregida (opcional)
    """
    # Cargar calibración
    with open(calibration_file, 'rb') as f:
        results = pickle.load(f)
    
    mtx = results['camera_matrix']
    dist = results['dist_coeffs']
    new_mtx = results['new_camera_matrix']
    roi = results['roi']
    
    # Leer imagen
    img = cv2.imread(image_path)
    h, w = img.shape[:2]
    
    # Corregir distorsión
    dst = cv2.undistort(img, mtx, dist, None, new_mtx)
    
    # Recortar la imagen según ROI
    x, y, w, h = roi
    dst_cropped = dst[y:y+h, x:x+w]
    
    if output_path:
        cv2.imwrite(output_path, dst_cropped)
        print(f"✓ Imagen corregida guardada en: {output_path}")
    
    return dst, dst_cropped


# =============================================================================
# EJEMPLO DE USO
# =============================================================================

if __name__ == "__main__":
    # PASO 1: Configurar el calibrador
    # Cambia estos valores según tu tablero:
    # - (9, 6) significa 9 esquinas horizontales y 6 verticales INTERNAS
    # - 25.0 es el tamaño de cada casilla en mm
    calibrator = CameraCalibrator()
    
    # PASO 2: Cargar todas las imágenes de calibración
    # Asegúrate de tener tus imágenes en una carpeta llamada 'calibration_images'
    image_pattern = 'imgs/*.jpg'  # Cambia según tu formato (jpg, png, etc.)
    image_paths = glob.glob(image_pattern)
    
    if not image_paths:
        print(f"❌ No se encontraron imágenes en: {image_pattern}")
        print("Por favor, coloca tus imágenes de calibración en la carpeta 'calibration_images'")
        exit(1)
    
    print(f"📁 Se encontraron {len(image_paths)} imágenes")
    print("\n🔍 Procesando imágenes...\n")
    
    # Procesar cada imagen
    for img_path in image_paths:
        calibrator.add_image(img_path, visualize=False)  # Cambia a True para ver las detecciones
    
    cv2.destroyAllWindows()
    
    # PASO 3: Ejecutar calibración
    if len(calibrator.objpoints) >= 3:
        results = calibrator.calibrate()
        
        # PASO 4: Mostrar y guardar resultados
        calibrator.print_results(results)
        calibrator.save_calibration(results, 'camera_calibration.pkl')
        
        # PASO 5 (OPCIONAL): Probar la corrección en una imagen
        if image_paths:
            test_image = image_paths[0]
            print(f"\n🧪 Probando corrección de distorsión en: {os.path.basename(test_image)}")
            corrected, cropped = undistort_image(
                test_image, 
                'camera_calibration.pkl',
                'test_undistorted.jpg'
            )
            
            # Mostrar comparación
            original = cv2.imread(test_image)
            comparison = np.hstack((original, corrected))
            cv2.imshow('Izquierda: Original | Derecha: Corregida', comparison)
            print("\n💡 Presiona cualquier tecla para cerrar la ventana de comparación")
            cv2.waitKey(0)
            cv2.destroyAllWindows()
    else:
        print("\n❌ No se detectaron suficientes tableros para calibrar.")
        print("Asegúrate de que:")
        print("  1. Tus imágenes muestran claramente el tablero de ajedrez")
        print("  2. El tamaño del tablero (chessboard_size) es correcto")
        print("  3. Las imágenes tienen buena iluminación y están enfocadas")