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

function generate_tile(x, y)
    return "wall"
end

function set_tile(x, y, value)
    map[x .. "," .. y] = value
end

function get_tile(x, y)
    if map[x .. "," .. y] == nil then
        map[x .. "," .. y] = generate_tile(x, y)
    end
    return map[x .. "," .. y]
end


for x=-2,2 do
    for y=-2,2 do
        map[x .. "," .. y] = "empty"
    end
end
for x=0,4 do
    for y=0,0 do
        map[x .. "," .. y] = "empty"
    end
end
for x=4,4 do
    for y=-2,5 do
        map[x .. "," .. y] = "empty"
    end
end


units = {Unit(0, 0)}

print(json_dumps(units))
print(json_dumps(map))


