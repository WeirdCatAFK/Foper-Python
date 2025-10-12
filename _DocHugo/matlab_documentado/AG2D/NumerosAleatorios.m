% -----------------------------------------------------------
% INICIALIZACIÓN DEL GENERADOR DE NÚMEROS ALEATORIOS
% -----------------------------------------------------------
% Se crean semillas usando tiempo actual y números primos para generar
% secuencias pseudoaleatorias reproducibles
gen = crearGenerador( ...
    (cputime - fix(cputime)) * 100000, ...
    primoSiguiente(1000000), ...
    primoSiguiente(900000) ...
);

%% Ejemplo 1: Integración Monte Carlo V1 (área bajo línea)
close all
a = 5;       % límite inferior en x
b = 8;       % límite superior en x
h = 25;      % altura máxima para área del rectángulo
AC = (b - a) * h;  % área total del rectángulo de referencia

x = 0:0.1:10;         % eje x
y = 2.5*x + 3;        % función lineal y = 2.5x + 3
subplot(1,2,1);
plot(x, y, 'b');      % dibuja la función original

%% Monte Carlo V1 (área bajo curva)
abajo = 0;             % contador de puntos debajo de la curva
k = 100000;            % número de puntos aleatorios
AH = [];               % historial de áreas aproximadas

for i = 1:k
    % Genera punto aleatorio en x
    gen = sigAzar(gen);
    x = (b - a) * gen.xn + a;

    % Genera punto aleatorio en y
    gen = sigAzar(gen);
    y = h * gen.xn;

    subplot(1,2,1);
    hold on;

    % Verifica si el punto está debajo de la curva y = 2.5x + 3
    if (y < 2.5*x + 3)
        abajo = abajo + 1;
        plot(x, y, '.k'); % punto negro si está debajo
    else
        plot(x, y, '.r'); % punto rojo si está arriba
    end

    % Calcula área aproximada hasta el momento
    subplot(1,2,2);
    A = abajo / i * AC;
    AH = [AH; A];
    plot(AH);
    title(sprintf('Area Aprox %3.4f', A));
    drawnow;
    pause(0.01);
end

A = abajo / k * AC; % área final aproximada

%% Gráfica 3D para visualización Monte Carlo V1
figure;
hold on;
axis on; grid on;
for x = 0:0.1:2*pi
    for y = 0:0.1:2*pi
        z = sin(x) * cos(y) + 1;
        plot3(x, y, z, '.b', 'markersize', 1);
    end
end

%% Monte Carlo V1: cálculo de volumen bajo superficie 3D
limx = [3, 5]; limy = [3, 5]; limz = 3;  % límites del cubo
abajo = 0;   % contador de puntos bajo la superficie
k = 100000;  % número de puntos aleatorios
vC = (limx(2)-limx(1)) * (limy(2)-limy(1)) * limz; % volumen del cubo

hold on;
for i = 1:k
    % Genera punto aleatorio normalizado en 3D
    gen = sigAzar(gen); x = gen.xn;
    gen = sigAzar(gen); y = gen.xn;
    gen = sigAzar(gen); z = gen.xn;

    % Escala los puntos a los límites reales
    x = (limx(2) - limx(1)) * x + limx(1);
    y = (limy(2) - limy(1)) * y + limy(1);
    z = limz * z;

    % Verifica si el punto está debajo de la superficie z = sin(x)*cos(y)+1
    if (z < sin(x) * cos(y) + 1)
        abajo = abajo + 1;
        plot3(x, y, z, '.r'); % rojo debajo de la superficie
    else
        plot3(x, y, z, '.k'); % negro encima de la superficie
    end

    % Volumen aproximado hasta el momento
    ev = vC * (abajo / i);
    title(sprintf('volumen aproximado %3.3f', ev));
    drawnow;
end

%% Ejemplo 1: Integración Monte Carlo V2 (suma de alturas)
close all
a = 5; b = 8; h = 25;
AC = (b-a) * h;
x = 0:0.1:10;
y = 2.5*x + 3;
subplot(1,2,1);
plot(x, y, 'b');

s = 0; k = 100000; AH = [];
for i = 1:k
    gen = sigAzar(gen);
    x = (b - a) * gen.xn + a;
    subplot(1,2,1); hold on;
    y = 2.5*x + 3;
    s = s + y;  % suma de alturas

    plot([x; x], [0; y], 'k'); % línea vertical hasta la función

    subplot(1,2,2);
    A = s / i; AH = [AH; A]; % promedio hasta el momento
    plot(AH);
    title(sprintf('Area Aprox %3.4f', A));
    drawnow;
    pause(0.01);
end

%% Monte Carlo V2: volumen 3D por promedio de alturas
figure; hold on; axis on; grid on;
for x = 0:0.1:2*pi
    for y = 0:0.1:2*pi
        z = sin(x) * cos(y) + 1;
        plot3(x, y, z, '.b', 'markersize', 1);
    end
end

limx = [3,5]; limy = [3,5]; limz = 3;
s = 0; k = 100000;
hold on;
for i = 1:k
    gen = sigAzar(gen); x = gen.xn;
    gen = sigAzar(gen); y = gen.xn;

    x = (limx(2) - limx(1)) * x + limx(1);
    y = (limy(2) - limy(1)) * y + limy(1);

    z = sin(x) * cos(y) + 1;
    plot3([x;x],[y;y],[0;z],'r'); % línea vertical hasta la superficie
    s = s + z;

    ev = s / i; % promedio de alturas (volumen aproximado)
    title(sprintf('volumen aproximado %3.3f', ev));
    drawnow;
end
