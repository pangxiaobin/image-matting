# -*- mode: python ; coding: utf-8 -*-

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--debug", action="store_true")
options = parser.parse_args()

block_cipher = None

# 分析步骤，收集所需的文件和依赖项
a = Analysis(
    ["main.py"],
    pathex=[],
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
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# 根据是否为调试模式设置不同的 EXE 和 COLLECT 参数
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="ImageMatting",
    debug=options.debug,  # 设置调试模式
    bootloader_ignore_signals=False,
    strip=False,  # 非调试模式时移除符号表
    upx=not options.debug,  # 非调试模式时使用 UPX 压缩
    console=options.debug,  # 调试模式时显示控制台窗口
    disable_windowed_traceback=not options.debug,  # 非调试模式时禁用窗口化的回溯
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon="assets/icon.ico",
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=not options.debug,  # 非调试模式时使用 UPX 压缩
    upx_exclude=[],
    name="image-matting_debug" if options.debug else "image-matting",
)
