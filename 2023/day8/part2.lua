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

local start_ids = {}
local target_ids = {}

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

	local key_last_char = key:sub(3, 3)
	if key_last_char == "A" then
		print("Start ID", key_id, key)
		table.insert(start_ids, key_id)
	elseif key_last_char == "Z" then
		print("Target ID", key_id, key)
		table.insert(target_ids, key_id)
	end
end

local function find(key, targets)
	for _, v in ipairs(targets) do
		if key == v then
			return true
		end
	end
	return false
end

local function ended(current_ids, target_ids)
	for _, cur in pairs(current_ids) do
		local found = find(cur, target_ids)
		if not found then
			return false
		end
	end
	return true
end

local N = #directions

-- ALL THIS PER START ID
local function reach_targets(start_id)
	local current_direction_index = 1
	local current_direction = nil
	local current_key_id = start_id
	local target_to_steps = {}
	local steps_to_loop = nil
	local steps = 0
	local steps_between = 0
	local current_sb = 0

	while steps < id * N do
		current_direction = directions[current_direction_index]

		if current_direction == 1 then
			current_key_id = left_maps[current_key_id]
		else
			current_key_id = right_maps[current_key_id]
		end
		steps = steps + 1
		steps_between = steps_between + 1

		if find(current_key_id, target_ids) then
			print("Steps BETWEEN", steps_between)
			table.insert(target_to_steps, { current_key_id, steps })
			current_sb = steps_between
			steps_between = 0
		end

		if current_key_id == start_id then
			steps_to_loop = steps
			break
		end

		current_direction_index = current_direction_index + 1
		if current_direction_index > N then
			current_direction_index = 1
		end
	end
	return { target_to_steps, current_sb }
end

local steps_btw = {}
for _, start_id in ipairs(start_ids) do
	local d = reach_targets(start_id)
	local target_to_steps = d[1]
	local steps_between = d[2]
	table.insert(steps_btw, steps_between)

	print("==============")
	print("Start ID", start_id)
	for _, ts in ipairs(target_to_steps) do
		print(ts[1], ts[2])
	end
	print("==============")
end

local function gcd(a, b)
	while b ~= 0 do
		a, b = b, a % b
	end
	return a
end
local function lcm(a, b)
	if a == 0 or b == 0 then
		return 0 -- by convention, lcm(0, x) = 0
	end
	return math.floor(math.abs(a * b) / gcd(a, b))
end
local function lcm_list(tbl)
	local result = tbl[1]
	for i = 2, #tbl do
		result = lcm(result, tbl[i])
	end
	return result
end

-- example:
print(lcm_list(steps_btw)) -- → 60
