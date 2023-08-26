set distpath=../../system/dist
set buildpath=../../system/build

pyinstaller main.spec --distpath %distpath% --workpath %buildpath% && python remove.py %distpath%/main