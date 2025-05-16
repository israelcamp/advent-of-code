local file, err = io.open("input.txt", "r")

local function get_sum_from_line(s)
	local matches = {}
	for match in string.gmatch(s, "%d") do
		table.insert(matches, match)
	end
	local result = tostring(matches[1]) .. tostring(matches[#matches])
	return tonumber(result)
end

if not file then
	print("Error opening file", err)
else
	local sum = 0
	for line in file:lines() do
		sum = sum + get_sum_from_line(line)
	end
	print(sum)
end
