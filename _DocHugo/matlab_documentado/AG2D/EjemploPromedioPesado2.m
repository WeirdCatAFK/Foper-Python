%% -----------------------------------------------------------
% FILTRADO DE SEÑAL CON PROMEDIO EXPONENCIAL
% -----------------------------------------------------------

close all;

% Generar señal de prueba: seno con ruido gaussiano
x = 0:0.001:6*pi;
y = sin(x) + 0.3*randn(size(x)); % Simula un sensor con ruido

% Graficar señal original
plot(y);
hold on;

% -----------------------------------------------------------
% FILTRO EXPONENCIAL SIMPLE
% -----------------------------------------------------------
t = 0.999;                % Factor de suavizado (cercano a 1 = fuerte memoria)
P = zeros(size(y));        % Inicializar señal filtrada
P(1) = y(1);               % Condición inicial

% Aplicar filtro exponencial
for i = 2:length(y)
    P(i) = t*P(i-1) + (1-t)*y(i);  % Cada nuevo valor es combinación del anterior y la señal actual
end

% Graficar señal filtrada sobre la original
plot(P, 'linewidth', 3);   % Señal filtrada en línea más gruesa
