function result = denorm(var, range)
    result = var .* (range(:, 2) - range(:, 1)) + range(:, 1);
end