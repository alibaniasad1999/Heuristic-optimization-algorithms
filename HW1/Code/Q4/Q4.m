clear;
clc;
% make data for city in three groupe
city_num = 10;
city_sort = zeros(city_num^2, 3);
% counter of all possible way
counter = 0;
for i = 0:city_num % first truck
    for j = 0:city_num % second truck
        if i + j > city_num || i + j == 0 % check for availabe group of city
            continue    
        end
        counter = counter + 1;
        city_sort(counter, :) = [i, j, 10 - (i+j)];
    end
end

% delete all the same choice
city_sort = sort(city_sort, 2);
city_sort = unique(city_sort, 'row');

city_sort(1, :) = []; % delete condition with no city

% location of cities
location = [-19, 25, -40, 2 ,  21, -21, 41, -25, 33,  44 ;...
            -5 ,-40, -24, 47, -19,  35, 13, -42,  8, -44];

min_cost = inf;
best_dir_final_1 = [];
best_dir_final_2 = [];
best_dir_final_3 = [];
all_ite = 0;
for i = 1:length(city_sort)
    map = [zeros(1, city_sort(i, 1)),... firt truck
        ones(1, city_sort(i, 2)), ... second truck
        2 * ones(1, city_sort(i, 3))]; % third truck
    [cost_1, ite_num_1, best_dir_1] = Travel_calculator(map == 0, location);
    [cost_2, ite_num_2, best_dir_2] = Travel_calculator(map == 1, location);
    [cost_3, ite_num_3, best_dir_3] = Travel_calculator(map == 2, location);
    all_ite = all_ite + ite_num_1 + ite_num_2 + ite_num_3;
    if max([cost_1, cost_2, cost_3]) < min_cost
        min_cost = max([cost_1, cost_2, cost_3]);
        best_dir_final_1 = best_dir_1;
        best_dir_final_2 = best_dir_2;
        best_dir_final_3 = best_dir_3;
    end 
end

% Travel_calculator(map == 1, location)

function [min_cost, iteration_num, best_direction] ...
    = Travel_calculator(map, location)

    min_cost = inf;
    best_direction = [];
    city_count = 1;
    cities = zeros(1, sum(map));
    for i = 1:length(map)
        if map(i) == 1
            cities(city_count) = i;
            city_count = city_count +  1;
        end
    end
    city_permutations = perms(cities);
    for i = 1:length(city_permutations)
        cost = 0;
        now_location = [0; 0];
        for j = 1:length(cities)
            cost = cost +  ...
            sum((now_location - location(:, city_permutations(i, j))).^2);
            now_location = location(:, city_permutations(i, j));
        end
        if cost < min_cost
            min_cost = cost;
            best_direction = city_permutations(i, :);
        end
    end
    if min_cost == inf
        min_cost = 0;
    end
    iteration_num = factorial(sum(map));

end
