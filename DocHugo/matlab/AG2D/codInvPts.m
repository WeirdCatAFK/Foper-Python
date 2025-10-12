function pts=codInvPts(puntos,a,b,epsilon,m)
global pot1
global pot2
pts=zeros(size(puntos,1),2);
X=puntos(:,1:m(1));                 %OPT
Y=puntos(:,m(1)+1:m(1)+m(2));       %OPT
for i=1:size(puntos,1)
    pts(i,1)=codInv(a(1),b(1),epsilon,X(i,:),pot1);
    pts(i,2)=codInv(a(2),b(2),epsilon,Y(i,:),pot2);
end