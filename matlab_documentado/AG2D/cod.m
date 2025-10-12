function r = cod(a, b, epsilon, nc, n)
% COD Codifica un número real dentro de un intervalo en una representación binaria.
%
% Sintaxis:
%   r = cod(a, b, epsilon, nc, n)
%
% Descripción:
%   Esta función toma un número real `nc` dentro del intervalo [a, b] y lo
%   codifica como una secuencia binaria de longitud `n`, con una precisión
%   determinada por `epsilon`.
%
% Parámetros:
%   a, b     -> Límites inferior y superior del intervalo donde se busca la solución.
%   epsilon  -> Precisión o tamaño del paso en el intervalo (resolución).
%   nc       -> Número que se desea codificar.
%   n        -> Cantidad de dígitos binarios necesarios para representar el número.
%
% Salida:
%   r -> Vector fila de longitud n que contiene la representación binaria de `nc`.

    % Inicializa el vector de salida con ceros
    r = zeros(1, n);
    
    % Calcula el número de pasos desde 'a' hasta 'nc' dividido por la precisión
    % Redondea para obtener un índice entero correspondiente a 'nc'
    num = round((nc - a) / epsilon);
    
    % Convierte el número 'num' a binario, almacenando cada bit en el vector 'r'
    for i = n:-1:1  % Recorre de derecha a izquierda (bit menos significativo primero)
        r(i) = mod(num, 2);   % Obtiene el bit menos significativo
        num = fix(num / 2);   % Desplaza los bits a la derecha (división entera por 2)
    end
end
