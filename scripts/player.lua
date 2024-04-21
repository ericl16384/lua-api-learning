-- while true do
--   while move_up() do end
--   while move_left() do end
--   while move_down() do end
--   while move_right() do end
-- end

-- solves mazes without loops - but broken :/
function amazing()
  moves = 0
  while move_forward() do
    moves = moves + 1
  end

  -- right path
  turn_right()
  if move_forward() then
    amazing()
    move_forward()
  end

  -- left path
  turn_right()
  turn_right()
  if move_forward() then
    amazing()
    move_forward()
  end

  -- back up
  turn_left()
  while moves > 0 do
    move_forward()
    moves = moves - 1
  end
  turn_left()
  turn_left()
end

amazing()
