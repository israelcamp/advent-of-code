local file = io.open("input.txt", "r")

local sections = {}

local current_section = {}
for line in file:lines() do
	if line == "" then
		if #current_section > 0 then
			table.insert(sections, current_section)
			current_section = {}
		end
	else
		table.insert(current_section, line)
	end
end

if #current_section > 0 then
	table.insert(sections, current_section)
end

local function get_maps_from_section(section)
	local source_to_destination = {}
	for i = 2, #section do
		local line = section[i]
		local map = {}
		for match in string.gmatch(line, "%d+") do
			table.insert(map, tonumber(match))
		end

		local destination_start = map[1]
		local source_start = map[2]
		local range_length = map[3]
		table.insert(source_to_destination, {
			source = source_start,
			destination = destination_start,
			length = range_length,
		})
	end
	return source_to_destination
end

local function get_maped_value(map, value)
	for _, mapper in ipairs(map) do
		if value >= mapper.source and value < mapper.source + mapper.length then
			return mapper.destination + (value - mapper.source)
		end
	end
	return value -- If no mapping found, return the original value
end

-- SEEDS
local seeds = {}
for match in string.gmatch(sections[1][1], "%d+") do
	table.insert(seeds, tonumber(match))
end

local seed_to_soil = get_maps_from_section(sections[2])
local soil_to_fertilizer = get_maps_from_section(sections[3])
local fertilizer_to_water = get_maps_from_section(sections[4])
local water_to_light = get_maps_from_section(sections[5])
local light_to_temperature = get_maps_from_section(sections[6])
local temperature_to_humidity = get_maps_from_section(sections[7])
local humidity_to_location = get_maps_from_section(sections[8])

local seed_to_location = {}
local min_location = math.huge
for _, seed in ipairs(seeds) do
	local soil = get_maped_value(seed_to_soil, seed)
	local fertilizer = get_maped_value(soil_to_fertilizer, soil)
	local water = get_maped_value(fertilizer_to_water, fertilizer)
	local light = get_maped_value(water_to_light, water)
	local temperature = get_maped_value(light_to_temperature, light)
	local humidity = get_maped_value(temperature_to_humidity, temperature)
	local location = get_maped_value(humidity_to_location, humidity)
	seed_to_location[seed] = location
	if location < min_location then
		min_location = location
	end
end

print("Minimum location: " .. min_location)
