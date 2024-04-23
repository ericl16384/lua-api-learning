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

-- function xy_table_to_key

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


-- for x=-1,1 do
--     for y=-1,1 do
--         set_tile(x, y, "empty")
--     end
-- end
-- for x=0,4 do
--     for y=0,0 do
--         set_tile(x, y, "empty")
--     end
-- end
-- for x=4,4 do
--     for y=-2,5 do
--         set_tile(x, y, "empty")
--     end
-- end
-- for x=-6,5 do
--     for y=4,4 do
--         set_tile(x, y, "empty")
--     end
-- end
-- for x=-4,-3 do
--     for y=-2,3 do
--         set_tile(x, y, "empty")
--     end
-- end
-- for x=-10,-5 do
--     for y=-1,-1 do
--         set_tile(x, y, "empty")
--     end
-- end
-- for x=-10,-10 do
--     for y=-1,10 do
--         set_tile(x, y, "empty")
--     end
-- end
-- for x=-10,10 do
--     for y=10,10 do
--         set_tile(x, y, "empty")
--     end
-- end

function make_maze(width, height)
    local function Node(x, y, parent)
        out = {}
        out.x = x
        out.y = y
        out.parent = parent
        return out
    end

    local function get_adjacents(node, distance)
        return {
            Node(node.x + distance, node.y),
            Node(node.x, node.y + distance),
            Node(node.x - distance, node.y),
            Node(node.x, node.y - distance)
        }
    end

    head = Node(0, 0)
    current = head

    closed_nodes = {} -- store x,y in keys
    hallways = {}

    closed_nodes[current.x .. "," .. current.y] = true

    for asdf=1,1000 do
        for i,node in ipairs(get_adjacents(current, 2)) do
            -- print(v.x)
            -- print(v.y)
            -- print("empty")
            -- set_tile(node.x, node.y, "empty")

            if closed_nodes[node.x .. "," .. node.y] then
            elseif node.x > width then
            elseif -node.x > width then
            elseif node.y > height then
            elseif -node.y > height then
            else
                x1 = current.x
                y1 = current.y
                x2 = node.x
                y2 = node.y
                if x1 > x2 then
                    x1, x2 = x2, x1
                end
                if y1 > y2 then
                    y1, y2 = y2, y1
                end
                table.insert(hallways, {x1, y1, x2, y2})

                current = Node(node.x, node.y, current)
                closed_nodes[node.x .. "," .. node.y] = true
                break
            end
        end

        for i,h in ipairs(hallways) do
            for x=h[1],h[3] do
                for y=h[2],h[4] do
                    set_tile(x, y, "empty")
                end
            end
        end
    end
end

make_maze(5, 5)




units = {Unit(0, 0)}

set_tile(0, 0, "empty")
explore_tile(0, 0)

set_tile(10, 10, "goal")
explore_tile(10, 10)

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
    out = move(units[1], units[1].x, units[1].y-1)--units[1].y+1)
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
    out = move(units[1], units[1].x, units[1].y+1)--units[1].y-1)
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



fog_of_war = false
