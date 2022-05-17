# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['Application.py'],
             pathex=['C:\\Users\\sklump\\OneDrive - HDR, Inc\\Apps\\IHSDM Optimization App'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=['win32com','certifi','etc','importlib_metadata-1.6.0-py3.7.egg-info','Include','IPython','jedi','jsonschema','jsonschema-3.2.0-py3.7.egg-info','lib2to3','markupsafe','matplotlib','mpl-data','nbconvert','nbconvert-5.6.1-py3.7.egg-info','nbformat','notebook','scipy','share','tornado','zmq'],
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
          name='Application',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False , icon='icon.ico')
