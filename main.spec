# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['main.py'],
    hiddenimports=[".venv/Lib/Site-Packages","pyqtgraph.console.template_pyqt5",
        "pyqtgraph.graphicsItems.ViewBox.axisCtrlTemplate_pyqt5",
        "pyqtgraph.graphicsItems.PlotItem.plotConfigTemplate_pyqt5",
        "pyqtgraph.imageview.ImageViewTemplate_pyqt5",
        "pyqtgraph.GraphicsScene.mouseDragTemplate_pyqt5",
        "pyqtgraph.GraphicsScene.exportDialogTemplate_pyqt5", 
        ],
    binaries=[],
    datas=[],
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
    name='main',
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
