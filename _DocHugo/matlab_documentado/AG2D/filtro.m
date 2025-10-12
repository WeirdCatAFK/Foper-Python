function Y = filtro(X, rho)
% FILTRO Aplica un filtro suavizador exponencial (filtro de primer orden).
%
% Sintaxis:
%   Y = filtro(X, rho)
%
% Descripción:
%   Esta función implementa un filtro recursivo simple para suavizar una
%   señal o vector de datos. Cada nuevo valor filtrado se calcula como
%   una combinación ponderada entre el valor anterior filtrado y el nuevo
%   valor de entrada, controlado por el parámetro 'rho'.
%
%   Matemáticamente:
%       Y(i) = (1 - rho) * Y(i-1) + rho * X(i)
%
%   Donde:
%       - rho controla la “velocidad” del filtro (0 < rho <= 1)
%       - Un rho pequeño produce una respuesta lenta (más suavizado)
%       - Un rho cercano a 1 produce una respuesta rápida (menos suavizado)
%
% Parámetros:
%   X   -> Vector de entrada (datos originales)
%   rho -> Coeficiente de suavizado (constante de filtro)
%
% Salida:
%   Y -> Vector con los valores suavizados

    % Inicializa el vector de salida con ceros del mismo tamaño que X
    Y = zeros(size(X));

    % El primer valor filtrado es igual al primer valor de entrada
    Y(1) = X(1);

    % Aplica el filtro recursivo para el resto de los elementos
    for i = 2:length(Y)
        Y(i) = (1 - rho) * Y(i - 1) + rho * X(i);
    end
end
