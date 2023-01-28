# autoPunchIn

## Convert Python Script to EXE
```
pyinstaller --noconfirm --onedir --console --icon "F:/Windowcmd/Python/punchin/favicon.ico"  "F:/Windowcmd/Python/punchin/punchin.py"
```


## FireBase deploy commands

1. firebase login
```
firebase login
```
2. allow collection of info -> Y
3. firebase init
```
firebase init
```
4. are you ready to procces -> Y
5. use up,down and space bar for selection, select hosting, press Enter
6. use your public directory-> public
7. single page app -> N
8. Set up automatic -> N
9. Overwrite? -> N
10. deploy
```
firebase deploy --only hosting:punchin
```
