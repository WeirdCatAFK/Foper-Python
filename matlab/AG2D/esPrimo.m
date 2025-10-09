function r= esPrimo( n)
r=1;
mitad=fix(n/2);
for i=2:mitad
    if (mod(n,i)==0)
        r=0;
        return;
    end
end
end

