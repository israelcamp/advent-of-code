local file = io.open("input.txt", "r")
local ths = 11

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
		elseif number_count < ths then
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

local cards = {}
for i = 1, #games do
	-- if i > 1 and not cards[i] then
	-- 	goto continue
	-- elseif i == 1 then
	-- 	cards[i] = 1
	-- end
	if not cards[i] then
		cards[i] = 1
	else
		cards[i] = cards[i] + 1
	end

	local matches = 0
	for _, my_number in ipairs(games[i].my_numbers) do
		if is_in_list(my_number, games[i].winning_numbers) then
			matches = matches + 1
		end
	end
	print("Game " .. i .. " has " .. matches .. " matches")
	for j = 1, matches do
		local key = i + j
		if key > #games then
			break
		end
		if not cards[key] then
			cards[key] = cards[i]
		else
			cards[key] = cards[key] + cards[i]
		end
	end
	::continue::
end

local total_cards = 0
for key, count in pairs(cards) do
	print(key .. " has " .. count .. " cards")
	total_cards = total_cards + count
end

print("Total cards: " .. total_cards)
