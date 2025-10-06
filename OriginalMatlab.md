# Cálculo principal

## disparidad.m

Es el script principal que ejecuta el cálculo de disparidad “por fuerza bruta”.

Usa desplazamiento.m para encontrar el mejor desplazamiento entre ventanas locales.

Calcula mapas de:

M: vectores de desplazamiento (x, y)

NM: norma del desplazamiento (magnitud de disparidad)

E: error de similitud mínimo

Tiene mucha instrumentación gráfica (subplots con histogramas, distribución de errores, etc.)

Finalmente limpia bordes, interpola y genera superficies y curvas de nivel.

Problemas comunes o puntos de mejora:

Hace bucles anidados sobre cada pixel → extremadamente lento (O(N²·R²)).

No usa normalización de intensidad local → errores si hay diferencias de iluminación.

Mezcla single, double y uint8 sin un flujo claro.

No usa máscaras para regiones inválidas de manera robusta.

```matlab
pkg load image

%% Algoritmo por fuerza bruta para realizar el mapa de disparidad
clear all
close all

escala=0.4;

imo=imresize(imread('DJI_20250815114314_0028_D.MP4.jpg'),0.4);
imd=single((imresize(imread('DJI_20250815114314_0028_D.MP4.jpg'),escala)));
imi=single((imresize(imread('DJI_20250815114458_0029_D.MP4.jpg'),escala)));
f=fspecial('gaussian',9,1.0);%1.5);
imd=conv2(imd,f,'same')./255;
imi=conv2(imi,f,'same')./255;
figure(1,"position",[0 0 1920 1080]);
colormap(gray);
subplot(231);image(imresize(imread('DJI_20250815114314_0028_D.MP4.jpg'),escala));hold on; title("Imagen Izquierda");daspect([1 1]);
subplot(232);image(imresize(imread('DJI_20250815114458_0029_D.MP4.jpg'),escala));hold on; title("Imagen Derecha");daspect([1 1]);
M=zeros([size(imd) 2]); % Contiene el vector de desplazamiento
NM=nan*zeros(size(imd)); % Contiene la norma
E=nan*zeros(size(imd));

r=15;  			 % el tamaño de la region
R=55;  			 % La region de busqueda máxima del dezplazamiento
muestreo= 2; % Nivel de muestreo para agilizar el cómputo
for y=1+r:muestreo:size(imd,1)-r
    for x=1+r:muestreo:size(imd,2)-r
        rx=x-r:x+r;
        ry=y-r:y+r;
        [X,Y]=meshgrid(rx,ry);
        [d,e]=desplazamiento(X(:),Y(:),imd,imi,R); % El método de desplazamiento
        M(y,x,1)=d(1);
        M(y,x,2)=d(2);
        NM(y,x)=sqrt(d(1).^2+d(2).^2);
        E(y,x)=e;
				fprintf("(x=%04d y=%04d)\n",x,y);
    end
    subplot(234);
    imagesc(NM);
		daspect([1 1]);
		hold on;
		title("Norma del Vector de Dezplazamiento");
    colorbar;
		hold off
    subplot(235);
    imagesc(E);
		daspect([1 1]);
		hold on;
		title("Error Minimo de Similitud");
    colorbar;
		hold off
    subplot(233);
    NMM=NM(:);
    hist(NMM(NMM>0),50);
		hold on;
		title("Distribución de la Norma");
		hold off
    subplot(236);
    EE=E(:);
    hist(EE(EE>0),50);
		hold on;
		title("Distribución del error");
		hold off
		figure(1,"position",[0 0 1920 1080]);
    drawnow;
    y,
end
%{
[X,Y]=meshgrid(1:1:size(imd,2),1:1:size(imd,1));

figure;
R=double(imo(:,:,1));
R=R(sub2ind(size(NM),Y(:),X(:)))/255;
G=double(imo(:,:,2));
G=G(sub2ind(size(NM),Y(:),X(:)))/255;
B=double(imo(:,:,3));
B=B(sub2ind(size(NM),Y(:),X(:)))/255;
Z=NM(sub2ind(size(NM),Y(:),X(:)));
X=X(:);
Y=Y(:);
figure;
hold on
for i=1:length(X)
    plot3(X(i),Y(i),Z(i),'.','MarkerFaceColor',[R(i) G(i) B(i)]);
end
%}


%colormap hsv
%surface(X(:),Y(:),NM(sub2ind(size(NM),Y(:),X(:))),'FaceColor','interp',...
%   'EdgeColor','none',...
%   'FaceLighting','gouraud')
%daspect([5 5 1])
%axis tight
%view(-50,30)
%camlight left

%%
MX=zeros(size(NM));
for y=1+r:1:size(imd,1)-r
    for x=1+r:1:size(imd,2)-r
        MX(y,x)=M(y,x,1);
    end
end
figure;
imagesc(MX);
save "DatosFif"
%%
imo=imresize(imread('DJI_20250815114458_0029_D.MP4.jpg'),escala);

load("DatosFif");
figure;
borde=60;
NM=NM(:,borde:end-borde);
imo=imo(:,borde:end-borde,:);
BB=(NM>45)|(NM<0.01);
SS=size(NM);

[y,x]=find(BB==1);
NM(sub2ind(SS,y,x))=NaN;
[X,Y]=meshgrid(1:1:size(imo,2),1:1:size(imo,1));
surface(X,Y,NM,imo,'EdgeColor','none','FaceAlpha',0.5)
figure;
mesh(NM);


##
[y,x]=find(isnan(NM)==0);

z=NM(sub2ind(size(NM),y(:),x(:)));

figure;
plot3(x,y,z,'.b','markersize',1);
zlim([20 50]);
grid on

figure;
[xq, yq] = meshgrid(linspace(min(x), max(x), size(NM,1)), linspace(min(y), max(y), size(NM,2)));

zq = griddata(x, y, z, xq, yq, "linear");  % Puedes usar "linear", "nearest", o "cubic"

contour(xq, yq, zq, 20);  % El número 20 indica cuántas curvas de nivel quieres
colorbar;
xlabel("X");
ylabel("Y");
title("Curvas de nivel interpoladas");
figure;
surf(zq);
colormap(bone);
shading "interp"
material dull
light("position",[200 200 100],"style","infinite")
zlabel([20,50]);
```

