function [accepted_pts] = get_accepted_points(pts, cond_func)
% Author: JINTIAN WANG , Date: 30/04/2026
% Returns the points from pts that returns True in cond_func.
% Input:
% ∗ pts: (N x D) matrix that contains N points with D dimension
% ∗ cond_func: a function that accepts a point as a D−dimensional vector and returns true
% if a certain condition is fulfilled and false otherwise (see hint).
%
% Output:
% ∗ accepted_pts: (M x D) that only returns D−dimensional points that fulfills the conditions
% by the cond_func function
%
% Example use:
% >> pts = rand(10000, 4); % 10000 points with 4 dimensions
% >> cond_func = @(pt) (sum(pt.^2, 2) < 1); % only accepts with radius < 1
% >> acc_pts = get_accepted_points(pts, cond_func);

n = size(pts, 1);
keep = false(n, 1);

for k = 1:n
    p = pts(k, :);
    keep(k) = cond_func(p);
end

accepted_pts = pts(keep, :);

end