local file = io.open("input.txt", "r")

if not file then
	print("Could not open file")
	return
end

local lines = {}
for line in file:lines() do
	table.insert(lines, line)
end
file:close()

local directions = {}
local dir_map = { L = 1, R = 2 }
for char in lines[1]:gmatch(".") do
	table.insert(directions, dir_map[char])
end

local id = 1
local string_to_id = {}
local right_maps = {}
local left_maps = {}

for i = 3, #lines do
	local row = lines[i]
	local key = string.sub(row, 1, 3)
	local left = string.sub(row, 8, 10)
	local right = string.sub(row, 13, 15)

	local left_id = string_to_id[left]
	if not left_id then
		left_id = id
		id = id + 1
		string_to_id[left] = left_id
	end

	local right_id = string_to_id[right]
	if not right_id then
		right_id = id
		id = id + 1
		string_to_id[right] = right_id
	end

	local key_id = string_to_id[key]
	if not key_id then
		key_id = id
		id = id + 1
		string_to_id[key] = key_id
	end

	right_maps[key_id] = right_id
	left_maps[key_id] = left_id
end

local zzz_id = string_to_id["ZZZ"]
local current_key_id = string_to_id["AAA"]

local current_direction_index = 1
local current_direction = nil
local N = #directions

--
local steps = 0
while true do
	if current_key_id == zzz_id then
		break
	end
	current_direction = directions[current_direction_index]

	if current_direction == 1 then
		current_key_id = left_maps[current_key_id]
	else
		current_key_id = right_maps[current_key_id]
	end

	current_direction_index = current_direction_index + 1
	if current_direction_index > N then
		current_direction_index = 1
	end
	steps = steps + 1
end
print("Reached ZZZ after " .. steps .. " steps.")
