classdef demander
    properties
        currPlace, frnd, purchPower, nextPlace, bestPlace
    end
    methods
        function obj = demander(loc, objFun, domain)
            obj.currPlace = propty(loc, objFun, domain);
            obj.purchPower = rand;
            obj.bestPlace = obj.currPlace;
            obj.frnd = [];
        end
        function obj = move(obj)
            obj.currPlace = obj.nextPlace;
            if obj.currPlace.value > obj.bestPlace.value
                obj.bestPlace = obj.currPlace;
            end
        end
        function obj = comm(obj, frnd, objFun, domain, KsigmaD)
            recommPropty = [obj.bestPlace, [frnd.bestPlace]];
            recommProptyValue = [recommPropty.value];
            [~, maxIdx] = max(recommProptyValue);
            recommPropty = recommPropty(maxIdx(1));
            nextPlaceMean = recommPropty.loc;
            nextPlaceStd = KsigmaD * abs(recommPropty.price) * sqrt(-2*log(obj.purchPower));
            loc = normrnd(nextPlaceMean, nextPlaceStd);
            loc(loc > 1) = 1;
            loc(loc < 0) = 0;
            obj.nextPlace = propty(loc, objFun, domain);
        end
    end
end