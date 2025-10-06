function [v,e]=desplazamiento(x,y,it,it1,w)
It=it(sub2ind(size(it),y,x));
minimo=inf;
v=zeros(2,1);
ne=size(x,1);
for xx=-w:w
    for yy=-w:w 
        xd=x+xx;
        yd=y+yy;
        error=sum((xd<=0)|(yd<=0)|(xd>size(it,2))|(yd>size(it,1)));
        if(error>0)
            continue;
        end
        It1=it1(sub2ind(size(it1),yd,xd));
        d=sum(abs(It-It1))/ne; % Métrica que se usa para medir la similitud
        if(d<minimo)
				    v(1)=xx;
						v(2)=yy;
            minimo=d;
        end
    end
end
e=minimo;
