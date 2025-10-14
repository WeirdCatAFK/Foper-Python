import cv2
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

try:
    from .genetico import genetico
except:
    from genetico import genetico


def calcular_mapa_disparidad(img_izquierda, img_derecha, radio_ventana, radio_busqueda):
    print("Iniciando cálculo del mapa de disparidad (con Numba)...")

    imi = img_izquierda.astype(np.float32) / 255.0
    imd = img_derecha.astype(np.float32) / 255.0

    h, w = imi.shape
    M = np.zeros((h, w, 2))
    NM = np.full((h, w), np.nan)
    E = np.full((h, w), np.nan)

    y_range = range(radio_ventana, h - radio_ventana)
    x_range = range(radio_ventana, w - radio_ventana)

    pbar = tqdm(total=(len(y_range) * len(x_range)), desc="Procesando ventanas")

    for y in y_range:
        for x in x_range:
            ry = np.arange(y - radio_ventana, y + radio_ventana + 1)
            rx = np.arange(x - radio_ventana, x + radio_ventana + 1)
            grid_x, grid_y = np.meshgrid(rx, ry)

            X_coords = grid_x.flatten().astype(np.float32)
            Y_coords = grid_y.flatten().astype(np.float32)
            It_plantilla = imi[Y_coords.astype(int), X_coords.astype(int)]

            sol = genetico(
                a=[-radio_busqueda, -radio_busqueda],
                b=[+radio_busqueda, +radio_busqueda],
                epsilon=1,
                n_generaciones=10,
                n_individuos=100,
                prob_mutacion=0.01,
                r_paciencia=5,
                # Se pasan los arrays directamente
                imi=imi,
                imd=imd,
                X_coords=X_coords,
                Y_coords=Y_coords,
                It_plantilla=It_plantilla,
            )

            M[y, x, :] = sol[:2]
            NM[y, x] = np.sqrt(sol[0] ** 2 + sol[1] ** 2)
            E[y, x] = sol[2]

            pbar.update(1)

    pbar.close()
    print("Cálculo finalizado.")
    return NM, E


# ---- Bloque de Pruebas ----
if __name__ == "__main__":
    try:
        img_i = cv2.imread("./resultados/imagenes/toma0.jpg", cv2.IMREAD_GRAYSCALE)
        img_d = cv2.imread("./resultados/imagenes/toma1.jpg", cv2.IMREAD_GRAYSCALE)
        if img_i is None or img_d is None:
            raise FileNotFoundError()
    except FileNotFoundError:
        print("Error: No se encontraron las imágenes.")
    else:
        mapa_disparidad, mapa_error = calcular_mapa_disparidad(img_i, img_d, 15, 55)
        # Visualización
        plt.figure(figsize=(12, 4))
        plt.subplot(1, 2, 1)
        plt.title("Mapa de Disparidad (Numba)")
        plt.imshow(mapa_disparidad, cmap="jet")
        plt.colorbar()
        plt.subplot(1, 2, 2)
        plt.title("Mapa de Error (Numba)")
        plt.imshow(mapa_error, cmap="jet")
        plt.colorbar()
        plt.show()
