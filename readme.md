## how to bundle and publish window/osx program

go to BLC.spec file, you need to fix the following two lines
line 7 pathex
line 17 image_files

to your current source file directory

save BLC.spec

in terminal/command line run
pyinstaller .\BLC.spec
