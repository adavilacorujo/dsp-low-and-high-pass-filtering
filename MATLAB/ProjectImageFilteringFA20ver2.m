%% Basic Two Dimensional Filtering Demos
% Marvi Teixeira 

clear all 
close all

%% Select Your Images for Display and Processing for Demos 1 to 2

% I_0=imread('..\IMAGES\moon.tif');  
I_1=imread('..\IMAGES\mri_data\yes\Y14.jpg'); 
I_2=imread('..\IMAGES\brainMRI_2.png'); 
I_3=imread('..\IMAGES\mri-brain-coronal-view-magnetic-3.jpg'); 
I_4=imread('..\IMAGES\ankle_1.jpg');

%% Show Selected Image
%figure 
%imshow(I)


%% Two Dimensional Low Pass Filter Demo 1

% % Select Filter
 hlp = [1/9  1/9  1/9; 1/9   1/9   1/9  ;1/9  1/9  1/9];
% hlp=[1/16 1/16 1/16 1/16 ; 1/16 1/16  1/16  1/16; 1/16 1/16 1/16 1/16 ; 1/16 1/16  1/16  1/16  ];
 hlp=[1/25 1/25 1/25 1/25 1/25; 1/25 1/25  1/25  1/25  1/25; 1/25 1/25 1/25 1/25 1/25; 1/25 1/25 1/25 1/25 1/25; 1/25 1/25 1/25 1/25 1/25];
 hlp = ones(9)*(1/81);
 hlp = ones(11)*(1/121);
  hlp = ones(25)*(1/(25*25));

% % Display Filtered Image
% figure
% imshow(imfilter(I,hlp))
% 
% % Display Frequency Response of Selected Filter
figure
title('Frequency Response: 3x3 Filter')
freqz2(hlp)

%% Two Dimensional High Pass Filter Demo 2

% % Select Filter

% hhp=[-1/9  -1/9  -1/9; -1/9   2   -1/9  ; -1/9  -1/9  -1/9];
% hhp=[-1/25 -1/25 -1/25 -1/25 -1/25; -1/25 -1/25  1.6  -1/25 -1/25; -1/25 -1/25 -1/25 -1/25 -1/25];
% hhp=[-1/25 -1/25 -1/25 -1/25 -1/25; -1/25  -1/25  -1/25  -1/25  -1/25; -1/25 -1/25  2 -1/25 -1/25;  -1/25  -1/25  -1/25  -1/25  -1/25; -1/25 -1/25 -1/25 -1/25 -1/25];

% hhp=ones(9)*(-1/81);
% hhp(5,5) = 2;
% % 
% % Display Filtered Image
% filtered_image = imfilter(I,hhp);


images = apply_filters(hlp, {I_1, I_2, I_3, I_4});
for i=1:length(images)
    figure
    image = cell2mat(images(i));
    imshow(image);
%     imwrite('image', '..\IMAGES\filtered_' +i + '.jpg');
end



% 
% % Display Frequency Response of Selected Filter
% figure
% freqz2(hhp)

function imgs = apply_filters(filter, images)
    imgs = {};
    len = length(images);
    len
    for i=1:len
        image = cell2mat(images(i));
        imgs = [imgs, imfilter(image, filter)];
    end
end



 
