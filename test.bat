set distpath=../../system/dist
set buildpath=../../system/build
@REM set distpath=../../widget/dist
@REM set buildpath=../../widget/build
pyinstaller main.spec --distpath %distpath% --workpath %buildpath% && python remove.py %distpath%/main