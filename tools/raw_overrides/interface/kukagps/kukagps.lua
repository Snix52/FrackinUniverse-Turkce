-- THIS IS THE FRACKIN RACES ONE
require "/scripts/util.lua"

MATERIALS = "materialList.materials"

function init()
        populateMaterialsList()
end

function addText(text)
	local path = string.format("%s.%s.text", MATERIALS, widget.addListItem(MATERIALS))
	widget.setText(path, text)
end

function addSeparator()
        addText("-------------------------------------------------------------------------------")
end

function populateMaterialsList()
        widget.clearListItems(MATERIALS)
        local worldId = string_split(player.worldId(),":")
        local planet = {location = {tonumber(worldId[2]),tonumber(worldId[3]),tonumber(worldId[4])}, planet = tonumber(worldId[5]), satellite = (tonumber(worldId[6]) or 0)}
        local system ={location = {tonumber(worldId[2]),tonumber(worldId[3]),tonumber(worldId[4])}}

        if worldId[1]=="InstanceWorld" then
            addText("Burası ayrı bir dünya alanı")

            -- More info about the dungeon could be added here
        elseif worldId[1]=="ClientShipWorld" then
                addText("Şu anda gemidesin")

                local shipInfo = player.shipUpgrades()
                local isBYOS = world.getProperty("fu_byos")

                if isBYOS then
                    addText("^green;Gemi türü:^reset; BYOS (Kendi Gemini İnşa Et)")
                    addText("Geminin dış duvarlarını kazarak alanı genişletebilirsin. Gemi yükseltme görevi yoktur.")

                    if (world.getProperty("fu_byos.systemTravel") or 0) > 0 then
                        addText("^green;Motor durumu^reset;: ^yellow;FTL motoru^reset; tam çalışır durumda (her yere yolculuk yapılabilir).")
                    elseif (world.getProperty("fu_byos.planetTravel") or 0) > 0 then
                        addText("^green;Motor durumu^reset;: ^yellow;STL Motoru^reset; (sistem içinde yolculuk yapılabilir).")
                        addText("Diğer sistemlere gitmek için motoru ^yellow;Küçük FTL Motoru^reset; ile değiştir.")
                        addText("Not: Motor türü ne olursa olsun sistem içi yolculukta yakıt harcanmaz.")
                    else
                        addText("^green;Motor durumu^reset;: ^red;devre dışı^reset; (çalışan motor bulunamadı).")
                        addText("Geminin herhangi bir yerine ^yellow;STL Motoru^reset; veya ^yellow;Küçük FTL Motoru^reset; yerleştirerek onarabilirsin.")
                    end
                else
                    addText("^green;Gemi türü:^reset; Ana oyun gemisi (BYOS değil)")

                    local shipLevel = shipInfo.shipLevel or 0
                    addText("^green;Gemi kademesi:^reset; " .. shipLevel)

                    if not contains(player.shipUpgrades().capabilities, "systemTravel") then
                        addText("^green;Motor durumu^reset;: ^red;devre dışı^reset; (onarılmadı).")
                        addText("Ana oyundaki Karakol'da Esther Bright ile buluştuğunda gemi hemen onarılır.")
                    else
                        addText("^green;Motor durumu^reset;: ^yellow;tam çalışır durumda^reset;.")
                        if shipLevel < 8 then
                            addText("Ana oyundaki gibi ^yellow;mürettebat^reset; veya ^yellow;lisanslar^reset; aracılığıyla yükseltilir.")
                        else
                            addText("En büyük boyuta ulaşıldı (gemi daha fazla genişletilemez).")
                        end
                    end
                end

                addSeparator()

                addText(string.format(
                    "^green;Yakıt tasarrufu:^reset; %.f%%",
                    100 * (shipInfo.fuelEfficiency or 0)
                ))
                addText("^green;Yakıt kapasitesi:^reset; " .. (shipInfo.maxFuel or '?'))
                addText("^green;Gemi hızı (sistem içi):^reset; " .. (shipInfo.shipSpeed or '?'))

                -- TODO: add information about the crew limits, etc.
        elseif worldId[1]=="CelestialWorld" then
            dungeons =root.assetJson("/interface/kukagps/dungeons.config")
            weather =root.assetJson("/interface/kukagps/weather.config")
            enviroment =root.assetJson("/interface/kukagps/enviroment.config")
            ores =root.assetJson("/interface/kukagps/ores.config")
            biomes =root.assetJson("/interface/kukagps/biomes.config")
            stars =root.assetJson("/interface/kukagps/stars.config")

            -- print system
            addText("^green;Sistem:^reset; "..celestial.planetName(system))

            local starType = celestial.planetParameters(system).typeName or "default"
            -- print star
            addText("^green;Yıldız:^reset; " .. (stars[starType] or '?'))

            -- print coord
            addText("^green;X koordinatı:^reset; "..system.location[1].."                        ^green;Y koordinatı:^reset; "..system.location[2])

            -- print planet
            addText("^green;Gezegen:^reset; "..celestial.planetName(planet))

            -- print planet primary biome
            local parameters = celestial.visitableParameters(planet)
            addText("                                                ^green;BİYOMLAR:^reset; ")

            local anomaliesFound=false
            local worldSize = world.size() or {0,0}

            -- Search for biomes.
            local function showLayer(layer, layerName, layerAbove, biomeColors)
                if not layer then return end

                local biomeCodes = {
                    layer.primaryRegion.biome,
                    layer.primarySubRegion.biome
                }
                for _, region in pairs(layer.secondaryRegions) do
                    table.insert(biomeCodes, region.biome)
                end
                for _, region in pairs(layer.secondarySubRegions) do
                    table.insert(biomeCodes, region.biome)
                end

                -- Remove duplicates, but preserve the order.
                local uniqueBiomeCodes = {}
                local alreadyListed = {}
                for _, biomeCode in ipairs(biomeCodes) do
                    if not alreadyListed[biomeCode] then
                        table.insert(uniqueBiomeCodes, biomeCode)
                        alreadyListed[biomeCode] = true
                    end
                end

                local listedBiomeNames = {}
                for _, biomeCode in ipairs(uniqueBiomeCodes) do
                    if isHiddenBiome(biomeCode) then
                        -- Semi-secret biomes like Precursor Underground are not listed.
                        anomaliesFound = true
                    else
                        local biomeName = biomes[biomeCode] or biomeCode
                        local biomeColor = biomeColors and biomeColors[biomeCode]
                        if biomeColor then
                            biomeName = string.format("^%s;%s^reset;", biomeColor, biomeName)
                        end

                        table.insert(listedBiomeNames, biomeName)
                    end
                end

                local biomesDescription
                if #listedBiomeNames == 0 then
                    -- The only biome is secret. Not really secret in this situation...
                    biomesDescription = '(tarama sonuçları belirsiz)'
                else
                    biomesDescription = table.concat(listedBiomeNames, ', ') .. '.'
                end

                local value = string.format("^green;%s^reset; [%s-%s]: %s",
                    layerName,
                    layer.layerMinHeight,
                    layerAbove and layerAbove.layerMinHeight or worldSize[2],
                    biomesDescription
                )
                addText(value)
            end

            showLayer(parameters.spaceLayer, "Uzay Katmanı")
            showLayer(parameters.atmosphereLayer, "Atmosfer Katmanı", parameters.spaceLayer)
            if parameters.surfaceLayer then
                showLayer(parameters.surfaceLayer, "Yüzey Katmanı", parameters.atmosphereLayer,
                    { [parameters.surfaceLayer.primaryRegion.biome] = "yellow" }
                )
            end
            showLayer(parameters.subsurfaceLayer, "Yüzey Altı Katmanı", parameters.surfaceLayer)

            local layerAboveCore
            if parameters.undergroundLayers then
                showLayer(parameters.undergroundLayers[1], "Yer Altı Katmanı 1", parameters.subsurfaceLayer)
                showLayer(parameters.undergroundLayers[2], "Yer Altı Katmanı 2", parameters.undergroundLayers[1])
                showLayer(parameters.undergroundLayers[3], "Yer Altı Katmanı 3", parameters.undergroundLayers[2])
                layerAboveCore = parameters.undergroundLayers[#parameters.undergroundLayers]
            end
            showLayer(parameters.coreLayer, "Çekirdek Katmanı", layerAboveCore or parameters.subsurfaceLayer)

            -- anomalies found?
            if anomaliesFound then
                addText("^red;Bu katmanlarda bazı anomaliler bulundu....^reset; ")
            end

            local pos = world.entityPosition(player.id())
            -- print pos
            addText("^green;X konumu:^reset; "..math.floor(pos[1]).."                                       ^green;Y konumu:^reset; "..math.floor(pos[2]))

            -- print world size
            addText("^green;Genişlik:^reset; "..worldSize[1].."                                            ^green;Yükseklik:^reset; "..worldSize[2])

            -- print planet threat and gravity
            addText(string.format("^green;Gezegen kademesi / Tehdit:^reset; %.2f", parameters.threatLevel))
            addText("^green;Yer çekimi:^reset; "..(parameters.gravity or 0))

            -- print planet ores names
            addText("^green;Cevherler:^reset; ")
            local localOres="None"
            local linecount=0
            for _,ore in pairs(celestial.planetOres(planet, (parameters.threatLevel or 0))) do
                if localOres=="None" then
                    localOres = (ores[ore] or ore)
                else
                    localOres = localOres..", "..(ores[ore] or ore)
                end
                linecount = linecount+1
                if linecount==7 then
                    -- print line and reset counter
                    localOres = localOres.."."
                    addText("       "..localOres)
                    localOres = "None"
                    linecount = 0
                end
            end
            if linecount ~= 0 then
                localOres = localOres.."."
                addText("       "..localOres)
            end

            addSeparator()

            if parameters.primaryBiome then -- asteroid fields don't have time in the typical sense
                -- print date
                addText("^green;Tarih:^reset; "..getDate(world.day()))

                -- print time
                addText("^green;Saat:^reset; "..timeConversion())

                -- print day length
                addText("^green;Gün uzunluğu:^reset; "..math.floor(world.dayLength()))
            end

            -- print light level
            local lightLevel = math.floor(world.lightLevel(world.entityPosition(player.id()))*100)/100
            addText("^green;Işık düzeyi:^reset; "..lightLevel)

            -- print windLevel
            local windLevel = math.floor(world.windLevel(world.entityPosition(player.id()))*100)/100
            addText("^green;Rüzgâr düzeyi:^reset; "..windLevel)

            -- print enviroment status effects
            local enviro="None"
            for _,env in pairs(parameters.environmentStatusEffects) do
                if enviro=="None" then
                    -- its the first.
                    enviro = enviroment[env] or env
                else
                    -- its NOT the first. Add comma.
                    enviro = enviro..", "..(enviroment[env] or env)
                end
            end

            addSeparator()

            enviro = enviro.."."
            addText("^green;Çevresel durum etkileri:^reset; "..enviro)

            addSeparator()

            addText("^green;Hava durumu:^reset; ")

            local weatherItem="None"
            linecount=0
            for _,w in pairs(parameters.weatherPool) do
                ww = (w.weight * 100)
                if weatherItem=="None" then
                    -- its the first.
                    weatherItem = (weather[w.item] or w.item).."("..ww.."%)"
                else
                    -- its NOT the first. Add comma.
                    weatherItem = weatherItem..", "..(weather[w.item] or w.item).."("..ww.."%)"
                end
                linecount = linecount+1
                if linecount==4 then
                    -- after 4 elements, print line and reset counter

                    weatherItem = weatherItem.."."
                    addText("          "..weatherItem)  -- print a long tab space, and then a line of weather info
                    weatherItem = "None"
                    linecount = 0
                end
            end
            if linecount ~= 0 then
                weatherItem = weatherItem.."."
                addText("          "..weatherItem)
            end

            addSeparator()

            -- print dungeons
            addText("^green;Gezegendeki zindanlar:^reset; ")

            -- Search for dungeons in spaceLayer. If exists in dungeon's list, look for name. Else, unknown dungeon.
            if (parameters.spaceLayer and parameters.spaceLayer.dungeons) then
                for _,dungeon in pairs(parameters.spaceLayer.dungeons) do
                    addText(dungeons[dungeon] or "Bilinmeyen["..dungeon.."]")
                end
            end
            -- Search for dungeons in atmosphereLayer. If exists in dungeon's list, look for name. Else, unknown dungeon.
            if (parameters.atmosphereLayer and parameters.atmosphereLayer.dungeons) then
                for _,dungeon in pairs(parameters.atmosphereLayer.dungeons) do
                    addText(dungeons[dungeon] or "Bilinmeyen["..dungeon.."]")
                end
            end
            -- Search for dungeons in surfaceLayer. If exists in dungeon's list, look for name. Else, unknown dungeon.
            if (parameters.surfaceLayer and parameters.surfaceLayer.dungeons) then
                for _,dungeon in pairs(parameters.surfaceLayer.dungeons) do
                    addText(dungeons[dungeon] or "Bilinmeyen["..dungeon.."]")
                end
            end
            -- Search for dungeons in subsurfaceLayer. If exists in dungeon's list, look for name. Else, unknown dungeon.
            if (parameters.subsurfaceLayer and parameters.subsurfaceLayer.dungeons) then
                for _,dungeon in pairs(parameters.subsurfaceLayer.dungeons) do
                    addText(dungeons[dungeon] or "Bilinmeyen["..dungeon.."]")
                end
            end
            -- Search for dungeons in undergroundLayers. If exists in dungeon's list, look for name. Else, unknown dungeon.
            if (parameters.undergroundLayers) then
                for _,layer in pairs(parameters.undergroundLayers) do
                    -- you have to go in every layer inside undergroundLayers
                    for _,dungeon in pairs(layer.dungeons) do
                        addText(dungeons[dungeon] or "Bilinmeyen["..dungeon.."]")
                    end
                end
            end
            -- Search for dungeons in corelayer. If exists in dungeon's list, look for name. Else, unknown dungeon.
            if (parameters.coreLayer and parameters.coreLayer.dungeons) then
                for _,dungeon in pairs(parameters.coreLayer.dungeons) do
                    addText(dungeons[dungeon] or "Bilinmeyen["..dungeon.."]")
                end
            end
        else
            -- no ship, no dungeon/instance and no world.......Where the fuck are you?
            addText("Dünya bilgileri alınamadı")
        end
end

-- contribution of zimberzimber
function string_split(str, pat)
    local t = {}  -- NOTE: use {n = 0} in Lua-5.0
    local fpat = "(.-)" .. pat
    local last_end = 1
    local s, e, cap = str:find(fpat, 1)
    while s do
        if s ~= 1 or cap ~= "" then
            table.insert(t, cap)
        end
        last_end = e+1
        s, e, cap = str:find(fpat, last_end)
        end
        if last_end <= #str then
            cap = str:sub(last_end)
            table.insert(t, cap)
        end
        return t
end

function timeConversion()
        -- Hubnester time conversion function
        hubTime = (world.timeOfDay() + 0.25) * 24    -- the 0.25 is to make 0 am = 6 am (when the day starts)
        if hubTime > 12 then
            hubTime = hubTime - 12
            hubTimeModifier = " pm"
            if hubTime > 12 then
                hubTime = hubTime - 12
                hubTimeModifier = " am"
                if hubTime < 1 then
                    hubTime = hubTime + 12
                end
            elseif hubTime < 1 then
                hubTime = hubTime + 12
            end
        else
            hubTimeModifier = " am"
        end
        hubHours = math.floor(hubTime, 0)
        hubMinutes = math.floor((hubTime - hubHours) * 60)
        if hubMinutes < 10 then
            hubMinutes = "0" .. tostring(hubMinutes)
        end
        return tostring(hubHours) .. ":" .. tostring(hubMinutes) .. tostring(hubTimeModifier)
end

function getDate(days)
    local month=1
    local daysperyear=365.242
	local year = math.floor(days / daysperyear)
	days = math.floor(days % daysperyear)
    local dayspermonth={31,28,31,30,31,30,31,31,30,31,30,31}
    if ((year%4)==0) or (((year%100)==0) and ((year%400)==0)) then
       dayspermonth={31,29,31,30,31,30,31,31,30,31,30,31}
    end
    while (days>=dayspermonth[month]) do
       days=days-dayspermonth[month]
       month=month+1
    end
    days=days+1
    return "Year "..year..", Month "..month.." and Day "..days
end

local precursorBiomes = {
    precursorsurface = true,
    precursorunderground = true
}
local elderBiomes = {
    atropuselder = true,
    atropuselderunderground = true,
    elder = true,
    elderunderground = true,
    shoggothbiome = true
}

function isHiddenBiome(biomeCode)
    if precursorBiomes[biomeCode] then
        return not player.hasCompletedQuest("precursor_unlock")
    elseif elderBiomes[biomeCode] then
        return not player.hasQuest('create_elder')
    end

    return false
end