## desplazamiento.m

Función auxiliar que calcula el desplazamiento óptimo (dx, dy) comparando dos parches.

Para cada desplazamiento dentro de [-w, w] calcula: d= $ \frac {1}{N} $ $ \sum _ {i=1}^ {1} $ -1+1

Escoge el desplazamiento con el mínimo error absoluto promedio.
Es el núcleo del algoritmo por fuerza bruta.
El problema es que no usa correlación normalizada ni ventanas ponderadas (como SAD o NCC), lo que hace que sea sensible al brillo y al ruido.

```matlab
function [v,e]=desplazamiento(x,y,it,it1,w)
It=it(sub2ind(size(it),y,x));
minimo=inf;
v=zeros(2,1);
ne=size(x,1);
for xx=-w:w
    for yy=-w:w
        xd=x+xx;
        yd=y+yy;
        error=sum((xd<=0)|(yd<=0)|(xd>size(it,2))|(yd>size(it,1)));
        if(error>0)
            continue;
        end
        It1=it1(sub2ind(size(it1),yd,xd));
        d=sum(abs(It-It1))/ne; % Métrica que se usa para medir la similitud
        if(d<minimo)
				    v(1)=xx;
						v(2)=yy;
            minimo=d;
        end
    end
end
e=minimo;
```

## estimacionFondo.m

Calcula el modelo de fondo promedio de un video.
Lee cada cuadro y hace un promedio acumulativo:

$ M* {n+1} $ =(1- $ \frac {1}{n} $ ) $ M* {n} $ + $ \frac {1}{n} $ $ I\_ {n} $
Útil para obtener una imagen “limpia” sin movimiento.

