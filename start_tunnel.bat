@echo off
chcp 65001 > nul
title TehNadzor Tunnel

echo ============================================================
echo 🌍 Создание публичного туннеля для TehNadzor...
echo ============================================================
echo.

echo Проверка, запущен ли сервер...
curl -s http://localhost:8000/docs > nul 2>&1
if errorlevel 1 (
    echo ❌ ОШИБКА: Сервер не запущен!
    echo.
    echo Сначала запустите: start_server.bat
    echo.
    pause
    exit /b 1
)

echo ✅ Сервер работает!
echo.
echo Создание туннеля...
echo.

lt --port 8000 --subdomain stroinadzor-api

pause
