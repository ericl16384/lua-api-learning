
-- foo = 1
-- bar = {1, 3, "hi"}

-- test = "hello world"

-- usage: just call it in a Lua environment and look for a file called out.txt

-- lists all global variables in a file
function writeAllGlobals()	
	local file = io.open("out.txt", "w+")

    local seen={}
    local function dump(t,i)
        seen[t]=true
        local s={}
        local n=0
        for k, v in pairs(t) do
            n=n+1
			s[n]=tostring(k)
        end
        table.sort(s)
        for k,v in ipairs(s) do
            file:write(i .. v .. "\n")
            v=t[v]
            if type(v)=="table" and not seen[v] then
                dump(v,i.."\t")
            end
        end
    end

    dump(_G,"")
	file:close()
end

-- version with print
-- can be tested here: https://www.lua.org/cgi-bin/demo
function printAllGlobals()
	local seen={}
	local function dump(t,i)
		seen[t]=true
		local s={}
		local n=0
		for k, v in pairs(t) do
			n=n+1
			s[n]=tostring(k)
		end
		table.sort(s)
		for k,v in ipairs(s) do
			print(i .. v)
			v=t[v]
			if type(v)=="table" and not seen[v] then
				dump(v,i.."\t")
			end
		end
	end

	dump(_G,"")
end

printAllGlobals()

-- io.write("hi")

-- io = 7

-- io.write("hi")

-- io.write(hi)
-- hi + hello



-- -- script.lua
-- -- Receives a table, returns the sum of its components.
-- io.write("The table the script received has:\n");
-- x = 0
-- for i = 1, #foo do
--   print(i, foo[i])
--   x = x + foo[i]
-- end
-- io.write("Returning data back to C\n");
-- return x