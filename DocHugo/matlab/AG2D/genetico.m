function Solucion=genetico(a,b,epsilon,n,soldaditos,mutacion,r,d,debug)
% a y b vectores
%
global pot1
global pot2


m(1)=fix(log2((b(1)-a(1))/epsilon)+1);
if (mod(m(1),2)==1) % La codificacion sea par
    m(1)=m(1)+1;
    pot1=2.^(m(1)-1:-1:0);
end
m(2)=fix(log2((b(2)-a(2))/epsilon)+1);
if (mod(m(2),2)==1) % La codificacion sea par
    m(2)=m(2)+1;
    pot2=2.^(m(1)-1:-1:0);
end

[puntos,ptsReal]=inicializacion(a,b,epsilon,m,soldaditos);
%puntos=inicializacion(a,b,epsilon,m,soldaditos);
solG=+inf; %  Porcentaje de parecido
solx=[0 0];  % POSICION donde lo encontro
nr=0;
Solucion=[NaN NaN NaN];
for i=1:n
    ptsy=evaluacion(a,b,epsilon,puntos,ptsReal,d);
    [sol,p]=min(ptsy);
    if(solG>sol)% Hay una mejor Solucion              &&(sum(abs(ptsReal(p,:)-solx))>0))
        solG=sol;
        solx(1)=codInv(a(1),b(1),epsilon,puntos(p,1:m(1)),pot1);
        solx(2)=codInv(a(2),b(2),epsilon,puntos(p,m(1)+1:m(1)+m(2)),pot2);
        if(debug==1)
            fprintf('Sol. Encontrada %3.1f, (%8.1f,%8.1f)\n',solG,solx(1),solx(2));
        end
        nr=1;
        Solucion=[solx(1) solx(2) solG];
    else
        nr=nr+1;
    end
    if(nr>r)
        if(debug==1)
            fprintf('Reiniciando Poblacion...\n');
        end
        [puntos,ptsReal]=inicializacion(a,b,epsilon,m,soldaditos);
        %puntos=inicializacion(a,b,epsilon,m,soldaditos);
        ptsy=evaluacion(a,b,epsilon,puntos,ptsReal,d);
        %ptsy=evaluacion(a,b,epsilon,puntos);
        nr=1;
    end
    indM=seleccion(a,b,epsilon,puntos,ptsy);
    puntos=puntos(indM,:);
    puntos=cruzamiento(puntos);
    puntos=mutar(puntos,mutacion);
    ptsReal=codInvPts(puntos,a,b,epsilon,m);
    if(debug==1)
        fprintf('=>%3.2f, (%8.1f,%8.1f,%3.5f)\n',i/n*100,solx(1),solx(2),solG);
    end
end