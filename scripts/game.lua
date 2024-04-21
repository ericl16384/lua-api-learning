function json_dumps(tbl)
    local function format(x)
        if type(x) == "table" then
            return json_dumps(x)
        elseif type(x) == "string" then
            return "\"" .. x .. "\""
        else
            return x
        end
    end

    out = "{"
    first = true
    for k, v in pairs(tbl) do
        if first then
            first = false
        else
            out = out .. ","
        end

        out = out .. format(k) .. ":" .. format(v)
    end
    out = out .. "}"
    return out
end



function Unit(x, y)
    x = x or 0
    y = y or 0

    out = {}
    out.x = x
    out.y = y
    out.owner = "player"
    return out
end


map = {}
for x=-2,2 do
    for y=-2,2 do
        map[x .. "," .. y] = "grass"
    end
end

units = {Unit(0, 0)}

print(json_dumps(units))
print(json_dumps(map))
