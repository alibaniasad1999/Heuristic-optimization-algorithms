classdef market
    properties
        objFun, nDim, domain, dmd, spl, maxFrnd, charLen, constrPer, KsigmaD, KsigmaS, KnumS
    end
    methods
        function obj = market(objFun, domain, nDemander, maxFrnd, nDim, nSupplier, constrPer, KsigmaD, KsigmaS, KnumS)
            obj.KnumS = KnumS;
            obj.KsigmaD = KsigmaD;
            obj.KsigmaS = KsigmaS;
            obj.charLen = sqrt(nDim);
            obj.objFun = objFun;
            obj.nDim = nDim;
            obj.domain = domain;
            obj.maxFrnd = maxFrnd;
            obj.constrPer = constrPer;
            for ii = 1:nDemander
                obj.dmd = [obj.dmd, demander(rand(obj.nDim, 1), obj.objFun, obj.domain)];
            end
            for ii = 1:nSupplier
                obj.spl = [obj.spl, supplier(rand(obj.nDim, 1))];
            end
            obj = obj.makeFrnd;
        end
        function obj = makeFrnd(obj)
            candidate = 1:length(obj.dmd);
            while ~isempty(candidate)
                if length(candidate) < obj.maxFrnd
                    selected = 1:length(candidate);
                else
                    selected = randperm(length(candidate), obj.maxFrnd);
                end
                for ii = 1:length(selected)
                	obj.dmd(candidate(selected(ii))).frnd = candidate(selected([1:(ii - 1), (ii + 1):length(selected)]))';
                end
            candidate(selected) = [];
            end
        end
        function obj = demandEval(obj)
            occupiedPropty = [obj.dmd.currPlace];
            occupiedPropty = [occupiedPropty.loc];
            for ii = 1:length(obj.dmd)
                obj.dmd(ii).currPlace.demand = (1/obj.charLen/length(obj.dmd)) * sum(obj.charLen - sqrt(sum((repmat(obj.dmd(ii).currPlace.loc, 1, length(obj.dmd)) - occupiedPropty) .^ 2)));
                obj.dmd(ii).bestPlace.demand = (1/obj.charLen/length(obj.dmd)) * sum(obj.charLen - sqrt(sum((repmat(obj.dmd(ii).bestPlace.loc, 1, length(obj.dmd)) - occupiedPropty) .^ 2)));
            end
        end
        function obj = supplyEval(obj)
            supplierPlace = [obj.spl.currPlace];
            supplierPlace = [supplierPlace.loc];
            for ii = 1:length(obj.dmd)
                obj.dmd(ii).currPlace.supply = (1/obj.charLen/length(obj.spl)) * sum(obj.charLen - sqrt(sum((repmat(obj.dmd(ii).currPlace.loc, 1, length(obj.spl)) - supplierPlace) .^ 2)));
                obj.dmd(ii).bestPlace.supply = (1/obj.charLen/length(obj.spl)) * sum(obj.charLen - sqrt(sum((repmat(obj.dmd(ii).bestPlace.loc, 1, length(obj.spl)) - supplierPlace) .^ 2)));
            end
        end
        function obj = priceEval(obj)
            obj = obj.demandEval;
            obj = obj.supplyEval;
            for ii = 1:length(obj.dmd)
                obj.dmd(ii).currPlace.price = obj.dmd(ii).currPlace.demand - obj.dmd(ii).currPlace.supply;
                obj.dmd(ii).bestPlace.price = obj.dmd(ii).bestPlace.demand - obj.dmd(ii).bestPlace.supply;
            end
        end
        function obj = demanderUpdate(obj)
            for ii = 1:length(obj.dmd)
                obj.dmd(ii) = obj.dmd(ii).comm(obj.dmd(obj.dmd(ii).frnd), obj.objFun, obj.domain, obj.KsigmaD);
            end
            for ii = 1:length(obj.dmd)
                obj.dmd(ii) = obj.dmd(ii).move;
            end
        end
        function obj = supplierUpdate(obj)
            nSupplier = ceil(obj.KnumS*length(obj.spl));
            selected = randi(length(obj.spl), 1, nSupplier);
            for ii = 1:length(selected)
                dmdMemo = [[obj.dmd.bestPlace], [obj.dmd.currPlace]];
                maxValue = max([dmdMemo.value]);
                minValue = min([dmdMemo.value]);
                [~, maxPriceIdx] = max([dmdMemo.price]);
                obj.spl(selected(ii)) = obj.spl(selected(ii)).move(dmdMemo(maxPriceIdx(1)), maxValue, minValue, nSupplier, obj.KsigmaS);
            end
        end
    end
end