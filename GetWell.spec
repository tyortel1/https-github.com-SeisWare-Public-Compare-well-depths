# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['GetWell.py'],
    pathex=[],
    binaries=[('_seisware_sdk_37.pyd', '.')],
    datas=[('C:\\Users\\jerem\\AppData\\Local\\Programs\\Python\\Python37\\python37.dll', '.'), ('libzmq-mt-4_3_0.dll', '.'), ('mfc140u.dll', '.'), ('msvcp140.dll', '.'), ('SWSDKCore.dll', '.'), ('vcruntime140.dll', '.'), ('__init__.py', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='GetWell',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
