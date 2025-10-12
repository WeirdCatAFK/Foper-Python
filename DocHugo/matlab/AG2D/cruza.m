function [v1,v2]=cruza(a,b)

n=fix(max(size(a)));
v1=zeros(size(a));
v2=zeros(size(a));
for i=1:n
  if(mod(i,2)==0)
      v1(i)=a(i);
      v2(i)=b(i);
  else
      v1(i)=b(i);
      v2(i)=a(i);
  end
end