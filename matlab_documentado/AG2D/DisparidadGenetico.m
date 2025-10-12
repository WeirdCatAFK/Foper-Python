%% BÚSQUEDA DE PATRÓN EN IMAGEN USANDO ALGORITMO GENÉTICO

% Activar perfil de rendimiento (opcional, para medir tiempos)
% profile on

% Cargar imagen de referencia y convertir a escala de grises
ref = fix(rgb2gray(imread('carita.jpg')) * 255);  % Escala 0-255
[ty, tx] = size(ref);                              % Tamaño de la referencia
ref = ref > 128;                                   % Binarizar la referencia (umbral 128)

% Cargar imagen donde se buscará el patrón
i = imread('GrupoPersonas.JPG');

% Cargar otra imagen binaria (posiblemente máscara u otra referencia)
ib = imread('imbinaria.bmp');
[tiy, tix] = size(ib);                             % Tamaño de la imagen binaria

% Guardar datos relevantes en estructura
datos.ref = ref;     % Imagen de referencia binaria
datos.ib  = ib;      % Imagen binaria auxiliar
datos.ty  = ty;      % Altura de la referencia
datos.tx  = tx;      % Ancho de la referencia

% Guardar datos (comentado)
% save('datos','ref','ib','ty','tx');

% Activar profiling para analizar rendimiento
profile on

% -----------------------------------------------------------
% EJECUCIÓN DEL ALGORITMO GENÉTICO
% -----------------------------------------------------------
sol = genetico([1 1], ...                  % Límite inferior de búsqueda (origen)
               [tix-tx-1 tiy-ty-1], ...   % Límite superior (para que la referencia quepa)
               1,                          % Precisión epsilon
               100,                        % Número de iteraciones
               10000,                      % Tamaño de la población
               0.01,                       % Probabilidad de mutación
               5,                          % Número de generaciones sin mejora antes de reiniciar
               0.6,                        % Factor de similitud deseado
               datos);                      % Estructura con imágenes y tamaños

% Visualizar el perfil de rendimiento
profile viewer

% -----------------------------------------------------------
% VISUALIZACIÓN DE RESULTADOS
% -----------------------------------------------------------
figure;
imagesc(i);            % Mostrar la imagen original
colormap(gray);        % Escala de grises
hold on;

% Marcar las posiciones encontradas por el algoritmo genético
plot(sol(:,1) + datos.tx/2, ...   % Centrar sobre la referencia
     sol(:,2) + datos.ty/2, ...
     'oy', 'markersize', 10);     % Círculos amarillos de tamaño 10

% profile viewer  % (opcional para revisar rendimiento)
