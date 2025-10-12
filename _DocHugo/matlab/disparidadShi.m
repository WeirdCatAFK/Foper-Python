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