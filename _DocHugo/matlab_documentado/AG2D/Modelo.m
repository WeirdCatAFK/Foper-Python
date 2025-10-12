function P = Modelo(alpha, y)
% MODELO Aplica un filtro exponencial simple a un vector de datos.
%
% Sintaxis:
%   P = Modelo(alpha, y)
%
% Descripción:
%   Esta función suaviza la señal o vector de datos 'y' mediante un
%   filtro recursivo de primer orden. Cada nuevo valor filtrado se
%   calcula como una combinación ponderada del valor anterior filtrado
%   y del nuevo valor de entrada.
%
%   Matemáticamente:
%       P(i) = (1 - alpha) * P(i-1) + alpha * y(i)
%
%   Donde:
%       - alpha controla el “peso” de la nueva observación (0 < alpha <= 1)
%       - Un alpha pequeño produce un suavizado fuerte (respuesta lenta)
%       - Un alpha cercano a 1 produce menor suavizado (respuesta rápida)
%
% Parámetros:
%   alpha -> Coeficiente de suavizado
%   y     -> Vector de datos de entrada
%
% Salida:
%   P -> Vector de salida filtrado

    % Inicializa el vector de salida con ceros del mismo tamaño que y
    P = zeros(size(y));

    % El primer valor filtrado es igual al primer valor de entrada
    P(1) = y(1);

    % Aplica el filtro recursivo para el resto de los elementos
    for i = 2:length(y)
        P(i) = (1 - alpha) * P(i-1) + alpha * y(i);
    end
end
