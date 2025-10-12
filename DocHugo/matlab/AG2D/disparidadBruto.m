pkg load image
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
    subplot(234);
    imagesc(NM);
    colorbar;
    subplot(235);
    imagesc(E);
    colorbar;
    subplot(233);
    NMM=NM(:);
    hist(NMM(NMM>0),50);
    subplot(236);
    EE=E(:);
    hist(EE(EE>0),50);
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
save "datosEjemplo"

%% Dibujar el mapa de disparidad
imo=imresize(imread('DSCF9319_001.jpg'),0.4);

load("datosEjemplo");
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
