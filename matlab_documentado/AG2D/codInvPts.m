function pts = codInvPts(puntos, a, b, epsilon, m)
% CODINVPTS Decodifica una población de puntos binarios a coordenadas reales (x, y).
%
% Sintaxis:
%   pts = codInvPts(puntos, a, b, epsilon, m)
%
% Descripción:
%   Esta función aplica la decodificación binaria → real (usando 'codInv')
%   a un conjunto de puntos (por ejemplo, una población de un algoritmo genético),
%   donde cada punto está representado como una secuencia binaria que contiene
%   las codificaciones de las variables X e Y.
%
% Parámetros:
%   puntos  -> Matriz donde cada fila representa un individuo (una secuencia binaria completa).
%   a, b    -> Vectores con los límites inferiores y superiores del intervalo para cada variable.
%              Por ejemplo: a = [ax ay], b = [bx by].
%   epsilon -> Precisión o tamaño del paso (resolución).
%   m       -> Vector con la cantidad de bits asignados a cada variable.
%              Ejemplo: m = [mX mY].
%
% Variables globales:
%   pot1, pot2 -> Vectores con las potencias de 2 correspondientes a cada variable,
%                 usados para convertir de binario a decimal en 'codInv'.
%
% Salida:
%   pts -> Matriz con las coordenadas decodificadas [x y] para cada individuo.

    % Declaración de variables globales que contienen las potencias de 2
    global pot1
    global pot2

    % Inicializa la matriz de salida con ceros
    % Cada fila corresponde a un punto (x, y)
    pts = zeros(size(puntos, 1), 2);

    % Extrae los bits correspondientes a la variable X y a la variable Y
    % X = primeras m(1) columnas, Y = las siguientes m(2) columnas
    X = puntos(:, 1:m(1));                  % Bits que representan la coordenada X
    Y = puntos(:, m(1)+1 : m(1)+m(2));      % Bits que representan la coordenada Y

    % Recorre cada punto (fila)
    for i = 1:size(puntos, 1)
        % Decodifica la parte binaria correspondiente a X
        pts(i, 1) = codInv(a(1), b(1), epsilon, X(i, :), pot1);

        % Decodifica la parte binaria correspondiente a Y
        pts(i, 2) = codInv(a(2), b(2), epsilon, Y(i, :), pot2);
    end
end
