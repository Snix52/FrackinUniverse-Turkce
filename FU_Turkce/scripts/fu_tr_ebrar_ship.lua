-- A small, one-time surprise on the player's own ship. This script is appended to
-- deploymentConfig/scripts, so it must preserve callbacks installed before it.
local previousInit = init
local previousUpdate = update

local objectName = "futrebrarstar"
local placedProperty = "fu_tr_ebrar_star_placed"
local retrySeconds = 1
local loggedError = false
local heights = {4, 3, 5, 2, 6, 7}

local function ownShip()
  if type(world.getProperty("ship.level")) ~= "number" then return false end
  local current = player.worldId()
  local own = player.ownShipWorldId()
  return current ~= nil and own ~= nil and current == own
end

local function tryPlaceStar()
  if not ownShip() or world.getProperty(placedProperty) == true then return end

  -- Deployment scripts have player/world bindings, but no mcontroller table.
  -- The player entity may not be visible yet while entering a world; retry later.
  local playerPosition = world.entityPosition(player.id())
  if not playerPosition then return end
  local nearby = world.objectQuery(playerPosition, 96, {order = "nearest"})
  local teleporter
  for _, id in ipairs(nearby) do
    local name = world.entityName(id)
    if name == objectName then
      -- Also recover if a previous session placed the object but closed before
      -- the property was saved.
      world.setProperty(placedProperty, true)
      return
    end
    if type(name) == "string" and name:lower():find("teleporter", 1, true) then
      teleporter = teleporter or id
    end
  end
  if not teleporter then return end

  local position = world.entityPosition(teleporter)
  if not position then return end
  local baseX, baseY = math.floor(position[1]), math.floor(position[2])
  for distance = 5, 10 do
    for _, height in ipairs(heights) do
      for _, sign in ipairs({1, -1}) do
        local tile = {baseX + sign * distance, baseY + height}
        -- A background tile keeps the star inside a ship room; placement itself
        -- checks the object's anchor and all of its occupied spaces.
        if type(world.material(tile, "background")) == "string"
          and not world.tileIsOccupied(tile, true)
          and world.placeObject(objectName, tile) then
          world.setProperty(placedProperty, true)
          return
        end
      end
    end
  end
end

function init(...)
  if previousInit then previousInit(...) end
  retrySeconds = 1
  loggedError = false
  -- Default blueprints cover new characters; teach existing saves too.
  local ok, err = pcall(function()
    player.giveBlueprint({name = objectName, count = 1})
  end)
  if not ok then
    sb.logWarn("Ebrar star blueprint unlock failed: %s", tostring(err))
  end
end

function update(dt, ...)
  if previousUpdate then previousUpdate(dt, ...) end
  retrySeconds = retrySeconds - dt
  if retrySeconds > 0 then return end
  retrySeconds = 10
  local ok, err = pcall(tryPlaceStar)
  if not ok and not loggedError then
    sb.logWarn("Ebrar star ship placement failed: %s", tostring(err))
    loggedError = true
  end
end
