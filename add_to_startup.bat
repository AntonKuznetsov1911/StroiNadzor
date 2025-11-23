@echo off
chcp 65001 > nul
title Добавить в автозагрузку

echo ============================================================
echo 🔧 Добавление TehNadzor в автозагрузку Windows
echo ============================================================
echo.

set "STARTUP_FOLDER=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
set "SCRIPT_PATH=%~dp0start_all.bat"

echo Создание ярлыка в автозагрузке...
echo.

powershell -Command "$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut('%STARTUP_FOLDER%\TehNadzor.lnk'); $s.TargetPath = '%SCRIPT_PATH%'; $s.WorkingDirectory = '%~dp0'; $s.WindowStyle = 7; $s.Save()"

if exist "%STARTUP_FOLDER%\TehNadzor.lnk" (
    echo ✅ Успешно добавлено в автозагрузку!
    echo.
    echo 📍 Местоположение ярлыка:
    echo    %STARTUP_FOLDER%\TehNadzor.lnk
    echo.
    echo 💡 Теперь TehNadzor будет запускаться автоматически при старте Windows
    echo.
    echo Хотите открыть папку автозагрузки? (Y/N)
    choice /c YN /n /m "Ваш выбор: "
    if errorlevel 2 goto end
    if errorlevel 1 explorer "%STARTUP_FOLDER%"
) else (
    echo ❌ ОШИБКА: Не удалось создать ярлык
)

:end
echo.
pause
