function r = seleccion(a, b, epsilon, puntos, y)
% SELECCION Selecciona los mejores individuos de una población para reproducción.
%
% Sintaxis:
%   r = seleccion(a, b, epsilon, puntos, y)
%
% Descripción:
%   Esta función implementa el operador de selección de un algoritmo genético.
%   Ordena la población según su evaluación (aptitud) y selecciona la mitad
%   superior para que continúe en la siguiente generación.
%
% Parámetros:
%   a, b     -> Límites del espacio de búsqueda (no se usan directamente aquí)
%   epsilon  -> Precisión de codificación (no se usa directamente aquí)
%   puntos   -> Matriz de individuos codificados en binario
%   y        -> Vector de valores de evaluación (aptitud) para cada individuo
%
% Salida:
%   r -> Índices de los individuos seleccionados (mitad superior de la población)

    % Ordena los individuos según su aptitud de mayor a menor
    [~, pys] = sort(y, 'descend');

    % Selecciona la mitad superior de la población
    r = pys(1 : size(puntos, 1)/2);
end