```matlab
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
```

## EstimacionImagenes.m

Script que:

Carga todos los videos .mp4 en la carpeta.

Llama a estimacionFondo para cada uno (200 cuadros).

Guarda el modelo como .oct y exporta una imagen .jpg.

Sirve para generar las imágenes base del par estéreo (izquierda/derecha).

```matlab
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
```

# Variaciones

## disparidadShi.m

Una versión más avanzada del cálculo de disparidad:

Usa gradientes ([gc, gr] = gradient(imd)) para ayudar en la estimación.

Llama a track, que parece una función de seguimiento óptico tipo Lucas-Kanade o Shi–Tomasi.

Es más eficiente y más preciso, pero depende de una función externa track.m que no incluiste.

```matlab
%% Algoritmo por fuerza bruta para realizar el mapa de disparidad
clear all
close all
imo=imresize(imread('DSCF9319_001.jpg'),0.4);
imd=single(rgb2gray(imresize(imread('DSCF9319_001.jpg'),0.4)));
imi=single(rgb2gray(imresize(imread('DSCF9319_002.jpg'),0.4)));
f=fspecial('gaussian',9,1.0);%1.5);
imd=conv2(imd,f,'same')./255;
imi=conv2(imi,f,'same')./255;
figure;
colormap(gray);
subplot(231);imagesc(imd);
subplot(232);imagesc(imi);
M=zeros([size(imd) 2]); % Contiene el vector de desplazamiento
NM=nan*zeros(size(imd)); % Contiene la norma 
E=nan*zeros(size(imd));

r=15;   % el tamaño de la region
R=55;  % La region de busqueda máxima del dezplazamiento
%para optimizacion
[gc,gr] = gradient(imd);
%----
for y=1+r:1:size(imd,1)-r
    for x=1+r:1:size(imd,2)-r
        rx=x-r:x+r;
        ry=y-r:y+r;
        [X,Y]=meshgrid(rx,ry);
        [d,resultado,e] = track(imd,imi,X(:), Y(:),100,gc,gr);
        %[d,e]=track(X(:),Y(:),imd,imi,R); % El método de desplazamiento
        M(y,x,1)=d(1);
        M(y,x,2)=d(2);
        NM(y,x)=sqrt(d(1).^2+d(2).^2);
        E(y,x)=e;
    end
    subplot(234);
    imagesc(NM);
    colorbar;
    subplot(235);
    imagesc(E);
    colorbar;
    subplot(233);
    NMM=NM(:);
    [f,b]=hist(NMM(NMM>0),50);
    bar(b,f./sum(f),1);
    subplot(236);
    EE=E(:);
    [f,b]=hist(EE(EE>0),50);
    bar(b,f./sum(f),1);
    drawnow;
    y,
end
%%
%{
[X,Y]=meshgrid(1:1:size(imd,2),1:1:size(imd,1));

figure;
R=double(imo(:,:,1));
R=R(sub2ind(size(NM),Y(:),X(:)))/255;
G=double(imo(:,:,2));
G=G(sub2ind(size(NM),Y(:),X(:)))/255;
B=double(imo(:,:,3));
B=B(sub2ind(size(NM),Y(:),X(:)))/255;
Z=NM(sub2ind(size(NM),Y(:),X(:)));
X=X(:);
Y=Y(:);
figure;
hold on
for i=1:length(X)
    plot3(X(i),Y(i),Z(i),'.','MarkerFaceColor',[R(i) G(i) B(i)]);
end
%}


%colormap hsv
%surface(X(:),Y(:),NM(sub2ind(size(NM),Y(:),X(:))),'FaceColor','interp',...
%   'EdgeColor','none',...
%   'FaceLighting','gouraud')
%daspect([5 5 1])
%axis tight
%view(-50,30)
%camlight left

%%
MX=zeros(size(NM));
for y=1+r:1:size(imd,1)-r
    for x=1+r:1:size(imd,2)-r
        MX(y,x)=M(y,x,1);
    end
end
figure;
imagesc(MX);
save 'datos40Shi'
%%
imo=imresize(imread('DSCF9319_001.jpg'),0.4);

load('datos40Shi');
figure;
borde=60;
NM=NM(:,borde:end-borde);
imo=imo(:,borde:end-borde,:);
BB=(NM>45)|(NM<0.01);
SS=size(NM);

[y,x]=find(BB==1);
NM(sub2ind(SS,y,x))=NaN;
[X,Y]=meshgrid(1:1:size(imo,2),1:1:size(imo,1));
surface(X,Y,NM,imo,'EdgeColor','none','FaceAlpha',0.5)
figure;
mesh(NM);
%%
close all
imo=imresize(imread('DSCF9319_001.jpg'),0.4);

load('datos40Shi');
figure;
borde=60;
NM=NM(:,borde:end-borde);
imo=imo(:,borde:end-borde,:);
BB=(NM>100)|(NM<0.01);
SS=size(NM);

[y,x]=find(BB==1);
NM(sub2ind(SS,y,x))=NaN;
[X,Y]=meshgrid(1:1:size(imo,2),1:1:size(imo,1));
surface(X,Y,NM,imo,'EdgeColor','none','FaceAlpha',0.5)
figure;
mesh(NM);
figure;
    imagesc(NM);
    title('Deepness Map');
    xlabel('Width (pixels)');
    ylabel('Height (pixels)');
    grid on
    %grid minor
    colorbar;
figure;
    imagesc(E);
    colorbar;
figure;
    NMM=NM(:);
    [F,B]=hist(NMM(NMM>0),50);
    bar(B,F./sum(F),1);
    title('Disparity Distribution');
    xlabel('Norm of Distance Estimated');
    ylabel('Probability');
    grid on
figure;
    EE=E(:);
    [F,B]=hist(EE(EE>0),50);
    F=F./sum(F);
    %B=B/255;
    bar(B,F,1);
    [Fm,Fp]=max(F);
    text(B(Fp+1),Fm+(0.5e-4),'\leftarrow Expected Error','color','red');
    title('Residual Error');
    xlabel('% Residual Error from used Metric');
    ylabel('Probability');
    grid on
 
    drawnow;
```

