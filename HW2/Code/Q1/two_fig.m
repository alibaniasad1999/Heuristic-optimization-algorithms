x1 = 0:1000;
y1 = 600 - x1;
plot(x1, y1, 'LineWidth', 2)
set(gca, 'FontSize', 16, 'FontName', 'Times New Roman');
xlabel('$x_1$', 'interpreter', 'latex', 'FontSize', 24);
ylabel('$y_1$', 'interpreter', 'latex', 'FontSize', 24);
x1_ans = 0:600;
y1_ans = 200 + 200 / 3 - 1 / 3 *  x1_ans;
hold on
plot(ones(1, length(x1)) * 500, x1, 'LineWidth', 2)
plot(x1, ones(1, length(x1)) * 800, 'LineWidth', 2)
axis([0, 600, 0 1000])
plot(x1_ans, y1_ans, 'LineWidth', 2);
legend('desired book', 'T city constrain', 'S city constrain', ...
    'cost function');
hold off

print('../../Figure/Q1/S_city', '-depsc');



x2 = 0:400;
y2 = 400 - x2;
plot(x2, y2, 'LineWidth', 2)
hold on
x2_ans = 0:400;
y2_ans = 400 - 2.5 *  x2_ans;



plot(ones(1, length(x1)) * 500, x1, 'LineWidth', 2)

plot(x1, ones(1, length(x1)) * 800, 'LineWidth', 2)

axis([0, 600, 0 1000])
set(gca, 'FontSize', 16, 'FontName', 'Times New Roman');
xlabel('$x_2$', 'interpreter', 'latex', 'FontSize', 24);
ylabel('$y_2$', 'interpreter', 'latex', 'FontSize', 24);
plot(x2_ans, y2_ans, 'LineWidth', 2);

legend('desired book', 'T city constrain', 'S city constrain', ...
    'cost function');

print('../../Figure/Q1/K_city', '-depsc');



