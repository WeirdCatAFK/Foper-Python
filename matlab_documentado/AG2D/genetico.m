function Solucion=genetico(a,b,epsilon,n,soldaditos,mutacion,r,d,debug)
% -----------------------------------------------------------
% Algoritmo genético para optimización 2D (minimización)
%
% Parámetros:
%   a, b      -> Límites inferiores y superiores del dominio [a1, a2], [b1, b2]
%   epsilon   -> Precisión con la que se discretiza el espacio
%   n         -> Número de generaciones (iteraciones)
%   soldaditos-> Tamaño de la población inicial
%   mutacion  -> Probabilidad de mutación
%   r         -> Número máximo de generaciones sin mejora antes de reiniciar
%   d         -> Estructura con información del problema (imagenes, coordenadas, etc.)
%   debug     -> Si es 1, imprime información de depuración
%
% Retorna:
%   Solucion = [x_best, y_best, f_best]  mejor posición y su evaluación
% -----------------------------------------------------------

global pot1
global pot2

% -----------------------------------------------------------
% Cálculo del número de bits necesarios para codificar cada variable
% -----------------------------------------------------------

m(1)=fix(log2((b(1)-a(1))/epsilon)+1);  % Bits para la coordenada X
if (mod(m(1),2)==1)                     % Si el número de bits es impar, hacerlo par
    m(1)=m(1)+1;
end
pot1=2.^(m(1)-1:-1:0);                  % Vector de potencias de 2 (para decodificación)

m(2)=fix(log2((b(2)-a(2))/epsilon)+1);  % Bits para la coordenada Y
if (mod(m(2),2)==1)                     % Si el número de bits es impar, hacerlo par
    m(2)=m(2)+1;
end
pot2=2.^(m(1)-1:-1:0);                  % (Nota: probablemente debería usar m(2), 
                                        % posible error en el código original)

% -----------------------------------------------------------
% Inicialización de la población
% -----------------------------------------------------------
[puntos,ptsReal]=inicializacion(a,b,epsilon,m,soldaditos);
% puntos   -> matriz binaria con la codificación genética
% ptsReal  -> coordenadas reales correspondientes (decodificadas)

solG=+inf;       % Mejor valor encontrado (inicialmente infinito)
solx=[0 0];      % Coordenadas de la mejor solución
nr=0;            % Contador de generaciones sin mejora
Solucion=[NaN NaN NaN];  % Estructura de salida por defecto

% -----------------------------------------------------------
% Bucle principal del algoritmo genético
% -----------------------------------------------------------
for i=1:n
    % Evaluación de la población
    ptsy=evaluacion(a,b,epsilon,puntos,ptsReal,d);

    % Encontrar el mejor individuo de la generación
    [sol,p]=min(ptsy);

    % -------------------------------------------------------
    % Si se encontró una mejor solución, actualizarla
    % -------------------------------------------------------
    if(solG>sol)
        solG=sol;
        % Decodificar el mejor individuo a valores reales
        solx(1)=codInv(a(1),b(1),epsilon,puntos(p,1:m(1)),pot1);
        solx(2)=codInv(a(2),b(2),epsilon,puntos(p,m(1)+1:m(1)+m(2)),pot2);

        if(debug==1)
            fprintf('Sol. Encontrada %3.1f, (%8.1f,%8.1f)\n',solG,solx(1),solx(2));
        end

        nr=1;  % Reinicia contador de generaciones sin mejora
        Solucion=[solx(1) solx(2) solG];
    else
        nr=nr+1;  % Incrementa el contador si no hubo mejora
    end

    % -------------------------------------------------------
    % Si hubo demasiadas generaciones sin mejora, reiniciar población
    % -------------------------------------------------------
    if(nr>r)
        if(debug==1)
            fprintf('Reiniciando Poblacion...\n');
        end
        [puntos,ptsReal]=inicializacion(a,b,epsilon,m,soldaditos);
        ptsy=evaluacion(a,b,epsilon,puntos,ptsReal,d);
        nr=1;
    end

    % -------------------------------------------------------
    % Operadores genéticos: selección, cruzamiento y mutación
    % -------------------------------------------------------

    indM=seleccion(a,b,epsilon,puntos,ptsy);   % Selección de los mejores
    puntos=puntos(indM,:);                     % Actualizar población con seleccionados
    puntos=cruzamiento(puntos);                % Crear descendencia (cruce)
    puntos=mutar(puntos,mutacion);             % Aplicar mutaciones
    ptsReal=codInvPts(puntos,a,b,epsilon,m);   % Decodificar población

    % -------------------------------------------------------
    % Mostrar progreso si está activado el modo debug
    % -------------------------------------------------------
    if(debug==1)
        fprintf('=>%3.2f%%, (%8.1f,%8.1f,%3.5f)\n',i/n*100,solx(1),solx(2),solG);
    end
end
