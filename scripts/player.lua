-- get_next_move = coroutine.create(function()
--     -- for i=1,10 do
--     --     print("co", i)
--     --     coroutine.yield(i)
--     -- end
--     coroutine.yield()
-- end)

while true do
    print("up")
    while move_up() do print("up") end

    print("left")
    while move_left() do print("left") end

    print("down")
    while move_down() do print("down") end

    print("right")
    while move_right() do print("right") end
end

-- -- solves mazes without loops - but broken :/
-- function amazing()
--   moves = 0
--   while move_forward() do
--     moves = moves + 1
--   end

--   -- right path
--   turn_right()
--   if move_forward() then
--     amazing()
--     move_forward()
--   end

--   -- left path
--   turn_right()
--   turn_right()
--   if move_forward() then
--     amazing()
--     move_forward()
--   end

--   -- back up
--   turn_left()
--   while moves > 0 do
--     move_forward()
--     moves = moves - 1
--   end
--   turn_left()
--   turn_left()
-- end

-- amazing()
