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
