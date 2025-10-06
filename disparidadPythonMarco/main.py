

import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import time

# Importa la función principal del orquestador
from disparidad_genetico import calcular_disparidad_genetico

def main():
    """
    Función principal para ejecutar el ejemplo del cálculo de disparidad.
    """
    print("Iniciando el proceso de cálculo de disparidad estéreo...")
    
    # --- 1. Carga de Imágenes ---
    # Asegúrate de que las rutas a las imágenes sean correctas.
    try:
        # Usamos las imágenes de ejemplo de tu proyecto
        img_path1 = './izquierda.png'
        img_path2 = './derecha.png'
        
        i1_color = Image.open(img_path1)
        i2_color = Image.open(img_path2)
    except FileNotFoundError:
        print(f"Error: No se encontraron las imágenes en las rutas especificadas.")
        print("Por favor, verifica que los archivos existen en:")
        print(f"- {img_path1}")
        print(f"- {img_path2}")
        return

    # --- 2. Preparación de Imágenes ---
    # Convertir a escala de grises y a matriz numpy de tipo uint8 (0-255)
    i1 = np.array(i1_color.convert('L'))
    i2 = np.array(i2_color.convert('L'))
    
    print(f"Imágenes cargadas con dimensiones: {i1.shape}")

    # --- 3. Definición de Parámetros ---
    # Estos valores pueden ser ajustados para experimentar
    TAM_VENTANA = 5  # Radio de la ventana. Una ventana de 5x5 es 2. Una de 11x11 es 5.
    MAX_DISP = 40    # Disparidad máxima a buscar.
    
    # --- 4. Ejecución del Algoritmo ---
    start_time = time.time()
    
    d_map = calcular_disparidad_genetico(
        i1, 
        i2, 
        tam_ventana=TAM_VENTANA, 
        max_disp=MAX_DISP
    )
    
    end_time = time.time()
    print(f"\nCálculo completado en {end_time - start_time:.2f} segundos.")

    # --- 5. Visualización de Resultados ---
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    
    axes[0].imshow(i1_color)
    axes[0].set_title('Imagen Izquierda (Original)')
    axes[0].axis('off')
    
    # Usamos 'jet' para una mejor visualización de la profundidad
    im = axes[1].imshow(d_map, cmap='jet', vmin=0, vmax=MAX_DISP)
    axes[1].set_title('Mapa de Disparidad (Genético)')
    axes[1].axis('off')
    
    # Añadir barra de color
    fig.colorbar(im, ax=axes[1], orientation='vertical', fraction=0.046, pad=0.04)
    
    plt.tight_layout()
    plt.show()
    np.save("mapa_disparejo.npy", d_map)

if __name__ == '__main__':
    main()

