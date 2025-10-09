function r=codInv(a,b,epsilon,n,p)
% [a,b] es el intervalo donde se está buscando la solución
% epsilon es la presición con el que se busca la solución
% nc Numero que deseamos codificar
% n la cantidad de digitos binarios necesarios para representar un numero

tam=size(n,2);
%p=2.^(tam-1:-1:0);
r=n*p';
%for i=tam:-1:1
%   r=r+n(i)*2.^(tam-i);
%end
r=a+epsilon*r;
