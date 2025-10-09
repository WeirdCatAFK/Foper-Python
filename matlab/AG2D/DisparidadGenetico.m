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