function h=rgb2gray(I)

h=rgb2hsv(I);
h=h(:,:,3);