## disparidadBruto.m

Versión empaquetada de disparidad.m como función.
Permite ejecutar:

[M,NM,E] = disparidadBruto(im1, im2, salida, escala, GUI);

y guarda resultados en salida.
Es básicamente la misma lógica que el script principal, pero modularizada.

```matlab
%% Algoritmo por fuerza bruta para realizar el mapa de disparidad
function [M,NM,E]=disparidadBruto(im1,im2,salida,e, GUI)
imo=imresize(imread(im1),0.4);
imd=single(rgb2gray(imresize(imread(im1),e)));
imi=single(rgb2gray(imresize(imread(im2),e)));
f=fspecial('gaussian',9,1.0);%1.5);
imd=conv2(imd,f,'same')./255;
imi=conv2(imi,f,'same')./255;
if(GUI==1)
    figure;
    colormap(gray);
    subplot(231);imagesc(imd);
		daspect([1 1]);
    subplot(232);imagesc(imi);
		daspect([1 1]);
end
M=zeros([size(imd) 2]);     % Contiene el vector de desplazamiento
NM=nan*zeros(size(imd));    % Contiene la norma
E=nan*zeros(size(imd));
r=15;       % el tamaño de la region
R=55;       % La region de busqueda máxima del dezplazamiento
for y=1+r:1:size(imd,1)-r
    for x=1+r:1:size(imd,2)-r
        rx=x-r:x+r;
        ry=y-r:y+r;
        [X,Y]=meshgrid(rx,ry);
        [d,e]=desplazamiento(X(:),Y(:),imd,imi,R); % El método de desplazamiento
        M(y,x,1)=d(1);
        M(y,x,2)=d(2);
        NM(y,x)=sqrt(d(1).^2+d(2).^2);
        E(y,x)=e;
    end
    if (GUI==1)
        subplot(234);
				hold off
        imagesc(NM,[]);
				daspect([1 1]);
				hold on
        colorbar;
        subplot(235);
				hold off
        imagesc(E);
				daspect([1 1]);
				hold on
        colorbar;
        subplot(233);
				hold off
        NMM=NM(:);
        hist(NMM(NMM>0),50);
				hold off
        subplot(236);
				hold on
        EE=E(:);
        hist(EE(EE>0),50);
				hold off
        drawnow;
    end
    fprintf('%0.3f\n',y/size(imd,2)*100);
end
save(salida);

```

