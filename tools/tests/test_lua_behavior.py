"""Run actual shipped Lua with minimal host stubs; this is NOT in-game LQA."""
import ctypes
import ctypes.util
import os
import json
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from custom_assets import load_custom_assets

TOOLS=Path(__file__).resolve().parents[1]
MOD=Path(os.environ.get('FU_TEST_MOD_DIR', str(TOOLS/'raw_overrides')))
FIXTURES=Path(__file__).parent/'lua'


class LuaBehaviorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        library=ctypes.util.find_library('lua5.4')
        if not library:
            try:
                from lupa.lua54 import LuaRuntime, LuaError
            except ImportError as exc:
                raise RuntimeError('Lua QA requires liblua5.4 or pip install lupa==2.8.') from exc
            cls.runtime_class, cls.lua_error = LuaRuntime, LuaError
            return
        cls.lua=ctypes.CDLL(library)
        lua=cls.lua
        lua.luaL_newstate.restype=ctypes.c_void_p
        lua.luaL_openlibs.argtypes=[ctypes.c_void_p]
        lua.luaL_loadbufferx.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.c_size_t,ctypes.c_char_p,ctypes.c_char_p]
        lua.luaL_loadbufferx.restype=ctypes.c_int
        lua.lua_pcallk.argtypes=[ctypes.c_void_p,ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.c_ssize_t,ctypes.c_void_p]
        lua.lua_pcallk.restype=ctypes.c_int
        lua.lua_tolstring.argtypes=[ctypes.c_void_p,ctypes.c_int,ctypes.POINTER(ctypes.c_size_t)]
        lua.lua_tolstring.restype=ctypes.c_void_p
        lua.lua_getglobal.argtypes=[ctypes.c_void_p,ctypes.c_char_p]
        lua.lua_getglobal.restype=ctypes.c_int
        lua.lua_close.argtypes=[ctypes.c_void_p]

    def string_at(self,state,index):
        size=ctypes.c_size_t()
        ptr=self.lua.lua_tolstring(state,index,ctypes.byref(size))
        return ctypes.string_at(ptr,size.value).decode('utf-8','replace') if ptr else ''

    def execute(self,program,run=True):
        if hasattr(self, 'runtime_class'):
            runtime = self.runtime_class()
            try:
                if run:
                    runtime.execute(program, name='@fu_lua_qa')
                    return runtime.globals().AUDIT_OUTPUT or ''
                runtime.compile(program, name='@fu_lua_qa')
                return ''
            except self.lua_error as exc:
                self.fail(str(exc))
        lua=self.lua;state=lua.luaL_newstate()
        self.assertTrue(state, 'Lua state allocation failed')
        try:
            lua.luaL_openlibs(state)
            code=program.encode('utf-8')
            status=lua.luaL_loadbufferx(state,code,len(code),b'@fu_lua_qa',None)
            if not status and run:status=lua.lua_pcallk(state,0,0,0,0,None)
            self.assertEqual(status,0,self.string_at(state,-1))
            if run:
                lua.lua_getglobal(state,b'AUDIT_OUTPUT')
                return self.string_at(state,-1)
            return ''
        finally:lua.lua_close(state)

    def scenarios(self,asset,fixture,expected):
        program='require = function(...) end\n'+(MOD/asset).read_text(encoding='utf-8')+'\n'+(FIXTURES/fixture).read_text(encoding='utf-8')
        rows=self.execute(program).splitlines()
        self.assertEqual(len(rows),expected)
        for line in rows:
            name,status,detail=line.split('\t',2)
            with self.subTest(name=name):self.assertEqual(status,'PASS',detail)

    def test_typewriter_14_scenarios(self):
        self.scenarios('zb/zb_textTyper.lua','typewriter.lua',14)

    def test_mech_fuel_8_scenarios(self):
        self.scenarios('interface/mechfuel/mechfuel.lua','mechfuel.lua',8)

    def test_ebrar_ship_12_scenarios(self):
        asset = 'scripts/fu_tr_ebrar_ship.lua'
        source = MOD / asset
        if not source.is_file():
            source = TOOLS / 'custom_assets' / asset
        fixture = (FIXTURES / 'ebrar_ship.lua').read_text(encoding='utf-8')
        before, after = fixture.split('-- SCRIPT UNDER TEST', 1)
        rows = self.execute(before + source.read_text(encoding='utf-8') + after).splitlines()
        self.assertEqual(len(rows), 12)
        for line in rows:
            name, status, detail = line.split('\t', 2)
            with self.subTest(name=name):
                self.assertEqual(status, 'PASS', detail)

    def test_every_raw_override_is_valid_lua(self):
        files=sorted(MOD.rglob('*.lua'))
        expected={s['asset'] for name in ('raw_text_translations.json','raw_runtime_overrides.json')
                  for s in json.loads((TOOLS/name).read_text(encoding='utf-8'))['assets'] if s['asset'].endswith('.lua')}
        if MOD.resolve() != (TOOLS/'raw_overrides').resolve():
            expected.update(name for name in load_custom_assets(TOOLS) if name.endswith('.lua'))
        self.assertEqual({p.relative_to(MOD).as_posix() for p in files},expected)
        for file in files:
            with self.subTest(file=str(file)):self.execute(file.read_text(encoding='utf-8'),run=False)

if __name__=='__main__':unittest.main()
