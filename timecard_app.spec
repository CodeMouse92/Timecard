# -*- mode: python ; coding: utf-8 -*-

def filter_binaries(all_binaries):
    exclude_binaries = set()
    for binary, path, type in all_binaries:
        if type != "BINARY":
            continue
        if "site-packages" in path:
            continue
        if "libpython3" in binary:
            continue

        exclude_binaries.add((binary, path, type))

    binaries = [x for x in all_binaries if x not in exclude_binaries]

    with open('dist/binary_list.txt', 'w') as file:
        for name, path, type in binaries:
            print(f".. Including {type} {path}")
            file.write(f"Including {type} {path}.\n")

        file.write("\n")

        for name, path, type in exclude_binaries:
            print(f">> EXCLUDING {type} {path}")
            file.write(f"EXCLUDING {type} {path}.\n")

        file.write("\n")

        info = "On Debian, use `dpkg -S <pkg_name> to find dependency packages."

        print(info)
        file.write(f"{info}\n")

    return binaries

block_cipher = None

added_files = [
    ('timecard/resources', 'timecard/resources')
]

a = Analysis(['timecard_app.py'],
             pathex=['./timecard'],
             binaries=[],
             datas=added_files,
             hiddenimports=['PySide2'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False
             )

pyz = PYZ(a.pure,
          a.zipped_data,
          cipher=block_cipher
          )

exe = EXE(pyz,
          a.scripts,
          filter_binaries(a.binaries),
          a.zipfiles,
          a.datas,
          [],
          name='timecard_app',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False
          )
