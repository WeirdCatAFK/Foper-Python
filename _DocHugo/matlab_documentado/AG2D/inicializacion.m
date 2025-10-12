function [pts, ptsr] = inicializacion(a, b, epsilon, m, n)
% INICIALIZACION Genera una población inicial para un algoritmo genético.
%
% Sintaxis:
%   [pts, ptsr] = inicializacion(a, b, epsilon, m, n)
%
% Descripción:
%   Esta función crea una población inicial de 'n' individuos para un
%   algoritmo genético que optimiza un problema 2D. 
%   Cada individuo se representa tanto en **binario (pts)** como en **coordenadas reales (ptsr)**.
%
% Parámetros:
%   a, b      -> Límites inferiores y superiores del dominio [a1, a2], [b1, b2]
%   epsilon   -> Precisión con la que se busca la solución
%   m         -> Vector [m1 m2] con el número de bits para codificar cada variable
%   n         -> Número de individuos a generar (tamaño de la población)
%
% Salida:
%   pts  -> Matriz binaria de tamaño n x (m1+m2), codificación genética de los individuos
%   ptsr -> Matriz n x 2 con las coordenadas reales de cada individuo

    % Inicializa la matriz binaria de la población
    pts = zeros(n, m(1) + m(2));

    % -----------------------------------------------------------
    % Genera coordenadas aleatorias dentro del rango [a, b]
    % -----------------------------------------------------------
    ptsr(:,1) = rand(n,1) * (b(1) - a(1)) + a(1);  % Componente X
    ptsr(:,2) = rand(n,1) * (b(2) - a(2)) + a(2);  % Componente Y

    % Redondea las coordenadas para ajustarlas a enteros
    ptsr = fix(ptsr);

    % -----------------------------------------------------------
    % Codifica cada individuo en binario
    % -----------------------------------------------------------
    for i = 1:n
        % Codifica X y Y usando la función 'cod' que transforma un valor real en un vector binario
        DNA = [cod(a(1), b(1), epsilon, ptsr(i,1), m(1)), ...
               cod(a(2), b(2), epsilon, ptsr(i,2), m(2))];

        % Guarda el individuo codificado en la matriz de población
        pts(i,:) = DNA;
    end
end
