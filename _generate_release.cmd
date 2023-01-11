CALL .\venv\Scripts\activate.bat
cd src
py -m PyInstaller --uac-admin --distpath ".\..\_WINDOWS_RELEASE" --workpath ".\..\_WINDOWS_BUILD" -w -F main.py
cd ..
copy .\settings.ini .\_WINDOWS_RELEASE\