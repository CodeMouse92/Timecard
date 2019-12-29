# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

added_files = [
    ('timecard/resources', 'timecard/resources')
]

a = Analysis(['timecard_app.py'],
             pathex=['/home/jason/Code/Repositories/timecard'],
             binaries=[],
             datas=added_files,
             hiddenimports=['PySide2'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='timecard',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False )
