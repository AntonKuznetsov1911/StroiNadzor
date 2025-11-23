@echo off
chcp 65001 > nul
title TehNadzor - Полный запуск

echo ============================================================
echo 🚀 Полный запуск TehNadzor (Сервер + Туннель)
echo ============================================================
echo.

cd /d "%~dp0backend"

echo [1/3] Запуск FastAPI сервера...
start /min "TehNadzor-API" cmd /c python demo_server.py

echo [2/3] Ожидание запуска сервера (5 сек)...
timeout /t 5 /nobreak > nul

echo [3/3] Создание публичного туннеля...
start "TehNadzor-Tunnel" cmd /k lt --port 8000 --subdomain stroinadzor-api

echo.
echo ✅ Все запущено!
echo.
echo 🌐 Локальный доступ:
echo    http://localhost:8000/docs
echo.
echo 🌍 Публичный доступ:
echo    https://stroinadzor-api.loca.lt/docs
echo.
echo 📝 Два окна открыты:
echo    - TehNadzor-API (минимизировано)
echo    - TehNadzor-Tunnel (показывает статус)
echo.
echo 💡 Чтобы открыть Swagger UI в браузере...
timeout /t 3 /nobreak > nul
start https://stroinadzor-api.loca.lt/docs

echo.
echo Нажмите любую клавишу для выхода...
pause > nul
