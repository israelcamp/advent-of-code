local file, err = io.open("input.txt", "r")

local function matches_num(current_string)
	if string.match(current_string, "one") then
		return 1
	elseif string.match(current_string, "two") then
		return 2
	elseif string.match(current_string, "three") then
		return 3
	elseif string.match(current_string, "four") then
		return 4
	elseif string.match(current_string, "five") then
		return 5
	elseif string.match(current_string, "six") then
		return 6
	elseif string.match(current_string, "seven") then
		return 7
	elseif string.match(current_string, "eight") then
		return 8
	elseif string.match(current_string, "nine") then
		return 9
	else
		return -1
	end
end

--@param s string
local function get_sum_from_line(s)
	local matches = {}

	local current_string = ""
	for i = 1, #s do
		local char = s:sub(i, i)
		if string.match(char, "%d") then
			table.insert(matches, tonumber(char))
			current_string = ""
		else
			current_string = current_string .. char
			local num = matches_num(current_string)
			if num > -1 then
				table.insert(matches, num)
				current_string = current_string:sub(#current_string, #current_string)
			end
		end
	end
	local result = tostring(matches[1]) .. tostring(matches[#matches])
	return tonumber(result)
end

if not file then
	print("Error opening file", err)
else
	local sum = 0
	for line in file:lines() do
		local line_result = get_sum_from_line(line)
		sum = sum + line_result
	end
	print(sum)
end
