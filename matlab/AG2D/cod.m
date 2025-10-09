function r=cod(a,b,epsilon,nc,n)
% [a,b] es el intervalo donde se está buscando la solución
% epsilon es la presición con el que se busca la solución
% nc Numero que deseamos codificar
% n la cantidad de digitos binarios necesarios para representar un numero

r=zeros(1,n);
num=round((nc-a)/epsilon);
for i=n:-1:1
    r(i)=mod(num,2);
    num=fix(num./2);
end