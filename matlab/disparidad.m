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

