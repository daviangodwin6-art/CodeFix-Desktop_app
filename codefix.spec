# PyInstaller build of the CodeFix desktop app (onedir, no console). Build: pyinstaller codefix.spec
# Needs frontend/dist (committed; rebuild with `npm run build` in frontend/). Output: dist/CodeFix/CodeFix.exe
# .env is deliberately NOT bundled: the app reads %APPDATA%\CodeFix\.env (agent/paths.py).
from PyInstaller.utils.hooks import collect_submodules

a = Analysis(
    ["desktop.py"],
    pathex=[],
    # Read at runtime from sys._MEIPASS (agent/paths.bundle_dir). Nothing else in agent/ reads files of its own.
    datas=[("frontend/dist", "frontend/dist")],
    # uvicorn picks its loop/protocol/lifespan modules by name at runtime; google.genai is imported lazily.
    hiddenimports=collect_submodules("uvicorn") + collect_submodules("google.genai") + ["server"],
    excludes=["pytest", "_pytest", "tkinter"],
    noarchive=False,
)
pyz = PYZ(a.pure)
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="CodeFix",
    icon="assets/codefix.ico",
    console=False,
    upx=False,
)
coll = COLLECT(exe, a.binaries, a.datas, name="CodeFix", upx=False)
