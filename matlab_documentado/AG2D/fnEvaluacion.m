function salida = fnEvaluacion(X, d)
% FNEVALUACION Evalúa el grado de similitud entre dos imágenes desplazadas.
%
% Sintaxis:
%   salida = fnEvaluacion(X, d)
%
% Descripción:
%   Esta función calcula una métrica de similitud entre una imagen base
%   (almacenada en 'd.It') y una imagen desplazada ('d.imd'), aplicando un
%   desplazamiento 2D indicado por el vector X = [dx, dy].
%
%   El objetivo es encontrar el desplazamiento (X) que minimiza la
%   diferencia entre ambas imágenes. Por lo tanto, un valor menor de salida
%   implica una mejor coincidencia.
%
% Parámetros:
%   X -> Vector [dx, dy] que indica el desplazamiento horizontal y vertical
%        aplicado a la región de interés.
%
%   d -> Estructura con los siguientes campos:
%        - d.imd : Imagen desplazada (matriz de intensidad)
%        - d.imi : Imagen original o base (usada para referencia)
%        - d.It  : Intensidades de la región de referencia
%        - d.X, d.Y : Coordenadas de los píxeles dentro de la ventana
%                     de comparación (vectores o matrices de igual tamaño)
%
% Salida:
%   salida -> Valor escalar que mide la diferencia (error) entre las
%             intensidades correspondientes. Menor = mejor coincidencia.
%             Devuelve NaN si el desplazamiento saca la región fuera
%             de los límites de la imagen.

    % Extrae la imagen desplazada (matriz completa)
    it1 = d.imd;

    % Calcula las coordenadas desplazadas según X = [dx, dy]
    xd = d.X(:) + X(1);  % desplazamiento en eje X (horizontal)
    yd = d.Y(:) + X(2);  % desplazamiento en eje Y (vertical)

    % ---- Validación de límites ----
    % Verifica que todas las coordenadas desplazadas estén dentro
    % de los límites válidos de la imagen.
    error = sum((xd <= 0) | (xd > size(d.imi, 2)) | (yd <= 0) | (yd > size(d.imi, 1)));

    % Si alguna coordenada está fuera del rango, se devuelve NaN
    if (error > 0)
        salida = NaN;
        return;
    end

    % ---- Métrica de similitud ----
    % Obtiene los valores de intensidad correspondientes en la imagen desplazada.
    % 'sub2ind' convierte (fila, columna) → índice lineal.
    It1 = it1(sub2ind(size(it1), yd, xd));

    % Calcula la diferencia absoluta entre intensidades originales y desplazadas
    % y promedia el resultado. Esta es una métrica tipo “error absoluto medio”.
    salida = sum(abs(d.It - It1)) / size(It1, 1);

    % (Alternativa comentada)
    % salida = d;
end
