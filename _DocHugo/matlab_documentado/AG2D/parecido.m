function por = parecido(Ir, Ic)
% PARECIDO Calcula el porcentaje de similitud entre dos imágenes binarias.
%
% Sintaxis:
%   por = parecido(Ir, Ic)
%
% Descripción:
%   Esta función compara dos matrices binarias (o lógicas) del mismo tamaño
%   y devuelve el porcentaje de píxeles que son exactamente iguales.
%
% Parámetros:
%   Ir -> Imagen de referencia (matriz binaria)
%   Ic -> Imagen comparada (matriz binaria)
%
% Salida:
%   por -> Porcentaje de similitud (valor entre 0 y 1)

    % Total de píxeles en la imagen
    RR = size(Ir, 1) * size(Ir, 2);

    % Matriz lógica indicando coincidencias píxel a píxel
    R = Ir == Ic;

    % Calcula el porcentaje de píxeles iguales
    por = sum(R(:)) / RR;

    % Alternativa comentada: si se quisiera usar XOR para diferencias
    % R = xor(Ir, Ic);
    % por = 1 - sum(R(:)) / RR;
end
