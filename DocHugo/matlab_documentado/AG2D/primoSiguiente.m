function p = primoSiguiente(n)
% PRIMOSIGUIENTE Encuentra el siguiente número primo mayor o igual a n.
%
% Sintaxis:
%   p = primoSiguiente(n)
%
% Descripción:
%   Esta función recibe un número entero n y devuelve el primer número primo
%   que sea mayor o igual a n. Utiliza la función auxiliar esPrimo para
%   verificar si un número es primo.
%
% Parámetros:
%   n -> Número entero inicial
%
% Salida:
%   p -> Primer número primo mayor o igual a n

    % Mientras n no sea primo, incrementar n
    while (esPrimo(n) == 0)
        n = n + 1;
    end

    % Asignar el primo encontrado a la salida
    p = n;
end
