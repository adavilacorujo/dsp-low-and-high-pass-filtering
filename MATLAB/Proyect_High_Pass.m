%% Proprietary Information:
% Elmer J. Jimenez #92263
% Andrés G.M. Dávila #93664
% Francisco A. Villagrasa #68409
% Alexander Centeno #96006
% Association: Polytechnic University of Puerto Rico, 
% EE4720-09 Digital Signal Processing (DSP) Proyect, Fall 2020
% Prof. Marvi Teixeira, PhD

clear all 
close all

%% Functions referred to in the script are found around the end of the script

%% Select Your Images for Display and Processing for Demos 1 to 2

[names, images] = get_images('..\IMAGES\');
%% Show Selected Images

% for i=1:length(images)
%     figure
%     imshow(cell2mat(images(i)));
% end

%% Two Dimensional High Pass Filters Demo 1

hlp_3 = ones(3)*(-1/9);
hlp_5 = ones(5)*(-1/25);
hlp_7 = ones(7)*(-1/49);
hlp_9 = ones(9)*(-1/81);
hlp_25 = ones(25)*(-1/625);
fltrs = {hlp_3, hlp_5, hlp_7, hlp_9, hlp_25};

%% Map to set center of each filter

filters = set_center_value(fltrs, [2,2,2,2,2]);

%% Filter each image
filtered_images = apply_filters(filters, images);

save_images(filters, images, filtered_images,names);
display_images(filters, images, filtered_images);

    

%% set_center_value: Used to set the value of each filter
% to a specific value
function fltrs = set_center_value(filters, values)
    center = containers.Map(1:2:99, 1:50);
    fltrs = {};
    for i=1:length(filters)
        filter = cell2mat(filters(i));
        [row, col] = size(filter);
        if length(values) == 1
            filter(center(row), center(col)) = values(1);
        else
            filter(center(row), center(col)) = values(i);
        end
        fltrs = [fltrs, filter];
    end
end

%% apply_filters: Used to apply each filter to each image provided
function filtered_images = apply_filters(filters, images)
    filtered_images = {};
    for i=1:length(images)
        imgs = {};
        for j=1:length(filters)
            image = cell2mat(images(i));
            filter = cell2mat(filters(j));
            imgs = [imgs, imfilter(image, filter)];
        end
        filtered_images = [filtered_images, imgs];
    end
end

%% display_images: function to display images after being filtered
function no_use = display_images(filters, images, filtered_images)
    N_filters = length(filters);
    N_images = length(images);
    sze = N_filters*N_images;
    j = 1;
    for i=1:sze             
        [row, col] = size(cell2mat(filters(j)));   
        imshow(cell2mat(filtered_images(i)));
        title(['Filter is', num2str(row), 'x',num2str(col)]);
        keyboard
        if mod(i, 5) == 0 && i ~= 1 
            j = 1;
        else
            j = j + 1; 
        end   
    end
end

%%
function no_use = save_images(filters, images, filtered_images, names)
    N_filters = length(filters);
    N_images = length(images);
    sze = N_filters*N_images;
    j = 1;
    x = 1;
    for i=1:sze             
        [row, col] = size(cell2mat(filters(j)));   
        title(['Filter is ', num2str(row), 'x',num2str(col)]);
        imwrite(cell2mat(filtered_images(i)), strcat('..\IMAGES\high_pass\', num2str(row), 'x',num2str(col), cell2mat(names(x))));
        if mod(i, 5) == 0 && i ~= 1 
            j = 1;
            x = x + 1;
        else
            j = j + 1; 
        end   
    end
end

function [names, images] = get_images(directory)
    images = {};
    names = {};
    if ~isfolder(directory)
        errorMessage = sprintf('Error: The following folder does not exist:\n%s\nPlease specify a new folder.', myFolder);
        uiwait(warndlg(errorMessage));
        directory = uigetdir(); % Ask for a new one.
        if directory == 0
             % User clicked Cancel
            return;
        end
    end
    
    files = {dir(fullfile(directory, '*.png')),dir(fullfile(directory, '*.jpg'))};
    for i=1:length(files)
        file = cell2mat(files(i));
        if length(file) > 1
            for i=1:length(file)
                fle = file(i);
                baseFileName = fle.name;
                fullFileName = fullfile(fle.folder, baseFileName);
                images = [images, imread(fullFileName)];
                names = [names, baseFileName];               
            end           
        else
            baseFileName = file.name;
            fullFileName = fullfile(file.folder, baseFileName);
            images = [images, imread(fullFileName)];
            names = [names, baseFileName];
        end       
    end
end

    
