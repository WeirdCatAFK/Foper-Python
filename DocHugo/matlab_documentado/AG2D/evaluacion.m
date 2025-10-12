function pts = evaluacion(a, b, epsilon, puntos, puntosR, d)
% EVALUACION Evalúa una población de puntos reales según una función objetivo.
%
% Sintaxis:
%   pts = evaluacion(a, b, epsilon, puntos, puntosR, d)
%
% Descripción:
%   Esta función calcula el valor de evaluación (fitness o costo)
%   para cada punto en la población, dependiendo de si el punto
%   pertenece al dominio válido [a, b].
%
%   Si el punto está dentro del intervalo permitido (ver 'pertenece'),
%   se evalúa con la función 'fnEvaluacion'. Si no, se le asigna un valor
%   de +inf (infinito positivo), indicando una solución no válida
%   en un problema de minimización.
%
% Parámetros:
%   a, b     -> Vectores con los límites inferior y superior del dominio.
%               Ejemplo: a = [ax ay], b = [bx by].
%   epsilon  -> Precisión del intervalo (no se usa directamente aquí, pero
%               se mantiene para compatibilidad con otras funciones).
%   puntos   -> Matriz binaria (representación codificada de la población).
%   puntosR  -> Matriz con los puntos ya decodificados a coordenadas reales [x y].
%   d        -> Parámetro adicional (por ejemplo, datos o coeficientes
%               requeridos por la función de evaluación).
%
% Salida:
%   pts -> Vector columna con el valor de evaluación (fitness) para cada punto.

    % Número de individuos en la población
    long = size(puntos, 1);

    % Inicializa el vector de evaluaciones
    pts = zeros(long, 1);

    % Recorre cada individuo
    for i = 1:long
        % (Alternativa desactivada) Podría decodificar aquí con codInv
        % valor = codInv(a, b, epsilon, puntos(i, :));

        % Verifica si el punto pertenece al dominio válido
        if pertenece(a, b, puntosR(i, :)) == 1
            % Evalúa el punto si está dentro de los límites
            pts(i) = fnEvaluacion(puntosR(i, :), d);
        else
            % Si está fuera del dominio, se penaliza con un valor infinito
            % (se usa +inf porque el objetivo es MINIMIZAR)
            pts(i) = +inf;
        end

        % (Opcional) Mostrar progreso en porcentaje:
        % fprintf('Evaluando => %3.4f%%\n', (i/long)*100);
    end
end


function r = pertenece(a, b, v)
% PERTENECE Verifica si un punto (v) está dentro del dominio [a, b].
%
% Sintaxis:
%   r = pertenece(a, b, v)
%
% Descripción:
%   Comprueba si el punto 2D 'v' cumple con los límites de ambos ejes
%   (x dentro de [a(1), b(1)] y y dentro de [a(2), b(2)]).
%   Además, descarta el caso donde alguna coordenada sea 0.
%
% Parámetros:
%   a, b -> Vectores con los límites inferior y superior del dominio.
%   v    -> Punto a verificar, vector fila [x y].
%
% Salida:
%   r -> Valor lógico (1 si pertenece, 0 si no).

    r = ...
        ((a(1) <= v(1)) && (v(1) <= b(1))) && ...  % X dentro del rango
        ((a(2) <= v(2)) && (v(2) <= b(2))) && ...  % Y dentro del rango
        ((v(1) ~= 0) && (v(2) ~= 0));              % Ninguna coordenada igual a 0
end
