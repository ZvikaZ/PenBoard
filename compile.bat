rem --onefile
pyinstaller.exe main.py --add-data="resources;resources" ^
    --icon "resources\icons8-quill-with-ink-48.png" ^
    --noconsole ^
    --noconfirm    ^
    --clean   ^
    --name PenBoard

"C:\Program Files (x86)\NSIS\Bin\makensis.exe" PenBoard.nsi
