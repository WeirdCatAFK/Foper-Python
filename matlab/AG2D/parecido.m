function por=parecido(Ir,Ic)
RR=size(Ir,1)*size(Ir,2);
R=Ir==Ic;
por=sum(R(:))/RR;
%R=xor(Ir,Ic);
%por=1-sum(R(:))/RR;