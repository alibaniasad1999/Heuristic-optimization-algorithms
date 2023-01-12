import numpy as np
import pandas as pd
data = pd.read_csv('PSO_I10ite100000.csv', header=None)
data = data.to_numpy()
data = data.reshape(1, len(data))
data.sort()

data1 = pd.read_csv('PSO_I10ite100000.csv', header=None)
data1 = data1.to_numpy()
data1 = data1.reshape(1, len(data1))
data1.sort()

print(data1[0][0], '&', data[0][0], '& \\lr{$1^{th}$(Best)}',  '& \multirow{7}{*}{1e3}  \\\\')
print(data1[0][6], '&', data[0][6], '& \\lr{$7^{th}$}',  '& \\\\')
print(data1[0][12], '&', data[0][12], '& \\lr{$13^{th}$(Median)}',  '& \\\\')
print(data1[0][18], '&', data[0][18], '& \\lr{$19^{th}$}',  '& \\\\')
print(data1[0][24], '&', data[0][24], '& \\lr{$25^{th}$(Worst)}',  '& \\\\')
print(data1.mean(), '&', data.mean(), '& \\lr{Mean}',  '& \\\\')
print(data1.std(), '&', data.std(), '& \\lr{Std}',  '& \\\\ \\hline')


# data = pd.read_csv('sol50func1ite10000.csv', header=None)
# data = data.to_numpy()
# data = data.reshape(1, len(data))
# data.sort()

# data1 = pd.read_csv('sol50func2ite10000.csv', header=None)
# data1 = data1.to_numpy()
# data1 = data1.reshape(1, len(data1))
# data1.sort()

# print(data1[0][0], '&', data[0][0], '& \\lr{$1^{th}$(Best)}',  '& \multirow{7}{*}{1e4}  \\\\')
# print(data1[0][6], '&', data[0][6], '& \\lr{$7^{th}$}',  '& \\\\')
# print(data1[0][12], '&', data[0][12], '& \\lr{$13^{th}$(Median)}',  '& \\\\')
# print(data1[0][18], '&', data[0][18], '& \\lr{$19^{th}$}',  '& \\\\')
# print(data1[0][24], '&', data[0][24], '& \\lr{$25^{th}$(Worst)}',  '& \\\\')
# print(data1.mean(), '&', data.mean(), '& \\lr{Mean}',  '& \\\\')
# print(data1.std(), '&', data.std(), '& \\lr{Std}',  '& \\\\ \\hline')

# data = pd.read_csv('sol50func1ite100000.csv', header=None)
# data = data.to_numpy()
# data = data.reshape(1, len(data))
# data.sort()

# data1 = pd.read_csv('sol50func2ite100000.csv', header=None)
# data1 = data1.to_numpy()
# data1 = data1.reshape(1, len(data1))
# data1.sort()

# print(data1[0][0], '&', data[0][0], '& \\lr{$1^{th}$(Best)}',  '& \multirow{7}{*}{1e4}  \\\\')
# print(data1[0][6], '&', data[0][6], '& \\lr{$7^{th}$}',  '& \\\\')
# print(data1[0][12], '&', data[0][12], '& \\lr{$13^{th}$(Median)}',  '& \\\\')
# print(data1[0][18], '&', data[0][18], '& \\lr{$19^{th}$}',  '& \\\\')
# print(data1[0][24], '&', data[0][24], '& \\lr{$25^{th}$(Worst)}',  '& \\\\')
# print(data1.mean(), '&', data.mean(), '& \\lr{Mean}',  '& \\\\')
# print(data1.std(), '&', data.std(), '& \\lr{Std}',  '& \\\\ \\hline')

