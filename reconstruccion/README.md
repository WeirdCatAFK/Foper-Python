# Algoritmos de Reconstrucción 3D

Este módulo contiene dos scripts de Python para la reconstrucción 3D a partir de imágenes estéreo.

## ¿Por qué dos scripts?

Existen dos implementaciones que corresponden a dos escenarios comunes en visión estéreo: el caso ideal (imágenes rectificadas) y el caso general (imágenes no rectificadas).

---

### 1. `reconstruction.py` (Caso Ideal / Rectificado)

-   **Cuándo usarlo:** Utiliza este script cuando tus imágenes estéreo ya han sido **rectificadas**. Esto significa que las cámaras se consideran perfectamente paralelas y alineadas, y las correspondencias de píxeles se encuentran en la misma línea horizontal. La entrada es un **mapa de disparidad**.

-   **Configuración Requerida (`CameraConfig`):**
    -   `fx`, `fy`: Distancia focal en píxeles.
    -   `cx`, `cy`: Punto principal (centro óptico).
    -   `baseline`: La distancia exacta entre los centros de las dos cámaras.

---

### 2. `casoB.py` (Caso General / No Rectificado)

-   **Cuándo usarlo:** Utiliza este script para el caso general, donde las cámaras pueden tener **cualquier rotación y traslación** relativa entre ellas. Este método es más flexible. La entrada es un conjunto de **puntos 2D correspondientes** entre las dos imágenes.

-   **Configuración Requerida (`StereoPairConfig`):**
    -   `K1`: Matriz intrínseca de la cámara 1.
    -   `K2`: Matriz intrínseca de la cámara 2.
    -   `R`: Matriz de rotación (3x3) de la cámara 1 a la 2.
    -   `T`: Vector de traslación (3x1) de la cámara 1 a la 2.
