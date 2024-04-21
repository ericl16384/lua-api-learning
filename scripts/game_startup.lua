units = {} -- array

function Unit(x, y)
    x = x or 0
    y = y or 0

    out = {}
    out.x = x
    out.y = y
    return out
end

-- append player
units[#units] = Unit(0, 0)

print(units)