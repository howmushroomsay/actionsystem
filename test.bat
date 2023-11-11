@REM set distpath=../../system/dist
@REM set buildpath=../../system/build
set distpath=../../widget/dist
set buildpath=../../widget/build
pyinstaller main.spec --distpath %distpath% --workpath %buildpath% && python remove.py %distpath%/main