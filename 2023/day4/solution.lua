local file = io.open("input.txt", "r")

local function printFile(file)
	if not file then
		print("File not found")
		return
	end

	for line in file:lines() do
		print(line)
	end

	file:close()
end

local function printGames(games)
	for i, game in ipairs(games) do
		print("Game " .. i .. ":")
		print("Winning Numbers: " .. table.concat(game.winning_numbers, ", "))
		print("My Numbers: " .. table.concat(game.my_numbers, ", "))
	end
end

local function is_in_list(value, list)
	for _, v in ipairs(list) do
		if v == value then
			return true
		end
	end
	return false
end

local games = {}
for line in file:lines() do
	local winning_numbers = {}
	local my_numbers = {}
	local number_count = 0
	for number in line:gmatch("%d+") do
		if number_count == 0 then
			print("Doing nothing")
		elseif number_count < 11 then
			table.insert(winning_numbers, tonumber(number))
		else
			table.insert(my_numbers, tonumber(number))
		end
		number_count = number_count + 1
	end
	games[#games + 1] = {
		winning_numbers = winning_numbers,
		my_numbers = my_numbers,
	}
end

printFile(file)
printGames(games)

local total_score = 0
for i = 1, #games do
	local matches = 0
	for _, my_number in ipairs(games[i].my_numbers) do
		if is_in_list(my_number, games[i].winning_numbers) then
			matches = matches + 1
		end
	end
	local score = 0
	if matches == 1 then
		score = 1
	elseif matches > 1 then
		score = 2 ^ (matches - 1)
	end
	total_score = total_score + score
end

print("Total Score: " .. total_score)
