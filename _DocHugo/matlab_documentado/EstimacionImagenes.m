% ------------------------------------------------------------
% Script principal para procesar múltiples archivos de video
% ------------------------------------------------------------
% Este script:
%   1. Busca todos los archivos .mp4 en el directorio actual.
%   2. Calcula un modelo de fondo para cada video usando la función
%      `estimacionFondo`, promediando un número determinado de cuadros.
%   3. Guarda el resultado intermedio en un archivo .oct.
%   4. Carga cada modelo de fondo y lo guarda como una imagen .jpg.
% ------------------------------------------------------------

clear all       % Limpia todas las variables del espacio de trabajo
clc % Limpia la consola

% Carga los paquetes necesarios para Octave
pkg load video % Permite leer y procesar videos
pkg load image % Permite manipular imágenes

close all % Cierra todas las ventanas de figuras abiertas

% ------------------------------------------------------------
% ETAPA 1: PROCESAMIENTO DE VIDEOS PARA GENERAR MODELOS DE FONDO
% ------------------------------------------------------------

% Obtiene la lista de todos los archivos con extensión .mp4 en el directorio actual
lista = dir("*.mp4");

% Recorre todos los archivos encontrados
for i = 1:size(lista, 1)

    disp('Procesando archivo de video...');
    disp(lista(i).name); % Muestra el nombre del archivo actual

    % Llama a la función estimacionFondo para calcular el modelo de fondo
    % Parámetros:
    %   - lista(i).name : nombre del archivo de video
    %   - 200           : cantidad de cuadros a analizar
    imF = estimacionFondo(lista(i).name, 200);

    % Guarda el modelo de fondo en un archivo .oct
    % El nombre del archivo será, por ejemplo: "video1.mp4.oct"
    save(sprintf("%s.oct", lista(i).name), "imF");
end

% ------------------------------------------------------------
% ETAPA 2: CONVERSIÓN DE LOS MODELOS DE FONDO A IMÁGENES JPG
% ------------------------------------------------------------

for i = 1:size(lista, 1)

    disp('Convirtiendo modelo de fondo a imagen...');
    disp(lista(i).name); % Muestra el nombre del archivo actual

    % Carga el modelo de fondo previamente calculado (.oct)
    load(sprintf("%s.oct", lista(i).name));

    % Muestra en consola el tamaño de la matriz del fondo (alto x ancho)
    disp(size(imF));

    % Convierte la matriz a tipo uint8 (rango [0,255]) y guarda como imagen JPG
    % con la máxima calidad (100%)
    imwrite(uint8(imF), sprintf("%s.jpg", lista(i).name), "jpg", "Quality", 100);
end
