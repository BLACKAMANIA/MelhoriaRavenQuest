@echo off
cd d CUsersJeffersonDesktopNova pasta

echo Instalando PyInstaller (se necessário)...
python -m pip install pyinstaller

echo.
echo Compilando 'Otimizador RavenQuest' com ícone e janela oculta...
python -m pyinstaller --noconfirm --onefile --windowed --icon=icon.ico otimizador_ravenquest.py

echo.
echo ✅ Compilação finalizada com sucesso!
echo ➤ Executável criado em distotimizador_ravenquest.exe
pause
