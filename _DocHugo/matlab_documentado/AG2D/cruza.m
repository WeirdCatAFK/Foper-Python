function [v1, v2] = cruza(a, b)
% CRUZA Realiza una operación de cruce (crossover) entre dos individuos binarios.
%
% Sintaxis:
%   [v1, v2] = cruza(a, b)
%
% Descripción:
%   Esta función implementa un operador de cruce simple utilizado en
%   algoritmos genéticos. A partir de dos vectores binarios (padres) 'a' y 'b',
%   genera dos nuevos vectores (hijos) 'v1' y 'v2' intercambiando bits de
%   forma alternada entre los padres.
%
% Parámetros:
%   a, b -> Vectores fila o columna del mismo tamaño que representan los
%           padres (individuos) a cruzar.
%
% Salida:
%   v1, v2 -> Nuevos vectores (hijos) generados por el cruce alternado.

    % Determina la cantidad de elementos del vector (longitud del cromosoma)
    n = fix(max(size(a)));

    % Inicializa los vectores hijos con ceros del mismo tamaño que los padres
    v1 = zeros(size(a));
    v2 = zeros(size(a));

    % Recorre cada posición del cromosoma
    for i = 1:n
        % Si la posición es par, se copian directamente los genes
        if mod(i, 2) == 0
            v1(i) = a(i);
            v2(i) = b(i);
        % Si la posición es impar, se intercambian los genes entre los padres
        else
            v1(i) = b(i);
            v2(i) = a(i);
        end
    end
end
