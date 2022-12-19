function cost = object_function(x)
load data.mat xData yData;
y_ans = x(1) * xData.^3 + x(2) * xData.^2 + x(3) * xData + ...
       x(4) * sin(x(5)*xData) + x(6)*cos(x(7)*xData);
plot(xData, yData);
hold on
plot(xData, y_ans)
cost = sum((yData-y_ans).^2);