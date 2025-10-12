function h = rgb2gray(I)
% RGB2GRAY Convierte una imagen RGB a una imagen en escala de grises.
%
% Sintaxis:
%   h = rgb2gray(I)
%
% Descripción:
%   Esta función convierte una imagen a color (RGB) en una versión
%   en escala de grises utilizando el canal de intensidad de la
%   representación HSV (valor).
%
% Parámetros:
%   I -> Imagen RGB de entrada (matriz MxNx3)
%
% Salida:
%   h -> Imagen en escala de grises (matriz MxN)

    % Convierte la imagen RGB a HSV
    h = rgb2hsv(I);

    % Extrae el canal de valor (V) que representa la intensidad
    h = h(:,:,3);
end
