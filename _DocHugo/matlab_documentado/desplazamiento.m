function [v, e] = desplazamiento(x, y, it, it1, w)
    % DESPLAZAMIENTO  Calcula el vector de desplazamiento (v) y el error (e)
    % entre dos imágenes o regiones de imagen (it e it1).
    %
    % Entrada:
    %   x, y : coordenadas (vectores columna) de los píxeles a comparar.
    %   it   : primera imagen o región de referencia.
    %   it1  : segunda imagen o región desplazada.
    %   w    : radio de búsqueda (ventana de desplazamiento).
    %
    % Salida:
    %   v : vector [dx; dy] con el desplazamiento que minimiza el error.
    %   e : error mínimo encontrado (métrica de similitud).
    %
    % Descripción:
    %   La función realiza una búsqueda exhaustiva (por fuerza bruta)
    %   dentro de una ventana de tamaño (2w+1)x(2w+1), comparando
    %   intensidades entre las posiciones (x, y) de 'it' y las posiciones
    %   desplazadas (x+dx, y+dy) en 'it1'.
    %   Se usa la diferencia absoluta promedio (SAD) como métrica de error.

    % --- Obtener intensidades base de la imagen it en las coordenadas (x, y)
    It = it(sub2ind(size(it), y, x));

    % --- Inicializar variables
    minimo = inf; % Valor inicial muy grande (para comparar)
    v = zeros(2, 1); % Vector de desplazamiento [dx; dy]
    ne = size(x, 1); % Número de elementos (píxeles) evaluados

    % --- Búsqueda exhaustiva en la ventana de desplazamiento [-w, w]
    for xx = -w:w

        for yy = -w:w

            % Calcular las coordenadas desplazadas
            xd = x + xx;
            yd = y + yy;

            % Verificar que las coordenadas estén dentro de los límites de la imagen
            error = sum((xd <= 0) | (yd <= 0) | (xd > size(it, 2)) | (yd > size(it, 1)));

            if (error > 0)
                % Si alguna coordenada se sale del rango, se omite este desplazamiento
                continue;
            end

            % Obtener intensidades correspondientes en it1 para el desplazamiento actual
            It1 = it1(sub2ind(size(it1), yd, xd));

            % Calcular la métrica de similitud (SAD promedio)
            d = sum(abs(It - It1)) / ne;

            % Si se encuentra un error menor, actualizar desplazamiento óptimo
            if (d < minimo)
                v(1) = xx; % Mejor desplazamiento en x
                v(2) = yy; % Mejor desplazamiento en y
                minimo = d; % Guardar nuevo error mínimo
            end

        end

    end

    % --- Devolver el error mínimo encontrado
    e = minimo;
end
