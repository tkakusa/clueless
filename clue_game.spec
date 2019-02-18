# -*- mode: python -*-

block_cipher = None


a = Analysis(['clue_game.py'],
             pathex=['C:\\Users\\TK\\Anaconda3\\pkgs\\vs2015_runtime-15.5.2-3\\Library\\bin', 'D:\\Projects\\clueless'],
             binaries=[],
             datas=[],
             hiddenimports=[],
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
          name='clue_game',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True )
