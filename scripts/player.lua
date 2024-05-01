
for i=1,3 do
    print("right")
    while move_right() do print("right") end

    print("up")
    while move_up() do print("up") end

    print("left")
    while move_left() do print("left") end

    print("down")
    while move_down() do print("down") end
end
