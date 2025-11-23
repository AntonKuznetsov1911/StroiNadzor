@echo off
chcp 65001 > nul
title Удалить из автозагрузки

echo ============================================================
echo 🗑️ Удаление TehNadzor из автозагрузки Windows
echo ============================================================
echo.

set "STARTUP_FOLDER=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"

if exist "%STARTUP_FOLDER%\TehNadzor.lnk" (
    del "%STARTUP_FOLDER%\TehNadzor.lnk"
    echo ✅ TehNadzor удален из автозагрузки
) else (
    echo ℹ️ TehNadzor не найден в автозагрузке
)

echo.
pause
