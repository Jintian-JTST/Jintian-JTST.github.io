% CO65_main.m
% Author: Jintian Wang, Date: 30/04/2026
%
% Monte Carlo integration for CO65.
% This script estimates:
%   1. the volume of a unit 10-dimensional sphere
%   2. the mass, centre of mass, and moments of inertia of a toroidal section
%   3. an integral over a disk
%
% Required helper functions:
%   get_accepted_points.m
%   calculate_sum.m


%% Part 1: volume of a unit 10-dimensional sphere

n = 100000;
D = 10;

% Points inside [-1, 1]^10
pst = 2 * rand(n, D) - 1;

%apply MC
acc_pst = get_accepted_points(pst, @(p) sum(p.^2) <= 1);

vol = 2^10;
R10 = size(acc_pst, 1) / n;
vol10 = vol * R10;

% err
err10 = vol * sqrt(R10 * (1 - R10) / n);

fprintf("\nPart 1: 10D unit sphere\n");
fprintf("Estimated volume = %.6f +/- %.6f\n", vol10, err10);



%% Part 2: toroidal section
fprintf("\nPart 2: toroidal section\n");
N = 10000;

% Bounding box:
x = 1 + 3 * rand(N, 1);
y = -3 + 7 * rand(N, 1);
z = -1 + 2 * rand(N, 1);

V = 42;  
points = [x, y, z];

% MC applied
torus_func = @(p) p(3)^2 + (sqrt(p(1)^2 + p(2)^2) - 3)^2 <= 1;
acc_pts = get_accepted_points(points, torus_func); %accepted points

% CALCULATIONS
s_rho = size(acc_pts, 1);
s_rho2 = s_rho;     
% rho = 1 inside, = 0 outside

% @(p)=acc_pts      p(1)=x     p(2)=y       p(3)=z
sx = calculate_sum(acc_pts, @(p) p(1));
sy = calculate_sum(acc_pts, @(p) p(2));
sz = calculate_sum(acc_pts, @(p) p(3));

sx2 = calculate_sum(acc_pts, @(p) p(1)^2);
sy2 = calculate_sum(acc_pts, @(p) p(2)^2);
sz2 = calculate_sum(acc_pts, @(p) p(3)^2);

sIxx = calculate_sum(acc_pts, @(p) p(2)^2 + p(3)^2);
sIyy = calculate_sum(acc_pts, @(p) p(3)^2 + p(1)^2);
sIzz = calculate_sum(acc_pts, @(p) p(1)^2 + p(2)^2);

sIxx2 = calculate_sum(acc_pts, @(p) (p(2)^2 + p(3)^2)^2);
sIyy2 = calculate_sum(acc_pts, @(p) (p(3)^2 + p(1)^2)^2);
sIzz2 = calculate_sum(acc_pts, @(p) (p(1)^2 + p(2)^2)^2);

% M
M = V * s_rho / N;
M_err = V * sqrt((s_rho2 / N - (s_rho / N)^2) / N);
fprintf("Mass = %.6f +/- %.6f\n", M, M_err);

% COM
xcm = V * sx / N / M;
ycm = V * sy / N / M;
zcm = V * sz / N / M;

xcm_err = V * sqrt((sx2 / N - (sx / N)^2) / N) / M;
ycm_err = V * sqrt((sy2 / N - (sy / N)^2) / N) / M;
zcm_err = V * sqrt((sz2 / N - (sz / N)^2) / N) / M;

fprintf("Centre of mass:\n");
fprintf("  x_cm = %.6f +/- %.6f\n", xcm, xcm_err);
fprintf("  y_cm = %.6f +/- %.6f\n", ycm, ycm_err);
fprintf("  z_cm = %.6f +/- %.6f\n", zcm, zcm_err);

% Inertia
Ixx = V * sIxx / N;
Iyy = V * sIyy / N;
Izz = V * sIzz / N;

Ixx_err = V * sqrt((sIxx2 / N - (sIxx / N)^2) / N);
Iyy_err = V * sqrt((sIyy2 / N - (sIyy / N)^2) / N);
Izz_err = V * sqrt((sIzz2 / N - (sIzz / N)^2) / N);

fprintf("Moments of inertia:\n");
fprintf("  Ixx = %.6f +/- %.6f\n", Ixx, Ixx_err);
fprintf("  Iyy = %.6f +/- %.6f\n", Iyy, Iyy_err);
fprintf("  Izz = %.6f +/- %.6f\n", Izz, Izz_err);


%% Part 3: surface integral over disk

N = 100000;

% -0.5 <= x <= 0.5, -0.5 <= y <= 0.5
xy = rand(N, 2) - 0.5;

%apply MC
acc_func= @(p) p(1)^2 + p(2)^2 <= 0.25;
acc_pst = get_accepted_points(xy,acc_func);

%integral
int_func = @(p) sin(log(p(1) + p(2) + 1));
sf = calculate_sum(acc_pst,int_func);

I = sf / N;

fprintf("\nPart 3: disk integral\n");
fprintf("Integral estimate = %.6f", I);

