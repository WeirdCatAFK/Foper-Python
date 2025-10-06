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
