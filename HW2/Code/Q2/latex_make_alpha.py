import numpy as np
import pandas as pd
data = pd.read_csv('sol30func1ite10000alpha=0.05.csv', header=None)
data = data.to_numpy()
data = data.reshape(1, len(data))
data.sort()

data1 = pd.read_csv('sol30func1ite10000alpha=0.1.csv', header=None)
data1 = data1.to_numpy()
data1 = data1.reshape(1, len(data1))
data1.sort()

data2 = pd.read_csv('sol30func1ite10000alpha=0.2.csv', header=None)
data2 = data2.to_numpy()
data2 = data2.reshape(1, len(data2))
data2.sort()

data3 = pd.read_csv('sol30func1ite10000alpha=0.3.csv', header=None)
data3 = data3.to_numpy()
data3 = data3.reshape(1, len(data3))
data3.sort()

print("{0:.3f}".format(data3[0][0]), '&', "{0:.3f}".format(data2[0][0]), '&', "{0:.3f}".format(data1[0][0]), '&', "{0:.3f}".format(data[0][0]), '& \\lr{$1^{th}$(Best)}',  '  \\\\')
print("{0:.3f}".format(data3[0][6]), '&', "{0:.3f}".format(data2[0][6]), '&', "{0:.3f}".format(data1[0][6]), '&', "{0:.3f}".format(data[0][6]), '& \\lr{$7^{th}$}',  '\\\\')
print("{0:.3f}".format(data3[0][12]), '&', "{0:.3f}".format(data2[0][12]), '&', "{0:.3f}".format(data1[0][12]), '&', "{0:.3f}".format(data[0][12]), '& \\lr{$13^{th}$(Median)}',  '\\\\')
print("{0:.3f}".format(data3[0][18]), '&', "{0:.3f}".format(data2[0][18]), '&', "{0:.3f}".format(data1[0][18]), '&', "{0:.3f}".format(data[0][18]), '& \\lr{$19^{th}$}',  ' \\\\')
print("{0:.3f}".format(data3[0][24]), '&', "{0:.3f}".format(data2[0][24]), '&', "{0:.3f}".format(data1[0][24]), '&', "{0:.3f}".format(data[0][24]), '& \\lr{$25^{th}$(Worst)}',  ' \\\\')
print("{0:.3f}".format(data3.mean()), '&', "{0:.3f}".format(data2.mean()), '&', "{0:.3f}".format(data1.mean()), '&', "{0:.3f}".format(data.mean()), '& \\lr{Mean}',  ' \\\\')
print("{0:.3f}".format(data3.std()), '&', "{0:.3f}".format(data2.std()), '&', "{0:.3f}".format(data1.std()), '&', "{0:.3f}".format(data.std()), '& \\lr{Std}',  ' \\\\ \\hline')


