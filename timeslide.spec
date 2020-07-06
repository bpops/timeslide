# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(['timeslide.py'],
             pathex=['.'],
             binaries=[],
             datas=[('models/*','models')],
             hiddenimports=[],
             hookspath=['hooks'],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

# libpng
a.binaries = a.binaries - TOC([('libpng16.16.dylib',None,None)])
a.binaries = a.binaries + TOC([('libpng16.16.dylib', 
    '/usr/local/Cellar/libpng/1.6.37/lib/libpng16.16.dylib', 'BINARY')])

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='TimeSlide',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False )

app = BUNDLE(exe,
             name='timeslide.app',
             icon=None,
             bundle_identifier=None,
             info_plist={
                 'NSHighResolutionCapable': 'True', # remove blurriness
             },)