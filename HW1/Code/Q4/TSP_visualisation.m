load('result.mat');
now_location = [0; 0];
plot([0, location(1, :)], [0, location(2, :)], 'k.', 'MarkerSize',36)
hold on
for i=1:length(best_dir_final_1)
    quiver(now_location(1),now_location(2),...
        -now_location(1) + location(1, best_dir_final_1(i)),...
        -now_location(2) + location(2, best_dir_final_1(i)), 0,...
    'r', 'linewidth', 2);
    now_location = location(:, best_dir_final_1(i));
end


now_location = [0; 0];
for i=1:length(best_dir_final_2)
    quiver(now_location(1),now_location(2),...
        -now_location(1) + location(1, best_dir_final_2(i)),...
        -now_location(2) + location(2, best_dir_final_2(i)), 0,...
        'g', 'linewidth', 2);
    now_location = location(:, best_dir_final_2(i));
end


now_location = [0; 0];
for i=1:length(best_dir_final_3)
    quiver(now_location(1),now_location(2),...
        -now_location(1) + location(1, best_dir_final_3(i)),...
        -now_location(2) + location(2, best_dir_final_3(i)), 0,...
        'b', 'linewidth', 2);
    now_location = location(:, best_dir_final_3(i));
end

print('../../Figure/Q4/best_path.png','-dpng','-r400');

