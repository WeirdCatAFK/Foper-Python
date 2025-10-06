function Modelo=estimacionFondo(nVideo,cuadros)

disp('Cargando video..');
archivo = VideoReader (nVideo);
%archivo = VideoReader ('f:\\grabacion.73.MP4');
disp('Estimando el  modelo de fondo..');
% Configuracion de fondo

escala=1;
% Estimación del Fondoclear
contador=1;
%return;
%figure;
while (! isempty (imagen= readFrame (archivo)))
   if(contador==1)
      Modelo=double(imresize(rgb2gray(imagen),escala));
   end

   imagenG=double(imresize(rgb2gray(imagen),escala));
   contador=contador+1;
   Modelo=(1-(1/contador))*Modelo+(1/contador)*imagenG;

   %imagesc(Modelo);
   %daspect([1 1]);
   %colormap(gray);
   %drawnow;
   fprintf("%d\n",contador);
   if(contador >cuadros)
      break;
   end
end
close(archivo);
end
