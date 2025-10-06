clear all
clc
% Abrir el archivo de video
 pkg load video
 pkg load image

close all

lista=dir("*.mp4");
for i=1:size(lista,1)

   disp('procesando archivo..');
   disp(lista(i).name);
   imF=estimacionFondo(lista(i).name, 200);

   save(sprintf("%s.oct",lista(i).name),"imF");
end

for i=1:size(lista,1)

   disp('procesando archivo..');
   disp(lista(i).name);

   load(sprintf("%s.oct",lista(i).name));
   disp(size(imF));
   imwrite(uint8(imF),sprintf("%s.jpg",lista(i).name),"jpg","Quality",100);
end

