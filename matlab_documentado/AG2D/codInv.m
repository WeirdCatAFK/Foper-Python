function r = codInv(a, b, epsilon, n, p)
% CODINV Decodifica una representación binaria en un valor real dentro de un intervalo.
%
% Sintaxis:
%   r = codInv(a, b, epsilon, n, p)
%
% Descripción:
%   Esta función realiza la operación inversa de 'cod'. 
%   Toma una secuencia binaria que representa un número (codificada por 'cod')
%   y la convierte nuevamente a su valor real dentro del intervalo [a, b],
%   usando la misma precisión 'epsilon'.
%
% Parámetros:
%   a, b     -> Límites inferior y superior del intervalo donde se busca la solución.
%   epsilon  -> Precisión (tamaño del paso) usada para codificar.
%   n        -> Vector fila con los bits (0 o 1) que representan el número codificado.
%   p        -> Vector de potencias de 2 (usualmente p = 2.^(tam-1:-1:0)).
%
% Salida:
%   r -> Valor real decodificado a partir del código binario.

    % Calcula el tamaño del vector binario (cantidad de bits)
    tam = size(n, 2);

    % Calcula el número decimal correspondiente a la secuencia binaria 'n'
    % Usando el producto punto entre el vector de bits y el vector de potencias de 2
    r = n * p';
    
    % (Alternativa comentada)
    % Este bloque realiza lo mismo pero usando un bucle:
    % for i = tam:-1:1
    %     r = r + n(i) * 2^(tam - i);
    % end

    % Escala el valor entero 'r' al intervalo real [a, b]
    % Sumando el desplazamiento inicial 'a' y aplicando el tamaño de paso 'epsilon'
    r = a + epsilon * r;
end
