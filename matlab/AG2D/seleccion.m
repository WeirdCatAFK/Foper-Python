function r=seleccion(a,b,epsilon,puntos,y)

%y=evaluacion(a,b,epsilon,puntos);

[~,pys]=sort(y,'descend');

r=pys(1:size(puntos,1)/2);
