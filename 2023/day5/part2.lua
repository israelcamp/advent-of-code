-- Advent of Code 2023 Day 5 – Part Two (Lua)

-- 1. Read and split input into sections
local function read_and_split_input(path)
	local file = io.open(path, "r")
	assert(file, "Could not open input file")
	local sections = {}
	local current = {}
	for line in file:lines() do
		if line == "" then
			if #current > 0 then
				table.insert(sections, current)
				current = {}
			end
		else
			table.insert(current, line)
		end
	end
	if #current > 0 then
		table.insert(sections, current)
	end
	file:close()
	return sections
end

-- 2. Parse seeds line into intervals { lo, hi }
local function parse_seed_intervals(line)
	local nums = {}
	for n in line:gmatch("%d+") do
		table.insert(nums, tonumber(n))
	end
	local ivs = {}
	for i = 1, #nums, 2 do
		local start, len = nums[i], nums[i + 1]
		table.insert(ivs, { lo = start, hi = start + len - 1 })
	end
	return ivs
end

-- 3. Parse map section into rules { s_lo, s_hi, d_lo }
local function parse_map_rules(section)
	local rules = {}
	for i = 2, #section do
		local d, s, len = section[i]:match("(%d+)%s+(%d+)%s+(%d+)")
		d, s, len = tonumber(d), tonumber(s), tonumber(len)
		table.insert(rules, { s_lo = s, s_hi = s + len - 1, d_lo = d })
	end
	table.sort(rules, function(a, b)
		return a.s_lo < b.s_lo
	end)
	return rules
end

-- 4. Map one interval through a set of rules, including identity gaps
local function map_one_interval(iv, rules)
	local outs = {}
	-- 4a. rule-based translations
	for _, r in ipairs(rules) do
		local lo = math.max(iv.lo, r.s_lo)
		local hi = math.min(iv.hi, r.s_hi)
		if lo <= hi then
			table.insert(outs, {
				lo = r.d_lo + (lo - r.s_lo),
				hi = r.d_lo + (hi - r.s_lo),
			})
		end
	end
	-- 4b. identity for gaps
	local cur = iv.lo
	for _, r in ipairs(rules) do
		if r.s_lo > cur then
			local gap_hi = math.min(iv.hi, r.s_lo - 1)
			if cur <= gap_hi then
				table.insert(outs, { lo = cur, hi = gap_hi })
			end
		end
		cur = math.max(cur, r.s_hi + 1)
		if cur > iv.hi then
			break
		end
	end
	if cur <= iv.hi then
		table.insert(outs, { lo = cur, hi = iv.hi })
	end
	return outs
end

-- 5. Merge overlapping or adjacent intervals
local function merge_intervals(list)
	table.sort(list, function(a, b)
		return a.lo < b.lo
	end)
	local merged = {}
	for _, iv in ipairs(list) do
		local last = merged[#merged]
		if last and iv.lo <= last.hi + 1 then
			last.hi = math.max(last.hi, iv.hi)
		else
			table.insert(merged, { lo = iv.lo, hi = iv.hi })
		end
	end
	return merged
end

-- 6. Propagate a list of intervals through one map
local function propagate_intervals(intervals, rules)
	local out = {}
	for _, iv in ipairs(intervals) do
		local mapped = map_one_interval(iv, rules)
		for _, m in ipairs(mapped) do
			table.insert(out, m)
		end
	end
	return merge_intervals(out)
end

-- Main
local sections = read_and_split_input("input.txt")
local seed_intervals = parse_seed_intervals(sections[1][1])

-- Parse all seven maps
local maps = {}
for i = 2, 8 do
	maps[i - 1] = parse_map_rules(sections[i])
end

-- Propagate through each map
local intervals = seed_intervals
for _, rules in ipairs(maps) do
	intervals = propagate_intervals(intervals, rules)
end

-- Find the minimum location
local min_loc = math.huge
for _, iv in ipairs(intervals) do
	if iv.lo < min_loc then
		min_loc = iv.lo
	end
end

print("Part 2 minimum location: " .. min_loc)
