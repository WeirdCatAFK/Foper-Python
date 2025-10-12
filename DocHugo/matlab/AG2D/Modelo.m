function P=Modelo(alpha,y)
P=zeros(size(y));
P(1)=y(1);
for i=2:length(y)
  P(i)=(1-alpha)*P(i-1)+alpha*(y(i));
end
