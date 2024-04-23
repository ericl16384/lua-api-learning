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
known_map = {}

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

function explore_tile(x, y)
    known_map[x .. "," .. y] = get_tile(x, y)
end


for x=-1,1 do
    for y=-1,1 do
        set_tile(x, y, "empty")
    end
end
for x=0,4 do
    for y=0,0 do
        set_tile(x, y, "empty")
    end
end
for x=4,4 do
    for y=-2,5 do
        set_tile(x, y, "empty")
    end
end
for x=-6,5 do
    for y=4,4 do
        set_tile(x, y, "empty")
    end
end
for x=-4,-3 do
    for y=-2,3 do
        set_tile(x, y, "empty")
    end
end
for x=-10,-5 do
    for y=-1,-1 do
        set_tile(x, y, "empty")
    end
end
for x=-10,-10 do
    for y=-1,10 do
        set_tile(x, y, "empty")
    end
end
for x=-10,10 do
    for y=10,10 do
        set_tile(x, y, "empty")
    end
end

set_tile(10, 10, "goal")
explore_tile(10, 10)



units = {Unit(0, 0)}

explore_tile(0, 0)

-- print(json_dumps(units))
-- print(json_dumps(map))



function move(unit, x, y)
    explore_tile(x, y)
    if get_tile(x, y) == "empty" then
        unit.x = x
        unit.y = y
        return true
    end
    return false
end

function move_up()
    out = move(units[1], units[1].x, units[1].y+1)
    print("move_up")
    turn_end()
    return out
end
function move_left()
    out = move(units[1], units[1].x-1, units[1].y)
    print("move_left")
    turn_end()
    return out
end
function move_down()
    out = move(units[1], units[1].x, units[1].y-1)
    print("move_left")
    turn_end()
    return out
end
function move_right()
    out = move(units[1], units[1].x+1, units[1].y)
    print("move_right")
    turn_end()
    return out
end


-- co = coroutine.create(function()
--     for i=1,10 do
--         print("co", i)
--         coroutine.yield(i)
--     end
-- end)

INTERFACE_FUNCTIONS = {"move_up", "move_left", "move_down", "move_right"}



fog_of_war = true
