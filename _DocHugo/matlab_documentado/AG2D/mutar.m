function puntos = mutar(puntos, n)
% MUTAR Aplica mutación a una población completa de individuos binarios.
%
% Sintaxis:
%   puntos = mutar(puntos, n)
%
% Descripción:
%   Esta función selecciona aleatoriamente un subconjunto de individuos de la
%   población y les aplica la mutación binaria (función `mutacion`). La
%   mutación introduce diversidad genética para evitar estancamiento.
%
% Parámetros:
%   puntos -> Matriz de individuos codificados en binario (cada fila es un individuo)
%   n      -> Probabilidad o porcentaje de mutación (0 < n <= 1)
%
% Salida:
%   puntos -> Población mutada

    % Número total de individuos
    total = size(puntos, 1);

    % Selecciona aleatoriamente floor(n * total) individuos para mutar
    ind = fix(rand(fix(n * total), 1)) + 1;

    % Aplica la función 'mutacion' a cada individuo seleccionado
    for i = 1:n
        puntos(ind(i), :) = mutacion(puntos(ind(i), :), 4); % muta 4 genes por individuo
    end
end
