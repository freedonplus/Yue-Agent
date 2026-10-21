# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller 打包配置：Yue Agent Python 后端 -> 单文件 exe（Tauri sidecar）

用法（在 Yue agent 目录下）：
    .venv\\Scripts\\python.exe -m PyInstaller build_sidecar.spec --noconfirm

产物：dist/yue-backend.exe
"""

from PyInstaller.utils.hooks import collect_all, collect_submodules

# ── 隐式导入：FastAPI 路由、LangChain/LangGraph 动态加载的模块 ──
hiddenimports = []

# app / Yue 两个包全部子模块（路由是运行时 import 的，静态分析抓不到）
for pkg in ("app", "Yue"):
    try:
        hiddenimports += collect_submodules(pkg)
    except Exception:
        pass

# 第三方动态加载的包：让 PyInstaller 完整收集
for pkg in (
    "uvicorn",
    "fastapi",
    "starlette",
    "pydantic",
    "pydantic_settings",
    "sqlalchemy",
    "aiosqlite",
    "langchain",
    "langchain_core",
    "langchain_anthropic",
    "langchain_deepseek",
    "langgraph",
    "langgraph_checkpoint_sqlite",
    "langgraph_sdk",
    "langchain_mcp_adapters",
    "mcp",
    "httpx",
    "anyio",
):
    try:
        datas, binaries, imports = collect_all(pkg)
        hiddenimports += imports
    except Exception:
        pass

# uvicorn 的协议/循环实现是按字符串 import 的
hiddenimports += [
    "uvicorn.logging",
    "uvicorn.loops",
    "uvicorn.loops.auto",
    "uvicorn.loops.asyncio",
    "uvicorn.protocols",
    "uvicorn.protocols.http",
    "uvicorn.protocols.http.auto",
    "uvicorn.protocols.http.h11_impl",
    "uvicorn.protocols.websockets",
    "uvicorn.protocols.websockets.auto",
    "uvicorn.lifespan",
    "uvicorn.lifespan.on",
    "uvicorn.lifespan.off",
]

# ── 运行时资源：template/ 与 skills/ 放到 exe 同级的目录 ──
datas_extra = [
    ("template", "template"),
    ("skills", "skills"),
]

a = Analysis(
    ["main.py"],
    pathex=["src"],
    binaries=[],
    datas=datas_extra,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        "tkinter",
        "matplotlib",
        "numpy",
        "pandas",
        "PIL",
        "PyQt5",
        "PySide2",
        "notebook",
        "IPython",
        "pytest",
    ],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="yue-backend",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,          # 无控制台窗口（sidecar 后台运行）
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
