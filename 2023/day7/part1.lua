local file = io.open("input.txt", "r")

if not file then
	print("Could not open file")
	return
end

function split(inputstr, sep)
	sep = sep or "%s" -- default to whitespace
	local t = {}
	for str in string.gmatch(inputstr, "([^" .. sep .. "]+)") do
		table.insert(t, str)
	end
	return t
end

function dict_length(t)
	local count = 0
	for _ in pairs(t) do
		count = count + 1
	end
	return count
end

local data = {}
for line in file:lines() do
	local parts = split(line, " ")
	local hand = parts[1]
	local bid = parts[2]

	local cards = {}
	for char in string.gmatch(hand, ".") do
		table.insert(cards, char)
	end

	table.insert(data, { hand = cards, bid = tonumber(bid), hand_string = hand })
end

file:close()

function indexOf(t, value)
	for i, v in ipairs(t) do
		if v == value then
			return i
		end
	end
	return nil -- Not found
end

function get_max(char_count)
	local max_count = 0
	for _, count in pairs(char_count) do
		if count > max_count then
			max_count = count
		end
	end
	return max_count
end

function calculate_hand_strength(hand)
	local char_count = {}
	for i = 1, #hand do
		local char = hand[i]
		char_count[char] = (char_count[char] or 0) + 1
	end
	local len = dict_length(char_count)
	local max_score = 7
	if len == 1 then
		return max_score -- All cards are the same
	end

	local max_count = get_max(char_count)
	if len == 2 and max_count == 4 then
		return max_score - 1 -- Four of a kind
	end

	if len == 2 and max_count == 3 then
		return max_score - 2 -- Full house
	end

	if len == 3 and max_count == 3 then
		return max_score - 3 -- Three of a kind
	end

	if len == 3 and max_count == 2 then
		return max_score - 4 -- Two pairs
	end

	if len == 4 then
		return max_score - 5 -- One pair
	end

	if len == 5 then
		return max_score - 6 -- High card
	end

	return 1
end

for i, entry in ipairs(data) do
	local hand = entry.hand

	local hand_strength = calculate_hand_strength(hand)
	entry.hand_strength = hand_strength
end

local groups = {}
for i, entry in ipairs(data) do
	local hand_strength = entry.hand_strength
	if not groups[hand_strength] then
		groups[hand_strength] = {}
	end
	table.insert(groups[hand_strength], entry)
end

local card_strengths = { "A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2" }

function is_a_stronger(a, b)
	local cards_a = a.hand
	local cards_b = b.hand
	for i = 1, #cards_a do
		local a = indexOf(card_strengths, cards_a[i])
		local b = indexOf(card_strengths, cards_b[i])
		if a ~= b then
			return a > b
		end
	end
	return false -- They are equal
end

for strength, entries in pairs(groups) do
	table.sort(entries, is_a_stronger)
end

local total = 0
local rank = 1
for curent_strength = 1, 7 do
	if not groups[curent_strength] then
		goto continue
	end

	local entries = groups[curent_strength]
	for _, entry in ipairs(entries) do
		total = total + entry.bid * rank

		rank = rank + 1
	end

	::continue::
end

print("Total: " .. total)
