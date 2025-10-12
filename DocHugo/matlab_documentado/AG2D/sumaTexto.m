function r = sumaTexto(msj)
% SUMATEXTO Convierte un texto en un número sumando los códigos ASCII de sus caracteres.
%
% Sintaxis:
%   r = sumaTexto(msj)
%
% Descripción:
%   Esta función toma un string o carácter de texto y devuelve la suma
%   de los valores ASCII de cada carácter en el mensaje.
%   Puede ser útil para generar un número pseudoaleatorio a partir de un texto.
%
% Parámetros:
%   msj -> Cadena de texto (string o char array)
%
% Salida:
%   r -> Suma de los valores ASCII de cada carácter del texto

    % Convierte los caracteres a sus valores ASCII y los suma
    r = sum(double(msj));
end
