pkg load image % Carga el paquete de procesamiento de imágenes (Octave)

%% -----------------------------------------------------------
%  ALGORITMO DE DISPARIDAD ESTÉREO POR FUERZA BRUTA
% ------------------------------------------------------------
% Este script calcula un mapa de disparidad entre dos imágenes
% (izquierda y derecha) de una escena, mediante búsqueda exhaustiva
% de desplazamientos locales usando la función 'desplazamiento'.
% ------------------------------------------------------------

clear all          % Limpia todas las variables
close all % Cierra todas las figuras abiertas

escala = 0.4; % Escala para redimensionar las imágenes

% --- Cargar y redimensionar imágenes
imo = imresize(imread('DJI_20250815114314_0028_D.MP4.jpg'), 0.4);
imd = single(imresize(imread('DJI_20250815114314_0028_D.MP4.jpg'), escala)); % Imagen derecha
imi = single(imresize(imread('DJI_20250815114458_0029_D.MP4.jpg'), escala)); % Imagen izquierda

% --- Aplicar un filtro gaussiano para suavizar el ruido
f = fspecial('gaussian', 9, 1.0);
imd = conv2(imd, f, 'same') ./ 255;
imi = conv2(imi, f, 'same') ./ 255;

% --- Preparar figura principal con las imágenes base
figure(1, "position", [0 0 1920 1080]);
colormap(gray);

subplot(231);
image(imresize(imread('DJI_20250815114314_0028_D.MP4.jpg'), escala));
hold on; title("Imagen Izquierda"); daspect([1 1]);

subplot(232);
image(imresize(imread('DJI_20250815114458_0029_D.MP4.jpg'), escala));
hold on; title("Imagen Derecha"); daspect([1 1]);

% --- Inicializar matrices de resultados
M = zeros([size(imd) 2]); % Vectores de desplazamiento (dx, dy)
NM = nan * zeros(size(imd)); % Norma (magnitud del vector)
E = nan * zeros(size(imd)); % Error mínimo de similitud

% --- Parámetros del algoritmo
r = 15; % Tamaño de la ventana local (región de comparación)
R = 55; % Rango máximo de búsqueda (desplazamiento máximo)
muestreo = 2; % Factor de muestreo (reduce el número de píxeles evaluados)

% ------------------------------------------------------------
%  Bucle principal: recorre la imagen y calcula disparidad
% ------------------------------------------------------------
for y = 1 + r:muestreo:size(imd, 1) - r

    for x = 1 + r:muestreo:size(imd, 2) - r

        % Definir la ventana local alrededor del píxel (x, y)
        rx = x - r:x + r;
        ry = y - r:y + r;
        [X, Y] = meshgrid(rx, ry);

        % Calcular desplazamiento y error mínimo usando la función auxiliar
        [d, e] = desplazamiento(X(:), Y(:), imd, imi, R);

        % Guardar resultados
        M(y, x, 1) = d(1);
        M(y, x, 2) = d(2);
        NM(y, x) = sqrt(d(1) .^ 2 + d(2) .^ 2); % Norma del vector de desplazamiento
        E(y, x) = e; % Error de similitud

        fprintf("(x=%04d y=%04d)\n", x, y); % Progreso de cálculo
    end

    % --- Visualizaciones en tiempo real ---
    subplot(234);
    imagesc(NM); daspect([1 1]);
    title("Norma del Vector de Desplazamiento");
    colorbar;

    subplot(235);
    imagesc(E); daspect([1 1]);
    title("Error Mínimo de Similitud");
    colorbar;

    subplot(233);
    NMM = NM(:);
    hist(NMM(NMM > 0), 50);
    title("Distribución de la Norma");

    subplot(236);
    EE = E(:);
    hist(EE(EE > 0), 50);
    title("Distribución del Error");

    figure(1, "position", [0 0 1920 1080]);
    drawnow; % Actualiza las figuras en pantalla
    y, % Muestra el índice de línea (progreso)
end

%% ------------------------------------------------------------
%  Bloque opcional: Visualización 3D del mapa de disparidad
% ------------------------------------------------------------
%{
[X, Y] = meshgrid(1:size(imd,2), 1:size(imd,1));
R = double(imo(:,:,1)); R = R(sub2ind(size(NM), Y(:), X(:))) / 255;
G = double(imo(:,:,2)); G = G(sub2ind(size(NM), Y(:), X(:))) / 255;
B = double(imo(:,:,3)); B = B(sub2ind(size(NM), Y(:), X(:))) / 255;
Z = NM(sub2ind(size(NM), Y(:), X(:)));
X = X(:); Y = Y(:);
figure; hold on
for i = 1:length(X)
    plot3(X(i), Y(i), Z(i), '.', 'MarkerFaceColor', [R(i) G(i) B(i)]);
end
%}

%% ------------------------------------------------------------
%  Guardado de resultados y visualización del componente X del desplazamiento
% ------------------------------------------------------------
MX = zeros(size(NM));

for y = 1 + r:1:size(imd, 1) - r

    for x = 1 + r:1:size(imd, 2) - r
        MX(y, x) = M(y, x, 1);
    end

end

figure;
imagesc(MX); % Mapa de desplazamiento en eje X
save "DatosFif" % Guarda todas las variables en archivo .mat

%% ------------------------------------------------------------
%  Carga de datos y refinamiento del mapa de disparidad
% ------------------------------------------------------------
imo = imresize(imread('DJI_20250815114458_0029_D.MP4.jpg'), escala);
load("DatosFif");

figure;
borde = 60; % Margen que se recorta para eliminar bordes ruidosos
NM = NM(:, borde:end - borde);
imo = imo(:, borde:end - borde, :);

% Eliminar valores de norma no válidos o demasiado grandes/pequeños
BB = (NM > 45) | (NM < 0.01);
SS = size(NM);
[y, x] = find(BB == 1);
NM(sub2ind(SS, y, x)) = NaN;

% --- Visualización de superficie 3D con textura de la imagen original ---
[X, Y] = meshgrid(1:size(imo, 2), 1:size(imo, 1));
surface(X, Y, NM, imo, 'EdgeColor', 'none', 'FaceAlpha', 0.5);

figure;
mesh(NM); % Malla 3D del mapa de disparidad

%% ------------------------------------------------------------
%  Interpolación y curvas de nivel del mapa de disparidad
% ------------------------------------------------------------
[y, x] = find(~isnan(NM)); % Píxeles válidos
z = NM(sub2ind(size(NM), y(:), x(:)));

figure;
plot3(x, y, z, '.b', 'markersize', 1);
zlim([20 50]);
grid on;

% --- Interpolación en malla regular ---
figure;
[xq, yq] = meshgrid(linspace(min(x), max(x), size(NM, 1)), ...
    linspace(min(y), max(y), size(NM, 2)));
zq = griddata(x, y, z, xq, yq, "linear"); % Interpolación lineal

% --- Curvas de nivel (contornos de disparidad) ---
contour(xq, yq, zq, 20);
colorbar;
xlabel("X"); ylabel("Y");
title("Curvas de nivel interpoladas");

% --- Superficie suavizada ---
figure;
surf(zq);
colormap(bone);
shading interp;
material dull;
light("position", [200 200 100], "style", "infinite");
zlabel([20, 50]);
