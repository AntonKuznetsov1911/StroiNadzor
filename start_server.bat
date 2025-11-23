@echo off
chcp 65001 > nul
title TehNadzor Server

echo ============================================================
echo 🚀 Запуск TehNadzor сервера...
echo ============================================================
echo.

cd /d "%~dp0backend"

echo [1/2] Запуск FastAPI сервера...
start /min "TehNadzor-API" cmd /c python demo_server.py

echo [2/2] Ожидание запуска сервера...
timeout /t 5 /nobreak > nul

echo.
echo ✅ Сервер запущен!
echo.
echo 🌐 Локальный доступ:
echo    http://localhost:8000/docs
echo.
echo 📝 Для публичного доступа запустите: start_tunnel.bat
echo.
echo Нажмите любую клавишу для выхода...
pause > nul
