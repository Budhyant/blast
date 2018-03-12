# -*- mode: python -*-

block_cipher = None


a = Analysis(['render.py'],
             pathex=['C:\\Users\\JohnnyKoo\\Downloads\\BLC_180311'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
image_files =  [('dimension.png', 'C:\\Users\\JohnnyKoo\\Downloads\\BLC_180311\\dimension.png', 'DATA')]
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='BLC',
          debug=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas + image_files,
               strip=False,
               upx=True,
               name='BLC')
