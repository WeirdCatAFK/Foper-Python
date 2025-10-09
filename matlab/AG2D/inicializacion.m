function [pts,ptsr]=inicializacion(a,b,epsilon,m,n)
% [a,b] es el intervalo donde se está buscando la solución
% epsilon es la presición con el que se busca la solución
% m La cantidad de digitos binarios para representar un numero
% n la cantidad de numeros para muestrear el espacio (trabajadorsitos)

pts=zeros(n,m(1)+m(2));
%             sum(m)
ptsr(:,1)=rand(n,1)*(b(1)-a(1))+a(1); % Uno para cada componente, X
ptsr(:,2)=rand(n,1)*(b(2)-a(2))+a(2); % para y
ptsr=fix(ptsr);
for i=1:n
  DNA=[cod(a(1),b(1),epsilon,ptsr(i,1),m(1)) ...
       cod(a(2),b(2),epsilon,ptsr(i,2),m(2))];
  pts(i,:)=DNA;
end