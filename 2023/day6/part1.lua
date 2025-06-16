local file = io.open("input.txt", "r")

if not file then
	print("Could not open file")
	return
end

local times = {}
local distances = {}
local line_count = 0
for line in file:lines() do
	local numbers = {}
	for num in line:gmatch("%d+") do
		table.insert(numbers, tonumber(num))
	end
	if line_count == 0 then
		times = numbers
	elseif line_count == 1 then
		distances = numbers
	else
		print("Unexpected line in file: " .. line)
	end
	line_count = line_count + 1
end
file:close()

local total = 1
for i = 1, #times do
	local T = times[i]
	local d = distances[i]
	local delta = math.sqrt(T * T - 4 * d)
	local h1 = math.ceil(((T + delta) / 2) - 1)
	local h2 = math.floor(((T - delta) / 2) + 1)
	local solutions = h1 - h2 + 1
	total = total * solutions
	print("For T = " .. T .. " and d = " .. d .. ", h1 = " .. h1 .. ", h2 = " .. h2 .. ", solutions = " .. solutions)
end

print("Total number of solutions: " .. total)
