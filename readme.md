# Proyecto de reconstrucción 3D

## Estructura del proyecto

Las carpetas que empiezan con \_ son código heredado como prueba de concepto, y es referencial y no tan relevante

Las siguientes carpetas contiene código que genera recursos

- entradas
  Aquí se almacenan N videos para generar la
- preparación
  Aquí se normalizan y preparan las imagenes extraidas del video (ej: se extra el promedio de la imagen para eliminar los objetos que se mueven de la escena)
- disparidad
  Aqui se generan las matrices de disparidad de pares de imagenes, cuyos resultados se guardan en la carpeta resultados
- reconstrucción
  Aqui se leen los datos generados en disparidad para generar visualizaciones 3d utilizando los datos
- resultados
  Aquí se guardan los archivos generados de la disparidad y recon

main.py es el archivo que orquestra todas las actividades en un solo pipeline, edita el archivo.env para cambiar los parámetros de procesamiento de los videos

## Uso del proyecto

Arrastra videos a la carpeta de entradas en formato .mp4

Este proyecto procesa n archivos y sus disparidades

Nombra tus archivos de video de tal manera que los videos de los que necesites calcular su disparidad de manera consecutiva

Por ejemplo

Tienes tus archivos:

```
entradas
├── Toma0.mp4
└── Toma1.mp4
```

El código generara la disparidad de Toma0-Toma1, generara sus matrices en la carpeta de resultados en /disparidades
