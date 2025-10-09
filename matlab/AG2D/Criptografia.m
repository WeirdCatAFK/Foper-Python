close all
password='fulanito2';
imagen=imread('imagen.jpg');
figure;image(imagen);

gen=crearGenerador(sumaTexto(password),...
    primoSiguiente(1000000),...
    primoSiguiente(900000));

dim=size(imagen);%%%%%%%%%%%%%%%%%%%%%%%%%
mensaje=uint8(imagen(:));%%%%%%%%%%%%%%%%%%
L=uint8(zeros(size(mensaje)));
for i=1:length(mensaje)
    gen=sigAzar(gen);
    L(i)=uint8(gen.xn*255);
end
% Encriptacion
mensajeE=uint8(zeros(size(mensaje)));
for i=1:length(mensaje)
    mensajeE(i)=bitxor((mensaje(i)),L(i));
end
Ei=reshape(mensajeE,dim);%%%%%%%%%%%%%%%%%%
disp('Mensaje encriptado');%%%%%%%%%%%%%%%%
figure;image(Ei); %%%%%%%%%%%%%%%%%%%%%%%%
%% DESENCRIPTAR

password='fulanito';

gen=crearGenerador(sumaTexto(password),...
    primoSiguiente(1000000),...
    primoSiguiente(900000));

L=uint8(zeros(size(mensajeE))); %%%%%%%%%%%%%%%%
for i=1:length(mensajeE)
    gen=sigAzar(gen);
    L(i)=uint8(gen.xn*255);
end
% Encriptacion
mensajeR=uint8(zeros(size(mensajeE)));%%%%%%%%%%%%%%%
for i=1:length(mensajeE)
    mensajeR(i)=bitxor((mensajeE(i)),L(i)); %%%%%
end
disp('Mensaje Des-encriptado');
Er=reshape(mensajeR,dim);%%%%%%%%%%%%%%%%%%
figure;image(Er); %%%%%%%%%%%%%%%%%%%%%%%%

%