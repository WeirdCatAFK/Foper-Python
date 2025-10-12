function r = mutacion(a, num)
% MUTACION Aplica mutación a una población codificada en binario.
%
% Sintaxis:
%   r = mutacion(a, num)
%
% Descripción:
%   Esta función toma una población de individuos codificados en binario
%   y aplica mutación aleatoria a 'num' genes de cada individuo. La mutación
%   consiste en invertir el valor de un bit (0 → 1, 1 → 0).
%
% Parámetros:
%   a   -> Vector o matriz con la población codificada en binario
%   num -> Número de genes a mutar
%
% Salida:
%   r -> Población mutada (misma dimensión que 'a')

    % n: número de genes por individuo (asume que a está codificado como [X Y])
    n = fix(max(size(a)) / 2);

    % Selecciona 'num' posiciones aleatorias para mutar
    ind = fix(n * rand(num, 1)) + 1;

    % Inicializa la población resultante igual a la original
    r = a;

    % Invierte los bits seleccionados (0 -> 1, 1 -> 0)
    r(ind) = ~a(ind);
end
