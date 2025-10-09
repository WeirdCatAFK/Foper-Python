function salida=fnEvaluacion(X,d)
%It=d.imi(sub2ind(size(d.imd),d.Y(:),d.X(:))); 
it1=d.imd;
xd=d.X(:)+X(1);
yd=d.Y(:)+X(2);
% Validar que sea un cuadro válido
error=sum((xd<=0)|(xd>size(d.imi,2))|(yd<=0)|(yd>size(d.imi,1)));
if(error>0)
    salida=NaN;
    return;
end
% Métrica de similitud
It1=it1(sub2ind(size(it1),yd,xd));
salida=sum(abs(d.It-It1))./size(It1,1); % Métrica que se usa para medir la similitud
%salida=d;
