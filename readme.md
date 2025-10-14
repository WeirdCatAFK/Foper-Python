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
