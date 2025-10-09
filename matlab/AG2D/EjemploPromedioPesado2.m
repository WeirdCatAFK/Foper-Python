close all
x=0:0.001:6*pi;

y=sin(x)+0.3*randn(size(x)); %SENSOR con ruido

plot(y);
t=0.999;
P=zeros(size(y));
P(1)=y(1);        % CONDICION INICIAL

for i=2:length(y)
    P(i)=t*P(i-1)+(1-t)*y(i);
end

hold on
plot(P,'linewidth',3);