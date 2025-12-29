# -*- mode: python ; coding: utf-8 -*-

hiddenimports = [
    'sqlalchemy',
    'sqlalchemy.dialects',
    'sqlalchemy.dialects.sqlite',
    'sqlalchemy.dialects.postgresql',
    'sqlalchemy.dialects.mysql',
    'sqlalchemy.ext',
    'sqlalchemy.ext.declarative',
    'sqlalchemy.orm',
    'sqlalchemy.sql',
    'sqlalchemy.util',
    'sqlalchemy.event',
    'sqlalchemy.pool',
    'sqlalchemy.engine',
    'sqlalchemy.schema',
    'rich',
]

a = Analysis(
    ['src/task_manager/main.py'],
    pathex=[],
    binaries=[],
    datas=[('src/task_manager/database.py', '.')],
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='task-manager',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
