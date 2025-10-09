function Modelo = estimacionFondo(nVideo, cuadros)
    % ------------------------------------------------------------
    %  FUNCIÓN: estimacionFondo
    % ------------------------------------------------------------
    %  Descripción:
    %  Calcula un modelo de fondo promedio a partir de los primeros
    %  'cuadros' frames de un video. Este modelo se obtiene mediante
    %  un promedio incremental (running average) sobre las imágenes
    %  en escala de grises.
    %
    %  Parámetros de entrada:
    %    nVideo  - Ruta o nombre del archivo de video.
    %    cuadros - Número de cuadros a procesar para estimar el fondo.
    %
    %  Salida:
    %    Modelo  - Imagen resultante que representa el fondo estimado.
    %
    %  Ejemplo:
    %    Modelo = estimacionFondo('video.mp4', 200);
    %
    % ------------------------------------------------------------

    disp('Cargando video...');
    archivo = VideoReader(nVideo); % Abre el archivo de video
    disp('Estimando el modelo de fondo...');

    % ------------------------------------------------------------
    %  CONFIGURACIÓN INICIAL
    % ------------------------------------------------------------
    escala = 1; % Factor de reducción de tamaño de imagen
    contador = 1; % Contador de cuadros leídos

    % ------------------------------------------------------------
    %  BUCLE PRINCIPAL DE LECTURA DE VIDEO
    % ------------------------------------------------------------
    % Se leen los cuadros del video uno por uno, convirtiéndolos a
    % escala de grises y actualizando el modelo de fondo mediante
    % un promedio incremental.
    %
    % Fórmula usada:
    %    Modelo = (1 - α) * Modelo + α * ImagenActual
    % donde α = 1 / contador
    % ------------------------------------------------------------

    while (!isempty(imagen = readFrame(archivo)))

        % Si es el primer cuadro, inicializa el modelo
        if (contador == 1)
            Modelo = double(imresize(rgb2gray(imagen), escala));
        end

        % Convierte el cuadro actual a escala de grises y tipo double
        imagenG = double(imresize(rgb2gray(imagen), escala));

        % Actualiza el contador de cuadros
        contador = contador + 1;

        % Actualiza el modelo de fondo mediante promedio incremental
        Modelo = (1 - (1 / contador)) * Modelo + (1 / contador) * imagenG;

        % --- Visualización opcional del proceso ---
        % imagesc(Modelo);
        % daspect([1 1]);
        % colormap(gray);
        % drawnow;

        % Imprime el número de cuadro actual en consola
        fprintf("%d\n", contador);

        % Detiene el proceso si se alcanza el número de cuadros deseado
        if (contador > cuadros)
            break;
        end

    end

    % Cierra el archivo de video
    close(archivo);

end
