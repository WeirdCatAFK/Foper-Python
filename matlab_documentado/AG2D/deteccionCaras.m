% -----------------------------------------------------------
% PROCESAMIENTO DE IMÁGENES Y BÚSQUEDA DE PATRÓN CON GENÉTICO
% -----------------------------------------------------------

%% BLOQUE COMENTADO: PRUEBAS Y EXTRACCIÓN DE MÁXIMOS LOCALES
%{
close all

% Cargar imagen y convertir a escala de grises
i = imread('grupoPersonas.JPG');
i = fix(rgb2gray(i) * 256);

% Visualización en 3D tipo mesh
mesh(i);
colormap(gray);

% Extraer máximos locales extendidos (valor h = 54)
for j = 54:54
    ib = imextendedmax(i, j);
    imagesc(ib);
    title(sprintf('valor %d.', j));
    ginput(1); % Esperar clic del usuario para continuar
end;

% Guardar imagen binaria resultante
imwrite(ib, 'imbinaria.bmp');

% Cargar referencia a buscar y binarizarla
ref = fix(rgb2gray(imread('carita.jpg'))*255);
ref = ref > 128;
[ty, tx] = size(ref);

% Visualizar referencia y región seleccionada de la imagen
figure;
subplot(1,2,1); imagesc(ref);

pi = 357; pj = 750; % Posición de prueba
region = ib(pi:pi+ty-1, pj:pj+tx-1);
subplot(1,2,2); imagesc(region);

% Calcular porcentaje de parecido entre referencia y región
valor = parecido(ref, region);
%}

%% BLOQUE PRINCIPAL: BÚSQUEDA AUTOMÁTICA CON GENÉTICO

% Cargar imagen de referencia y binarizarla
ref = fix(rgb2gray(imread('carita.jpg'))*255);
[ty, tx] = size(ref);
ref = ref > 128;

% Cargar imagen donde se buscará la referencia
i = imread('GrupoPersonas.JPG');

% Cargar imagen binaria preprocesada (máscara de máximos locales)
ib = imread('imbinaria.bmp');
[tiy, tix] = size(ib);

% Guardar datos relevantes en estructura
datos.ref = ref;    % Imagen de referencia binaria
datos.ib  = ib;     % Imagen binaria auxiliar
datos.ty  = ty;     % Altura de referencia
datos.tx  = tx;     % Ancho de referencia

% Activar profiling para análisis de rendimiento
profile on

% Ejecutar algoritmo genético para encontrar la mejor coincidencia
sol = genetico([1 1], ...                  % Límite inferior de búsqueda
               [tix-tx-1 tiy-ty-1], ...   % Límite superior (para que referencia quepa)
               1,                          % Precisión epsilon
               100,                        % Número de iteraciones
               10000,                      % Tamaño de población
               0.01,                       % Probabilidad de mutación
               5,                          % Número de generaciones sin mejora
               0.6,                        % Factor de similitud deseado
               datos);                      % Datos de imágenes

% Visualizar resultados del perfil de rendimiento
profile viewer

% Mostrar imagen original y marcar coincidencias encontradas
figure;
imagesc(i);
colormap(gray);
hold on;
plot(sol(:,1) + datos.tx/2, ...   % Centrar sobre la referencia
     sol(:,2) + datos.ty/2, ...
     'oy', 'markersize', 10);     % Círculos amarillos para posiciones encontradas
