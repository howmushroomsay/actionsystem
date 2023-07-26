set distpath=../../action_exe/system/dist
set buildpath=../../action_exe/system/build

pyinstaller main.spec --distpath %distpath% --workpath %buildpath%
python remove.py %distpath%/main