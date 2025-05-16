local file = io.open("input.txt", "r")

local config = {
	red = 12,
	green = 13,
	blue = 14,
}

local function find_max_of_color(game_string, color)
	local highest_match = 0
	for match in string.gmatch(game_string, "(%d+)" .. " " .. color) do
		local color_match = tonumber(match)
		if color_match > highest_match then
			highest_match = color_match
		end
	end
	return highest_match
end

local colors = { "red", "green", "blue" }
local possible_sum = 0
local all_power = 0
for line in file:lines() do
	local game_power = 1
	local game_id = string.match(line, "Game (%d+):")
	local possible = true

	for i = 1, #colors do
		local color = colors[i]
		local color_high = find_max_of_color(line, color)
		game_power = game_power * color_high

		if color_high > config[color] then
			possible = false
		end
	end
	if possible then
		possible_sum = possible_sum + tonumber(game_id)
	end
	all_power = all_power + game_power
end

print(possible_sum)
print(all_power)
