# autoPunchIn

Punchin is an automation tool which interacts with the ZingHR website and mark attendance on behalf of the employee. Punchin can be set up to run at specific times, such as when an employee arrives at the office in the morning or when they leave in the evening.

## Convert Python Script to EXE
```
pyinstaller --noconfirm --onedir --console --icon "F:/Windowcmd/Python/punchin/favicon.ico"  "F:/Windowcmd/Python/punchin/punchin.py"
```
## or
1. Run auto-py-to-exe interactive mode
```
auto-py-to-exe
```
2. select main punchin.py file, add icon file, add assets folder and autoPunchin.xml to additional files(you can add it later by copy-pasting it punchin directory)

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
9. Overwrite? -> N (This step has been skiped so copy all resource(all dirs and .html files) again in public directory)
10. deploy (before that modify the firebase json) for punchin deployment only
11.
```
    {
  "hosting": {
	"site": "punchin",
    "public": "public",
    "ignore": [
      "firebase.json",
	  "**/.*",
      "**/node_modules/**"
    ]
  }
}
```
```
firebase deploy --only hosting:punchin
```
