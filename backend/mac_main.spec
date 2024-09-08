lblock_cipher = None

# 分析步骤，收集所需的文件和依赖项
a = Analysis(
    ["main.py"],
    pathex=[],  # 确保包含当前目录
    binaries=[],
    datas=[
        ('./web', 'web'),  # 收集 web 目录
        ('./hub_model', 'hub_model'),
        ('./assets', 'assets'),
        ('config.json', '.'),
        ('./.venv/lib/python3.12/site-packages/tinify', 'tinify')

    ],
    hiddenimports=['api', 'conf', 'hub_model', 'utilities', 'loguru'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='MacImageMatting',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = BUNDLE(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name='MacImageMatting.app',
    icon='assets/icon.icns',
    bundle_identifier="com.example.image-matting", 
)

