%% MATLAB GA %%
[ga_ans, cost] = ga(@object_function, 7, [], [], [], [],...
    zeros(1, 7), 10*ones(1, 7)); % with 0:10 bound
% global counter
counter = 0;



function cost = object_function(x)
% global counter
% counter = counter + 1;
load data.mat xData yData;
y_ans = x(1) * xData.^3 + x(2) * xData.^2 + x(3) * xData + ...
       x(4) * sin(x(5)*xData) + x(6)*cos(x(7)*xData);
plot(xData, yData);
hold on
plot(xData, y_ans)
% fprintf('%d\n', counter)
cost = sum((yData-y_ans).^2);
end