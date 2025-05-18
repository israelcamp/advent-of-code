local file = io.open("input.txt")

local matrix = {}
for line in file:lines() do
	local row = {}
	for i = 1, #line do
		local char = line:sub(i, i)
		table.insert(row, char)
	end
	table.insert(matrix, row)
end

local function tuple_key(a, b)
	return tostring(a) .. "," .. tostring(b)
end
-- lets find the value
local indices_to_numbers = {}
local numbers_global_index = 0
local current_number = ""
local current_indices = {}

for i, row in ipairs(matrix) do
	current_number = ""
	current_indices = {}
	for j, value in ipairs(row) do
		if string.match(value, "%d") then
			current_number = current_number .. value
			table.insert(current_indices, tuple_key(i, j))
		else
			if #current_number > 0 then
				for k, key in ipairs(current_indices) do
					indices_to_numbers[key] = { numbers_global_index, tonumber(current_number) }
				end
				numbers_global_index = numbers_global_index + 1
			end
			current_indices = {}
			current_number = ""
		end
	end
	if #current_number > 0 then
		for k, key in ipairs(current_indices) do
			indices_to_numbers[key] = { numbers_global_index, tonumber(current_number) }
		end
		numbers_global_index = numbers_global_index + 1
	end
end

local function find_numbers_around(row, col, matrix, indices_to_numbers, part_numbers)
	local directions = {
		{ 0, 1 },
		{ 0, -1 },
		{ 1, 0 },
		{ -1, 0 },
		{ -1, -1 },
		{ -1, 1 },
		{ 1, -1 },
		{ 1, 1 },
	}
	local max_rows = #matrix
	local max_cols = #matrix[1]
	for i = 1, #directions do
		local dir = directions[i]
		local drow = dir[1]
		local dcol = dir[2]
		local next_row = row + drow
		local next_col = col + dcol
		if next_row > 0 and next_row <= max_rows and next_col > 0 and next_col <= max_cols then
			local number = indices_to_numbers[tuple_key(next_row, next_col)]
			if number ~= nil then
				local index = number[1]
				local value = number[2]
				part_numbers[index] = value
			end
		end
	end
end

-- lets iterate on the grid to find the symbols
--
local part_numbers = {}
for i, row in ipairs(matrix) do
	for j, value in ipairs(row) do
		if value ~= "." and not string.match(value, "%d") then
			find_numbers_around(i, j, matrix, indices_to_numbers, part_numbers)
		end
	end
end

local result = 0
for key, value in pairs(part_numbers) do
	print(key, value)
	result = result + value
end

print(result)
