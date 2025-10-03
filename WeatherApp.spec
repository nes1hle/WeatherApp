# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['WeatherApp.py'],
    pathex=[],
    binaries=[],
    datas=[('Data/leaves.png', '.'), ('Data/weather.png', '.'), ('Data/thunder_cloud_and_rain.png', '.'), ('Data/partly_sunny_rain.png', '.'), ('Data/rain_cloud.png', '.'), ('Data/snow_cloud.png', '.'), ('Data/tornado.png', '.'), ('Data/sunny.png', '.'), ('Data/cloud.png', '.')],
    hiddenimports=[],
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
    name='WeatherApp',
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
    icon=['Data/weather.ico'],
)
