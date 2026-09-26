-- Focused host-stub test for the shipped player deployment script.
-- Run from the repository root with a Lua 5.4 runtime.
local state
local priorInitCalls, priorUpdateCalls = 0, 0
init = function() priorInitCalls = priorInitCalls + 1 end
update = function() priorUpdateCalls = priorUpdateCalls + 1 end

local function reset()
  state = {
    shipLevel = 1,
    currentWorld = "ship:owner",
    ownWorld = "ship:owner",
    playerPosition = {100, 100},
    names = {[10] = "fu_byosteleporter"},
    positions = {[10] = {100, 100}},
    objects = {10},
    background = "shipwall",
    occupied = false,
    placeResult = true,
    placeCalls = 0,
    markCalls = 0,
    blueprintCalls = 0,
    warnings = 0
  }
  init()
end

world = {
  getProperty = function(key)
    if key == "ship.level" then return state.shipLevel end
    if key == "fu_tr_ebrar_star_placed" then return state.marked end
  end,
  setProperty = function(key, value)
    assert(key == "fu_tr_ebrar_star_placed" and value == true)
    state.markCalls = state.markCalls + 1
    state.marked = value
  end,
  objectQuery = function(_, radius)
    assert(radius == 96)
    if state.queryError then error("query failed") end
    return state.objects
  end,
  entityName = function(id) return state.names[id] end,
  entityPosition = function(id)
    if id == 1 then return state.playerPosition end
    return state.positions[id]
  end,
  material = function(_, layer)
    assert(layer == "background")
    return state.background
  end,
  tileIsOccupied = function(_, foreground)
    assert(foreground == true)
    return state.occupied
  end,
  placeObject = function(name, tile)
    assert(name == "futrebrarstar")
    state.placeCalls = state.placeCalls + 1
    state.lastTile = tile
    if state.placeResult then
      state.events = state.events or {}
      table.insert(state.events, "place")
    end
    return state.placeResult
  end
}
player = {
  id = function() return 1 end,
  worldId = function() return state.currentWorld end,
  ownShipWorldId = function() return state.ownWorld end,
  giveBlueprint = function(item)
    assert(item.name == "futrebrarstar" and item.count == 1)
    state.blueprintCalls = state.blueprintCalls + 1
  end
}
-- Starbound player deployment does not expose mcontroller.
mcontroller = nil
sb = {logWarn = function() state.warnings = state.warnings + 1 end}

-- SCRIPT UNDER TEST

local results = {}
local function check(name, action)
  reset()
  action()
  table.insert(results, name .. "\tPASS\tok")
end

check("existing-own-ship-placed-once", function()
  local before = priorUpdateCalls
  update(1)
  assert(priorUpdateCalls == before + 1 and priorInitCalls >= 1)
  assert(state.blueprintCalls == 1)
  assert(state.placeCalls == 1 and state.marked == true and state.markCalls == 1)
  assert(state.lastTile[1] == 105 and state.lastTile[2] == 104)
  update(10)
  assert(state.placeCalls == 1 and state.markCalls == 1)
end)

check("other-players-ship-is-untouched", function()
  state.currentWorld = "ship:friend"
  update(1)
  assert(state.placeCalls == 0 and state.markCalls == 0)
end)

check("generic-unknown-world-is-untouched", function()
  state.shipLevel = nil
  update(1)
  assert(state.placeCalls == 0 and state.markCalls == 0)
end)

check("ship-id-not-ready-retries", function()
  state.ownWorld = nil
  update(1)
  assert(state.placeCalls == 0)
  state.ownWorld = state.currentWorld
  update(10)
  assert(state.placeCalls == 1 and state.marked == true)
end)

check("player-entity-not-ready-retries", function()
  state.playerPosition = nil
  update(1)
  assert(state.placeCalls == 0 and state.warnings == 0)
  state.playerPosition = {100, 100}
  update(10)
  assert(state.placeCalls == 1 and state.marked == true)
end)

check("missing-teleporter-retries", function()
  state.objects = {}
  update(1)
  assert(state.placeCalls == 0 and state.markCalls == 0)
  state.objects = {10}
  update(10)
  assert(state.placeCalls == 1 and state.marked == true)
end)

check("full-ship-never-overwrites-objects", function()
  state.occupied = true
  update(1)
  assert(state.placeCalls == 0 and state.markCalls == 0)
end)

check("no-background-never-places-outside-ship", function()
  state.background = false
  update(1)
  assert(state.placeCalls == 0 and state.markCalls == 0)
end)

check("failed-placement-retries-without-marker", function()
  state.placeResult = false
  update(1)
  assert(state.placeCalls > 0 and state.markCalls == 0 and state.marked == nil)
  state.placeResult = true
  update(10)
  assert(state.marked == true and state.markCalls == 1)
end)

check("existing-star-is-adopted-without-duplicate", function()
  state.names[20] = "futrebrarstar"
  state.objects = {20, 10}
  update(1)
  assert(state.placeCalls == 0 and state.marked == true)
end)

check("teleporter-name-is-case-insensitive", function()
  state.names[10] = "Fu_ByosTeleporterTier0"
  update(1)
  assert(state.placeCalls == 1 and state.marked == true)
end)

check("placement-errors-do-not-break-existing-player-update", function()
  state.queryError = true
  local before = priorUpdateCalls
  update(1)
  update(10)
  assert(priorUpdateCalls == before + 2 and state.warnings == 1)
  assert(state.markCalls == 0)
end)

AUDIT_OUTPUT = table.concat(results, "\n")