## disparidadBatch.m

Ejecuta el proceso en lotes, usando pares de imágenes listadas en ds2006.txt.

Llama a disparidadBruto repetidamente.

Luego visualiza y genera superficies 3D y mapas de profundidad.

```matlab
%Procesamiento en lotes
clc
disp('Leyendo...');
L=leerTexto('ds2006.txt');
for i=17:2:length(L)
    [M,NM,E]=disparidadBruto(L{i},L{i+1},sprintf('2006.bruto.%d.mat',i),1,1);
    fprintf('Juegos Stereo %f0.4.\n',i/length(L)*100);
end
disp('Finalizado');
return;

%%
MX=zeros(size(NM));
for y=1+r:1:size(imd,1)-r
    for x=1+r:1:size(imd,2)-r
        MX(y,x)=M(y,x,1);
    end
end
figure;
imagesc(MX);
save 'datos40'
%%
imo=imresize(imread('DSCF9319_001.jpg'),0.4);

load('datos40');
figure;
borde=60;
NM=NM(:,borde:end-borde);
imo=imo(:,borde:end-borde,:);
BB=(NM>45)|(NM<0.01);
SS=size(NM);

[y,x]=find(BB==1);
NM(sub2ind(SS,y,x))=NaN;
[X,Y]=meshgrid(1:1:size(imo,2),1:1:size(imo,1));
surface(X,Y,NM,imo,'EdgeColor','none','FaceAlpha',0.5)
figure;

%%
close all
imo=imresize(imread('DSCF9319_001.jpg'),0.4);

load('datos40');
figure;
borde=60;
NM=NM(:,borde:end-borde);
imo=imo(:,borde:end-borde,:);
BB=(NM>=42)|(NM<0.01);
SS=size(NM);

[y,x]=find(BB==1);
NM(sub2ind(SS,y,x))=NaN;
[X,Y]=meshgrid(1:1:size(imo,2),1:1:size(imo,1));
surface(X,Y,NM,imo,'EdgeColor','none','FaceAlpha',0.5)
view(30,120)
grid on
ax = gca;
ax.XDir = 'reverse'
%grid minor
xlabel('Height (Pixels)');
xlabel('Width (Pixels)');
ylabel('Height (Pixels)');
zlabel('Deepness (Pixels)');
title('Disparity map');
figure;
mesh(NM);
figure;
    imagesc(NM);
    title('Deepness Map');
    xlabel('Width (pixels)');
    ylabel('Height (pixels)');
    grid on
    grid minor
    colorbar;
figure;
    imagesc(E);
    colorbar;
figure;
    NMM=NM(:);
    [F,B]=hist(NMM(NMM>0),50);
    bar(B,F./sum(F),1);
    title('Disparity Distribution');
    xlabel('Norm of Distance Estimated');
    ylabel('Probability');
    grid on
figure;
    EE=E(:);
    [F,B]=hist(EE(EE>0),50);
    F=F./sum(F);
    B=B/255;
    bar(B,F,1);
    [Fm,Fp]=max(F);
    text(B(Fp+1),Fm+(0.5e-4),'\leftarrow Expected Error','color','red');
    title('Residual Error ');
    xlabel('% Residual Error from used Metric');
    ylabel('Probability');
    grid on
 
    drawnow;
%%
mesh(NM);
```

