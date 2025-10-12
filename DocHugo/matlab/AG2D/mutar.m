function puntos=mutar(puntos,n)
% puntos, lista de puntos en binario
% n, la probabilidad o porcentaje de mutacion

total=size(puntos,1);
ind=fix(rand(fix(n*total),1))+1;
for i=1:n
  puntos(ind(i),:)=mutacion(puntos(ind(i),:),4);
end