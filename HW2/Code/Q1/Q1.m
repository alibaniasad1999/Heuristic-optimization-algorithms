%% visualisation %%
x_1 = 0:500;
y_1 = 200 - x_1;
x_2 = 0:500;
y_2 = 500 - x_2;
f1 = figure();




patch([x_1 fliplr(x_1)], [y_1 fliplr(y_2)], 'g','FaceAlpha',.3);
hold on
plot(x_1, y_1, 'LineWidth', 2)
set(gca, 'FontSize', 16, 'FontName', 'Times New Roman');
xlabel('$x_1$', 'interpreter', 'latex', 'FontSize', 24);
ylabel('$x_2$', 'interpreter', 'latex', 'FontSize', 24);

axis([0 500 0 500])
plot(x_2, y_2, 'LineWidth', 2)

print('../../Figure/Q1/valid_x1_x2', '-depsc');


%% LP %%
x1 = optimvar('x1');
x2 = optimvar('x2');
y1 = optimvar('y1');
y2 = optimvar('y2');
prob = optimproblem('Objective',5*x1 + 10*x2 + 15*y1 + 4*y2,...
    'ObjectiveSense','min');
prob.Constraints.c1 = x1 + x2 <= 500;
prob.Constraints.c2 = y1 + y2 <= 800;
prob.Constraints.c3 = x1 + y1 == 600;
prob.Constraints.c4 = x2 + y2 == 400;
prob.Constraints.c5 = x1 >= 0;
prob.Constraints.c6 = x2 >= 0;
prob.Constraints.c7 = y1 >= 0;
prob.Constraints.c8 = y2 >= 0;

problem = prob2struct(prob);
[sol,fval,exitflag,output] = linprog(problem);