## disparidadBatchShi

Procesamiento en lotes utilizando la otra versión del algoritmo de disparidad

```matlab
%Procesamiento en lotes
clc
clear all
disp('Leyendo...');
L=leerTexto('wds2006.txt');
for i=1:2:length(L)
    [M,NM,E]=disparidadShiTomasi(L{i},L{i+1},sprintf('2006.ShiTomasi.%d.mat',i),1,1);
    fprintf('Juegos Stereo %0.4f.\n',i/length(L)*100);
end
disp('Finalizado');
return;

return
%%
%{
[X,Y]=meshgrid(1:1:size(imd,2),1:1:size(imd,1));

figure;
R=double(imo(:,:,1));
R=R(sub2ind(size(NM),Y(:),X(:)))/255;
G=double(imo(:,:,2));
G=G(sub2ind(size(NM),Y(:),X(:)))/255;
B=double(imo(:,:,3));
B=B(sub2ind(size(NM),Y(:),X(:)))/255;
Z=NM(sub2ind(size(NM),Y(:),X(:)));
X=X(:);
Y=Y(:);
figure;
hold on
for i=1:length(X)
    plot3(X(i),Y(i),Z(i),'.','MarkerFaceColor',[R(i) G(i) B(i)]);
end
%}


%colormap hsv
%surface(X(:),Y(:),NM(sub2ind(size(NM),Y(:),X(:))),'FaceColor','interp',...
%   'EdgeColor','none',...
%   'FaceLighting','gouraud')
%daspect([5 5 1])
%axis tight
%view(-50,30)
%camlight left

%%
MX=zeros(size(NM));
for y=1+r:1:size(imd,1)-r
    for x=1+r:1:size(imd,2)-r
        MX(y,x)=M(y,x,1);
    end
end
figure;
imagesc(MX);
save 'datos40Shi'
%%
imo=imresize(imread('DSCF9319_001.jpg'),0.4);

load('datos40Shi');
figure;
borde=60;
NM=NM(:,borde:end-borde);
imo=imo(:,borde:end-borde,:);
BB=(NM>45)|(NM<0.01);
SS=size(NM);

[y,x]=find(BB==1);
NM(sub2ind(SS,y,x))=NaN;
[X,Y]=meshgrid(1:1:size(imo,2),1:1:size(imo,1));
surface(X,Y,NM,imo,'EdgeColor','none','FaceAlpha',0.5)
figure;
mesh(NM);
%%
close all
imo=imresize(imread('DSCF9319_001.jpg'),0.4);

load('datos40Shi');
figure;
borde=60;
NM=NM(:,borde:end-borde);
imo=imo(:,borde:end-borde,:);
BB=(NM>100)|(NM<0.01);
SS=size(NM);

[y,x]=find(BB==1);
NM(sub2ind(SS,y,x))=NaN;
[X,Y]=meshgrid(1:1:size(imo,2),1:1:size(imo,1));
surface(X,Y,NM,imo,'EdgeColor','none','FaceAlpha',0.5)
figure;
mesh(NM);
figure;
    imagesc(NM);
    title('Deepness Map');
    xlabel('Width (pixels)');
    ylabel('Height (pixels)');
    grid on
    %grid minor
    colorbar;
figure;
    imagesc(E);
    colorbar;
figure;
    NMM=NM(:);
    [F,B]=hist(NMM(NMM>0),50);
    bar(B,F./sum(F),1);
    title('Disparity Distribution');
    xlabel('Norm of Distance Estimated');
    ylabel('Probability');
    grid on
figure;
    EE=E(:);
    [F,B]=hist(EE(EE>0),50);
    F=F./sum(F);
    %B=B/255;
    bar(B,F,1);
    [Fm,Fp]=max(F);
    text(B(Fp+1),Fm+(0.5e-4),'\leftarrow Expected Error','color','red');
    title('Residual Error');
    xlabel('% Residual Error from used Metric');
    ylabel('Probability');
    grid on
 
    drawnow;
```
