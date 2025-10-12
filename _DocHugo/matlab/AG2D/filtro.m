function Y=filtro(X,rho)

Y=zeros(size(X));
Y(1)=X(1);
for i=2:length(Y)
  Y(i)=(1-rho)*Y(i-1)+rho*(X(i));
end
