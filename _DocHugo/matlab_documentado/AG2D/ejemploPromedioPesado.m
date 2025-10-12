close all;

% Generar señal de prueba: combinación de seno con ruido gaussiano
x = 0:0.001:(2*pi)*4;
y = 1 + sin(x) + 0.2*randn(size(x));

% Alternativa más compleja (comentada)
% y = sin(x) + 0.3*cos(16*x) + 0.2*randn(size(x));

% Graficar señal original
plot(y);

% Guardar señal en archivo para uso posterior
save('datos', 'y');

% Parámetro de precisión para el algoritmo genético
p = 0.0001;

% -----------------------------------------------------------
% EJECUCIÓN DEL ALGORITMO GENÉTICO
% -----------------------------------------------------------
sol = genetico(0.1, 0.9, p, 100, 1000, 0.1, 5);

% Ajustar señal usando el modelo generado por el algoritmo genético
ye = Modelo(sol, y);

hold on;
plot(ye);  % Graficar señal ajustada sobre la original

return  % Termina ejecución antes del siguiente bloque

%% -----------------------------------------------------------
% ANIDAMIENTO DE FILTRADO CON ITERACIONES MÚLTIPLES
% -----------------------------------------------------------

Y = zeros(100, length(y));  % Guardar señales ajustadas
R = zeros(100, length(y));  % Guardar residuales

for i = 1:100
    fprintf('Anidamiento %d.\n', i);
  
    % Ejecutar algoritmo genético en cada iteración
    sol = genetico(p, 1-p, p, 40, 10, 0.1, 20);
    
    % Aplicar filtro a la señal usando los parámetros encontrados
    ye = filtro(y, sol);
    
    % Guardar resultados
    Y(i, :) = ye;           % Señal filtrada
    R(i, :) = y - ye;       % Residual
    y = ye;                 % Actualizar señal para la siguiente iteración
   
    % Guardar datos en archivo
    save('datos', 'y');
    
    % Visualización de resultados
    subplot(2,1,1);
    hold on; plot(y, 'r');       % Señal filtrada en rojo
    subplot(2,1,2);
    plot(R(i, :)); drawnow;      % Residual
end
