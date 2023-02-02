classdef supplier
    properties
        currPlace
    end
    methods
        function obj = supplier(loc)
            obj.currPlace = propty(loc);
        end
        function obj = move(obj, idealPropty, maxValue, minValue, nSupplier, KsigmaS)
            normValue = (idealPropty.value  - minValue)/(maxValue - minValue);
            qSupply = (1 - normValue)/(nSupplier + 1);
            loc = normrnd(idealPropty.loc, KsigmaS*qSupply);
            loc(loc > 1) = 1;
            loc(loc < 0) = 0;
            obj.currPlace = propty(loc);
        end
    end
end