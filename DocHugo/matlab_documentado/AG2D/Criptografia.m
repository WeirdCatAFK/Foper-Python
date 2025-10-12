% -----------------------------------------------------------
% CIFRADO Y DESCIFRADO DE IMÁGENES CON XOR Y GENERADOR ALEATORIO
% -----------------------------------------------------------

close all;

% Contraseña que se usará para generar la semilla
password = 'fulanito2';

% Cargar imagen a cifrar
imagen = imread('imagen.jpg');
figure; image(imagen); % Mostrar imagen original

% Crear generador pseudoaleatorio con semilla derivada de la contraseña
gen = crearGenerador( ...
    sumaTexto(password), ...        % Convierte la contraseña en un número
    primoSiguiente(1000000), ...   % Números primos para parámetros del generador
    primoSiguiente(900000) ...
);

% Dimensiones de la imagen
dim = size(imagen);

% Aplanar la imagen en un vector de bytes
mensaje = uint8(imagen(:));

% Generar secuencia aleatoria para cifrado
L = uint8(zeros(size(mensaje)));
for i = 1:length(mensaje)
    gen = sigAzar(gen);           % Generar nuevo valor pseudoaleatorio
    L(i) = uint8(gen.xn * 255);  % Escalar a rango 0-255
end

% -----------------------------------------------------------
% CIFRADO: XOR entre la imagen y la secuencia pseudoaleatoria
% -----------------------------------------------------------
mensajeE = uint8(zeros(size(mensaje)));
for i = 1:length(mensaje)
    mensajeE(i) = bitxor(mensaje(i), L(i)); % Operación XOR
end

% Reconstruir la imagen cifrada con las mismas dimensiones
Ei = reshape(mensajeE, dim);
disp('Mensaje encriptado');
figure; image(Ei); % Mostrar imagen cifrada

% -----------------------------------------------------------
% DESCIFRADO: usando la misma contraseña
% -----------------------------------------------------------
password = 'fulanito'; % Contraseña para descifrar (debe ser la misma)

% Regenerar la secuencia pseudoaleatoria
gen = crearGenerador( ...
    sumaTexto(password), ...
    primoSiguiente(1000000), ...
    primoSiguiente(900000) ...
);

L = uint8(zeros(size(mensajeE)));
for i = 1:length(mensajeE)
    gen = sigAzar(gen);
    L(i) = uint8(gen.xn * 255);
end

% Aplicar XOR de nuevo para recuperar la imagen original
mensajeR = uint8(zeros(size(mensajeE)));
for i = 1:length(mensajeE)
    mensajeR(i) = bitxor(mensajeE(i), L(i));
end

disp('Mensaje Des-encriptado');
Er = reshape(mensajeR, dim); % Reconstruir imagen original
figure; image(Er); % Mostrar imagen descifrada
