rem --onefile
pyinstaller.exe main.py --add-data="resources;resources" ^
    --icon "resources\icons8-quill-with-ink-48.png" ^
    --noconsole ^
    --noconfirm    ^
    --clean   ^
    --name PenBoard
