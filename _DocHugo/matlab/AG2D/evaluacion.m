function pts=evaluacion(a,b,epsilon,puntos,puntosR,d)
long=(size(puntos,1));
pts=zeros(long,1);
for i=1:long
  %valor=codInv(a,b,epsilon,puntos(i,:));
  if (pertenece(a,b,puntosR(i,:))==1)
     pts(i)=fnEvaluacion(puntosR(i,:),d);
  else
      pts(i)=+inf; % ASI PORQUE LA COMPAÑERA QUIERE Minimo
  end
%  fprintf('Evaluando => %3.4f\n',(i/long)*100);
end
end
function r=pertenece(a,b,v)
  r=((a(1)<=v(1))&&(v(1)<=b(1)))&&((a(2)<=v(2))&&(v(2)<=b(2)))&&((v(1)~=0)&&(v(2)~=0));
end