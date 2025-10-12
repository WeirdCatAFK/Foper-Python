%%
close all
x=0:0.001:(2*pi)*4;
y=1+sin(x)+0.2*randn(size(x));

%y=sin(x)+0.3*cos(16*x)+0.2*randn(size(x));

%subplot(2,1,1);
plot(y);

save('datos','y');
p=0.0001;
sol=genetico(0.1,0.9,p,100,1000,0.1,5);

ye=Modelo(sol,y);
hold on
plot(ye);
return
%%

Y=zeros(100,length(y));
R=zeros(100,length(y));
for i=1:100
   fprintf('Anidamiento %d.\n',i);
  
   sol=genetico(p,1-p,p,40,10,0.1,20);
   ye=filtro(y,sol);
   Y(i,:)=ye;
   R(i,:)=y-ye;
   y=ye;
   
   save('datos','y');
   subplot(2,1,1);
   hold on;plot(y,'r');
   subplot(2,1,2);
   plot(R(i,:));drawnow;
end
