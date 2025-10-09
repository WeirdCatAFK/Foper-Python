%{
close all
i=imread('grupoPersonas.JPG');
i=fix(rgb2gray(i)*256);

mesh(i);
colormap(gray);
figure;
for j=54:54
    ib=imextendedmax(i,j);
    imagesc(ib);
    title(sprintf('valor %d.',j));
    ginput(1);
end;

imwrite(ib,'imbinaria.bmp');
%%
ref=fix(rgb2gray(imread('carita.jpg'))*255);
ref=ref>128;
[ty,tx]=size(ref);
figure;
subplot(1,2,1);
imagesc(ref);

pi=357;
pj=750;
region=ib(pi:pi+ty-1,pj:pj+tx-1);
subplot(1,2,2);
imagesc(region);

valor=parecido(ref,region),
%}
%%
%profile on
ref=fix(rgb2gray(imread('carita.jpg'))*255);
[ty,tx]=size(ref);
ref=ref>128;
i=imread('GrupoPersonas.JPG');
ib=imread('imbinaria.bmp');
[tiy,tix]=size(ib);
datos.ref=ref;
datos.ib=ib;
datos.ty=ty;
datos.tx=tx;
%save('datos','ref','ib','ty','tx');
profile on
sol=genetico([1 1],[tix-tx-1 tiy-ty-1],1,100,10000,0.01,5,0.6,datos);
profile viewer
figure;imagesc(i);colormap(gray);
hold on
plot(sol(:,1)+datos.tx/2,sol(:,2)+datos.tx/2,'oy','markersize',10);
%profile viewer