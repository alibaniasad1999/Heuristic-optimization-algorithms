clear;
clc;
warning off
% read map from csv
table_map = readtable('map.csv');
map = table2array(table_map);

start = [4, 4];
goal = [3, 1];
map(start(1), start(2)) = 2;
map(goal(1), goal(2)) = 2;

start_graph = 15;
end_graph = 9;



x = [0.5 4.5];
y = [0.5 4.5];

imagesc(x, y, map)

axis equal

grid on

xticks(0:5)
yticks(0:5)

axis([0, 5, 0, 5])

colormap([0 0 0; 1 1 1; 1 0 0]);

paths_table = readtable('paths.csv');
paths = table2array(paths_table);

graph_map = zeros(length(map), length(map));

counter = 0;

for i = 1:length(graph_map)
    for j = 1:length(graph_map)
    if map(i, j) == 0
        graph_map(i, j)= inf;
        continue;
    end
    graph_map(i, j) = counter;
    counter = counter+ 1;
    end
end
base_map = map;
% firt path 
for i=1:length(paths)
    [x_sol, y_sol] = find(graph_map == str2double(paths(1, i)));
    if graph_map(x_sol, y_sol) == end_graph
        break;
    end
    if graph_map(x_sol, y_sol) == start_graph
        continue;
    end
    map(x_sol, y_sol) = 3;
    colormap([0 0 0; 1 1 1; 1 0 0; 0 0 1])
    imagesc(x, y, map);
    axis equal
    grid on
    xticks(0:5)
    yticks(0:5)
    axis([0, 5, 0, 5])
    pause(0.5);
end

map = base_map; % delete path from map




