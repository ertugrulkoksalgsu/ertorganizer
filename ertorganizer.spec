# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller derleme tarifi — ertorganizer'i tek bir standalone binary'ye paketler.

Hem macOS hem Windows runner'inda calisir:  pyinstaller ertorganizer.spec
Sistem araclari (poppler, LibreOffice, pandoc) paketlenmez; onlar disarida
kalir ve eksikse calisma aninda graceful error ile kullaniciya bildirilir.
"""

from PyInstaller.utils.hooks import collect_all

# Opsiyonel bagimliliklar fonksiyon icinde lazy import ediliyor; her birinin
# alt modullerini ve veri dosyalarini acikca topla ki binary eksiksiz olsun.
_packages = [
    "pdf2image",
    "pypdf",
    "pdf2docx",
    "docx2pdf",
    "docx",
    "pypandoc",
    "openpyxl",
    "markdown",
    "rich",
    "prompt_toolkit",
]

datas = []
binaries = []
hiddenimports = []

for _pkg in _packages:
    try:
        _d, _b, _h = collect_all(_pkg)
        datas += _d
        binaries += _b
        hiddenimports += _h
    except Exception:
        # Paket bu ortamda kurulu degilse atla; ilgili donusum calisma
        # aninda zaten graceful error verir.
        pass

a = Analysis(
    ["pyi_entry.py"],
    pathex=["."],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=["tkinter", "test_folder"],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="ertorganizer",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
)
