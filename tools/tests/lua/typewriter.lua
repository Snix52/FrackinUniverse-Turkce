
sb = {logError = function(...) end}
pane = {playSound = function(...) end, stopAllSounds = function(...) end}
player = {id = function() return 1 end}
world = {entityName = function() return "Çağrı" end}
widget = {setText = function(w, text) assert(utf8.len(text), "invalid UTF-8 sent to widget") end}
local results = {}
local function test(name, fn)
  local ok, err = pcall(fn)
  table.insert(results, name .. "\t" .. (ok and "PASS" or "FAIL") .. "\t" .. (ok and "" or tostring(err)))
end
local function complete(source, textData, validateUtf8)
  local td = textData or {}
  textTyper.init(td, source)
  local frames = 0
  while not td.isFinished do
    textTyper.update(td, "testWidget")
    frames = frames + 1
    assert(frames < 10000, "did not finish")
    if validateUtf8 then assert(utf8.len(td.written), "invalid UTF-8 during typing") end
  end
  return td.written, frames
end

test("ASCII exact output", function()
  assert(complete("Hello world!") == "Hello world!")
end)
test("All Turkish letters and each intermediate frame", function()
  local text = "çÇğĞıİöÖşŞüÜ Türkçe"
  local output = complete(text, nil, true)
  assert(output == text)
end)
test("One Turkish codepoint per typing step", function()
  local td = {}; textTyper.init(td, "çğıİöşü")
  for i=1,7 do textTyper.update(td); assert(utf8.len(td.written)==i) end
end)
test("Three and four-byte codepoints", function()
  local text = "A€中🛰B"; assert(complete(text, nil, true) == text)
end)
test("Color tokens remain exact", function()
  local text = "^red;Şarj^reset; +10%"; assert(complete(text, nil, true) == text)
end)
test("Pause token preserves visible output and delay", function()
  local output, frames = complete("A[(pause)2]Ş", nil, true)
  assert(output == "AŞ"); assert(frames == 6, "unexpected frame count: " .. frames)
end)
test("Instant Turkish segment", function()
  local td={}; textTyper.init(td, "A[(instant)Şarj]B")
  textTyper.update(td); textTyper.update(td)
  assert(td.written=="AŞarj")
  assert(complete("A[(instant)Şarj]B", nil, true)=="AŞarjB")
end)
test("Turkish dynamic data substitution", function()
  assert(complete("[(data)value] hazır", {value="İnce İşçilik"}, true)=="İnce İşçilik hazır")
end)
test("Turkish player name substitution", function()
  assert(complete("Merhaba [(playername)]!", nil, true)=="Merhaba Çağrı!")
end)
test("Skip handles color, pause and Turkish letters", function()
  local td={}; textTyper.init(td, "^red;Ş[(pause)4]ü^reset;")
  textTyper.skip(td,"testWidget")
  assert(td.written=="^red;Şü^reset;" and td.isFinished)
end)
test("Callback after Turkish character", function()
  local called=0
  local output=complete("ğ[(function)callback]x", {callback=function() called=called+1 end}, true)
  assert(output=="ğx" and called==1)
end)
test("Nil fallback does not crash", function()
  local output=complete(nil)
  assert(string.find(output,"received a nil value",1,true))
end)
test("Scramble range does not corrupt surrounding Turkish", function()
  local td={}; textTyper.init(td,"ş[(scramble)3]ü")
  while not td.isFinished do
    textTyper.update(td); textTyper.scrambling(td)
    assert(utf8.len(td.written),"scramble emitted invalid UTF-8")
  end
  assert(string.sub(td.written,1,2)=="ş")
  assert(string.sub(td.written,-2)=="ü")
end)
test("Empty input finishes", function() assert(complete("")=="") end)

AUDIT_OUTPUT = table.concat(results,"\n")
