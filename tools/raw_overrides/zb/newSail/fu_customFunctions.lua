function fu_toggleAtmosphereMode()
	local text
	if player.worldId() ~= player.ownShipWorldId() then
		text = "Atmosfer modunu yalnızca geminin sahibi değiştirebilir."
	elseif world.getProperty("ship.level") ~= 0 then
		text = "Bu özellik yalnızca BYOS gemilerinde kullanılabilir."
	elseif world.getProperty("fu_byos.newAtmosphereSystem") then
		world.setProperty("fu_byos.newAtmosphereSystem", false)
		text = "BYOS atmosfer modu, yalnızca oyuncunun arkasında arka plan duvarı olup olmadığını denetleyecek şekilde ayarlandı."
	else
		world.setProperty("fu_byos.newAtmosphereSystem", true)
		text = "BYOS atmosfer modu, oyuncunun kapalı bir odada olup olmadığını denetleyecek şekilde ayarlandı (geliştirme aşamasında)."
	end
	resetGUI()
	textTyper.init(cfg.TextData, text)
end

function fu_configureShipPet()
	local shipPet = world.getObjectParameter(pane.sourceEntity(), "shipPetType")
	if not shipPet then
		text = "Bu özellik yalnızca evcil hayvanı olan S.A.I.L. konsollarında çalışır."
		resetGUI()
		textTyper.init(cfg.TextData, text)
		return
	end

	local petConfigPane = root.assetJson("/interface/objectcrafting/fu_pethouse/fu_pethouse.config")
	if petConfigPane and petConfigPane.gui then
		petConfigPane.gui.itemGrid = nil
		petConfigPane.gui.changeObjectPet = nil
		petConfigPane.gui.addObjectPetToList = nil
		petConfigPane.containerId = pane.sourceEntity()
		player.interact("ScriptPane", petConfigPane)
	end
end

function fu_crashberry()
	status.clearAllPersistentEffects()
	status.clearEphemeralEffects()
end

function fu_recheckresearch()
	player.setProperty("fu_recheckResearch",true)
end
