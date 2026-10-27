function [val] = calculate_sum(acc_pts, func)
% Author: JINTIAN WANG , Date: 30/04/2025
% Calculate the sum of func(pt) for every pt in acc_pts and returns the value.
% Input:
% ∗ acc_pts: the list of points accepted for the calculation with the form of a (M x D) matrix,
% and each row of the matrix corresponds to each point.
% ∗ func: a function that accept a point and returns a value to be calculated.
%
% Output:
% ∗ val: sum of func(pt) for every pt in acc_pts
%
% Example use:
% >> % Calculating the x−distance of centre of mass of the positive quadrant of a
% >> % 3−dimensional sphere with radius 1
% >> pts = rand(10000, 3); % 10000 points with 4 dimensions
% >> cond_func = @(pt) (sum(pt.^2, 2) < 1); % only accepts with radius < 1
% >> acc_pts = get_accepted_points(pts, cond_func);
% >> func = @(pt) pt(1); % get the x−coordinate of the poi

val = 0;

for k = 1:size(acc_pts, 1)
    p = acc_pts(k, :);
    val = val + func(p);
end

end