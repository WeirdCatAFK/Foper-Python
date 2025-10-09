%% Algoritmo por fuerza bruta para realizar el mapa de disparidad
clear all
close all
escala=0.4;
imo=imresize(imread('DSCF9319_001.jpg'),escala);
imd=single(rgb2gray(imresize(imread('DSCF9319_001.jpg'),escala)));
imi=single(rgb2gray(imresize(imread('DSCF9319_002.jpg'),escala)));
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

% Preparar Genetico
[tiy,tix]=size(imi);
datos.imi=imi;
datos.imd=imd;
datos.ty=tiy;
datos.tx=tix;


% -----------
r=15;   % el tamaño de la region
R=55;  % La region de busqueda máxima del dezplazamiento
for y=1+r:1:size(imd,1)-r
    for x=1+r:1:size(imd,2)-r
        rx=x-r:x+r;
        ry=y-r:y+r;
        [X,Y]=meshgrid(rx,ry);
%        [d,e]=desplazamiento(X(:),Y(:),imd,imi,R); % El método de desplazamiento
% GENETICO MODIFICACION
        datos.X=X(:);
        datos.Y=Y(:);
        datos.It=datos.imi(sub2ind(size(datos.imd),datos.Y(:),datos.X(:))); %Por optimizacion
%        sol=genetico([x-R y-R],[x+R y+R],1,10,100,0.01,5,0.6,datos);
        sol=genetico([-R -R],[+R +R],1,100,1000,0.01,5,datos,0);

        M(y,x,1)=sol(1);
        M(y,x,2)=sol(2);
        NM(y,x)=sqrt(sol(1).^2+sol(2).^2);
        E(y,x)=sol(3);
%{
        subplot(234);
        imagesc(NM);
        colorbar;
        subplot(235);
        imagesc(E);
        colorbar;
        drawnow;
        %}
    fprintf('+++++++++++++++++++++++++++++++++++++++++ Avance porcentual de la imagen (%3.6f) +++++++++++++++++++++++++++++++++++++++++\r',100*((size(imd,2)-r)*y+x)/((size(imd,1)-r)*((size(imd,2)-r))));
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
save 'datos40GA-1000'
%%
imo=imresize(imread('DSCF9319_001.jpg'),0.4);

load('datos40GA-1000');
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