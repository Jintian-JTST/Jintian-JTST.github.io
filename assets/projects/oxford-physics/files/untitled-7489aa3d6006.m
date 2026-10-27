function [image_out] = wavy_image(image_in)
    Y = size(image_in, 1);
    X = size(image_in, 2);
    theta = 5;
    A = 50;  % Set the Amplitude
    k = 13; % Set the frequency 
    max_shift = 2*A; % CHANGED for new wavy_image (allow for 2A extra pixels)
    image_out = zeros(Y, X+max_shift, 3);
    for y=1:Y
        %% modify these lines for this wavy_image function

        local_shift = round(A * sin(k * (y / Y) * 2 * pi));  % integer shift, offset so >=0
        local_x = 1:X;

        local_x = local_x + local_shift;
        local_x = local_x(local_x > 0 & local_x <= X + max_shift); % Ensure local_x is within bounds
        image_out(y, local_x, :) = image_in(y, :, :);
    end
end


% CO01 - Exercise 2 - Wavy Image 

% Load the image
MyImage = imread('Hubble.jpg');

% Normalise the colours
MyImage = double(MyImage)/255;

% Call the Wavy_image function with output name MyNewImage
[MyNewImage] = wavy_image(MyImage);

% Display the new image
image(MyNewImage);