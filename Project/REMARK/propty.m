classdef propty
    properties
        loc, value, price, demand, supply
    end
    methods
        function obj = propty(loc, varargin)
            obj.loc = loc;
            if nargin > 1
               obj.value = feval(varargin{1}, denorm(loc, varargin{2}));
            end
        end
    end
end

