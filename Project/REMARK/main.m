clc, clear
rng('shuffle')
format short e
options.nDim = 2;
options.nDemander = 80;
options.nSupplier = ceil(options.nDemander/4);
options.maxFrnd = ceil(options.nDemander/4);
options.constrPer = 10;
options.KsigmaD = 0.7;
options.KsigmaS = 0.2;
options.KnumS = 0.4;
options.domain = [zeros(options.nDim, 1)-65.536, zeros(options.nDim, 1)+65.536];
options.nFeval = 5000;
options.objFun = 'Foxholes';
[x, val, valHist, m] = remark(options);