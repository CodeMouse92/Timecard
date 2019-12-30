# -*- mode: python ; coding: utf-8 -*-
import subprocess

def find_package(path, prefix=''):
    try:
        process = subprocess.check_output(
            ("dpkg", "-S", f"{prefix}{path}"),
            stderr=subprocess.DEVNULL,
            encoding='utf-8'
            )
    except subprocess.CalledProcessError:
        if prefix == '':
            return find_package(path, prefix='/usr')
        else:
            return None
    except FileNotFoundError:
        print("Could not find 'dpkg' (this probably isn't a Debian system.)")
        return None
    else:
        return process.split(':')[0]

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
        packages = set()
        for name, path, type in binaries:
            print(f"    Including {type} {path}")

        print("\n")

        for name, path, type in exclude_binaries:
            package = find_package(path)
            print(f"    EXCLUDING {type} {path}")
            if package:
                packages.add(package)
                print(f"    from package {package}\n")
            else:
                print(f"/!\ WARNING: No package found\n")

        for package in packages:
            file.write(f"{package}\n")

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
          name='timecard-app',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False
          )
