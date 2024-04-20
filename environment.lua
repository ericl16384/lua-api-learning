-- https://www.lua.org/manual/5.4/
debug = nil
io = nil
os = nil
package = nil
python = nil

-- https://www.lua.org/pil/5.2.html
__caught_print_output = ""
function print(...)
    local arg = {...}

    if arg == nil then
        arg = {""}
    end

    for i, v in ipairs(arg) do
        __caught_print_output = __caught_print_output .. tostring(v) .. "\t"
    end
    __caught_print_output = __caught_print_output .. "\n"
end


return "environment.lua success"
-- but there will probably be more...