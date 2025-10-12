function pts = cruzamiento(puntos)
% CRUZAMIENTO Aplica el operador de cruce a una población de individuos.
%
% Sintaxis:
%   pts = cruzamiento(puntos)
%
% Descripción:
%   Esta función aplica la operación de cruce (usando la función 'cruza')
%   a una población de individuos binarios. Cada individuo se cruza con su
%   siguiente en la lista, y el último se cruza con el primero, generando
%   así una nueva generación de hijos. Finalmente, devuelve una población
%   extendida que incluye tanto los padres originales como los hijos generados.
%
% Parámetros:
%   puntos -> Matriz donde cada fila representa un individuo codificado en binario.
%
% Salida:
%   pts -> Matriz con los individuos originales (padres) y los nuevos hijos concatenados.

    % Inicializa la matriz que contendrá los hijos con el mismo tamaño que la población original
    ptshijos = zeros(size(puntos));

    % Cruza cada individuo con el siguiente en la población
    for i = 1:(size(puntos, 1)) - 1
        % Obtiene dos hijos (a, b) cruzando el individuo i con el siguiente
        [a, b] = cruza(puntos(i, :), puntos(i + 1, :));
        % Solo guarda el primer hijo (a) en la nueva población
        ptshijos(i, :) = a;
    end

    % Cruza el último individuo con el primero (cierre del ciclo)
    [a, b] = cruza(puntos(end, :), puntos(1, :));
    ptshijos(end, :) = a;

    % Combina la población original y la población de hijos
    pts = [puntos; ptshijos];
end
