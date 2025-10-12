%y=(cputime-fix(cputime))*100000;
%k=primoSiguiente(1000000);
%a=primoSiguiente(900000);
gen=crearGenerador((cputime-fix(cputime))*100000,...
                   primoSiguiente(1000000),...
                   primoSiguiente(900000));
%% Inicialización del Ejemplo 1
close all
a=5;
b=8;
h=25;
AC=(b-a)*h;
x=0:0.1:10;
y=2.5*x+3;
subplot(1,2,1);
plot(x,y,'b')
%% Integración por montecarlo V 1
abajo=0;
k=100000;
AH=[];
for i=1:k
  gen= sigAzar(gen);
  x=(b-a)*gen.xn+a;
  gen= sigAzar(gen);
  y=h*gen.xn;
  subplot(1,2,1);
  hold on
  
  if(y<2.5*x+3)
      abajo=abajo+1;
      plot(x,y,'.k');
  else
      plot(x,y,'.r');
  end
  subplot(1,2,2);
  A=abajo/i*AC;
  AH=[AH;A];
  plot(AH);
  title(sprintf('Area Aprox %3.4f',A));
  drawnow;
  pause(0.01);
end
A=abajo/k*AC;
%% Grafica de 3D para calcular el area por Monte Carlo V1
figure;
hold on
axis on
grid on
for x=0:0.1:2*pi
    for y=0:0.1:2*pi
        z=sin(x)*cos(y)+1;
        plot3(x,y,z,'.b','markersize',1);
    end
end
%% Monte Carlo V1
%limites para integrar
limx=[3,5];
limy=[3,5];
limz=3;
% Variable para saber la proporcion
abajo=0;
% Cantidad de puntitos
k=100000;
% Volumen del cubito
vC=(limx(2)-limx(1))*(limy(2)-limy(1))*limz;
hold on
for i=1:k
  % Generamos puntitos
  gen= sigAzar(gen);
  x=gen.xn; 
  gen= sigAzar(gen);
  y=gen.xn;
  gen= sigAzar(gen);
  z=gen.xn;
  % Normalizarlos
  x=(limx(2)-limx(1))*x+limx(1);
  y=(limy(2)-limy(1))*y+limy(1);
  z=(limz)*z;
  % Checar
  %z=sin(x)*cos(y)+1;
  if(z<(sin(x)*cos(y)+1))% funcion
      abajo=abajo+1;
      plot3(x,y,z,'.r');
  else
      plot3(x,y,z,'.k');
  end
  
  ev=vC*(abajo/i);
  title(sprintf('volumen aproximado %3.3f',ev));
  drawnow;
end
%% Inicialización del Ejemplo 1
close all
a=5;
b=8;
h=25;
AC=(b-a)*h;
x=0:0.1:10;
y=2.5*x+3;
subplot(1,2,1);
plot(x,y,'b')

% Integración por montecarlo V 2
s=0;
k=100000;
AH=[];
for i=1:k
  gen= sigAzar(gen);
  x=(b-a)*gen.xn+a;
  subplot(1,2,1);
  hold on
  y=2.5*x+3;
  s=s+y;
  
  plot([x; x],[0; y],'k');

  subplot(1,2,2);
  A=s/i;
  AH=[AH;A];
  plot(AH);
  title(sprintf('Area Aprox %3.4f',A));
  drawnow;
  pause(0.01);
end
%% Grafica de 3D para calcular el area por Monte Carlo V1
figure;
hold on
axis on
grid on
for x=0:0.1:2*pi
    for y=0:0.1:2*pi
        z=sin(x)*cos(y)+1;
        plot3(x,y,z,'.b','markersize',1);
    end
end
%% Monte Carlo V2
%limites para integrar
limx=[3,5];
limy=[3,5];
limz=3;
% Variable para saber la proporcion
s=0;
% Cantidad de puntitos
k=100000;
hold on
for i=1:k
  % Generamos puntitos
  gen= sigAzar(gen);
  x=gen.xn; 
  gen= sigAzar(gen);
  y=gen.xn;
  % Normalizarlos
  x=(limx(2)-limx(1))*x+limx(1);
  y=(limy(2)-limy(1))*y+limy(1);
  % Checar
  z=sin(x)*cos(y)+1;
  plot3([x;x],[y;y],[0;z],'r');
  s=s+z;
  ev=s/i;
  title(sprintf('volumen aproximado %3.3f',ev));
  drawnow;
end
