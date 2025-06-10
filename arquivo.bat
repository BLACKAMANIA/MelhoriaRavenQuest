@echo off
echo Ativando ambiente virtual...
call .venv\Scripts\activate

echo Criando executável com PyInstaller...
pyinstaller --noconfirm --onefile --windowed ^
--icon=icon.ico ^
--add-data "background.png;." ^
--add-data "interface_config.json;." ^
otimizador_ravenquest.py

echo.
echo ✅ Executável gerado em: dist\otimizador_ravenquest.exe
pause
