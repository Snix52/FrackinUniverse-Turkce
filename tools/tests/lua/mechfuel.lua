local results = {}
local messages, label, item
local function reset()
  messages = {}; label = nil; item = {name="fixtureFuel", count=2}
  self = {enabled=true, currentFuel=20, maxFuel=100, fuels={fixtureFuel={fuelMultiplier=30, fuelType="chemical"}}}
  widget = {
    itemSlotItem=function(name) assert(name=="itemSlot_fuel"); return item end,
    setText=function(name,text) assert(name=="lblEfficiency"); label=text end
  }
  player = {id=function() return 1 end}
  world = {type=function() return "ship" end, sendEntityMessage=function(id,command,value)
    assert(id==1); messages[command]=value; return {} end}
  pane = {playSound=function(sound) assert(sound=="/sfx/tech/mech_activate2.ogg") end}
end
local function test(name, fn)
  reset()
  local ok, err = pcall(fn)
  table.insert(results,name.."\t"..(ok and "PASS" or "FAIL").."\t"..(ok and "" or tostring(err)))
end
local function unchanged(amount)
  assert(self.currentFuel==amount and item.count==2 and next(messages)==nil)
end
test("Full tank warning and no consumption",function()
  self.currentFuel=100;fuel()
  assert(label=="^red;Depo dolu.^white;");unchanged(100)
end)
test("Incompatible fuel warning and no consumption",function()
  self.currentFuelType="otherType";fuel()
  assert(label=="^red;Depoda farklı türde yakıt var; önce depoyu boşalt.^white;");unchanged(20)
end)
test("Valid refuel keeps command IDs and calculations",function()
  fuel();assert(self.currentFuel==80 and item.count==0)
  assert(messages.setFuelType=="chemical" and messages.setQuestFuelCount==80 and label==nil)
end)
test("Compatible fuel remains accepted",function()
  self.currentFuelType="chemical";fuel();assert(self.currentFuel==80 and label==nil)
end)
test("No item remains a no-op",function()
  item=nil;fuel();assert(self.currentFuel==20 and next(messages)==nil and label==nil)
end)
test("Unauthorized refuel remains a no-op",function()
  self.enabled=false;fuel();unchanged(20);assert(label==nil)
end)
test("Unknown fuel remains a no-op",function()
  item.name="unsupported";fuel();unchanged(20);assert(label==nil)
end)
test("Missing max fuel remains a no-op",function()
  self.maxFuel=nil;fuel();unchanged(20);assert(label==nil)
end)
AUDIT_OUTPUT=table.concat(results,"\n")
